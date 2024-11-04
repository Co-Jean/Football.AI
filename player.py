import pygame
from os import getcwd
import math
from neural_net import Network

data_dir = getcwd() + "\\Images\\"

SIZE = 100
SCALE = 0.35


def load_image(name, scale=SCALE):
    """
    loads an image

    :param name: name of the image file
    :param scale: scale of the image in relation to original image size
    :return: the image and a matching pygame.rect object
    """
    sprite = pygame.image.load(data_dir + name)
    sprite = sprite.convert_alpha()
    size = sprite.get_size()
    scale = (size[0] * scale, size[1] * scale)

    sprite = pygame.transform.scale(sprite, scale)
    rect = sprite.get_rect()

    return sprite, rect


def get_movement_vector(length: float, angle: float) -> tuple[float, float]:
    """
    returns the vector components with given information

    :param length: magnitude of the vector
    :param angle: angle of the vector
    :return: vector components
    """
    radian = math.radians(angle)
    x = math.cos(radian) * length
    y = math.sin(radian) * -length
    return x, y


class Player(pygame.sprite.Sprite):
    """
    Object representing a player. A player can be on offense or defense on red or blue team.
    Each player is tracked on their team by the player_id attribute.
    """
    def __init__(self, role: str, color: str, stats: list[int], player_id: int):
        pygame.sprite.Sprite.__init__(self)
        # Team
        self.role = role
        self.player_id = player_id

        # stats
        self.speed = stats[0]
        self.strength = stats[1]

        # Pygame
        self.sprite, self.rect = load_image(color + "_" + role + ".png")
        self.image = pygame.Surface((SIZE * SCALE, SIZE * SCALE))

        # State
        self.angle = 90
        self.has_ball = False

        # Network
        self.network = Network([10, 2])
        self.net_input = [0]*10

    def update(self, bounds: tuple[int, int], max_height: int, external_force=(0, 0)):
        """
        Updates the player. Moves them according to the output of Network.feedfoward() and
        any external forces another player has applied to them.

        :param bounds: x coordinate bounds limiting players to the field
        :param max_height: y coordinate bound limiting players to the field
        :param external_force: any external forces being applied to the player, defaults (0, 0)
        """
        move, turn = self.network.feedforward(self.net_input)

        if turn < 0.25:
            self.angle = (self.angle + 2*self.speed) % 360
        elif turn > 0.75:
            self.angle = (self.angle - 2*self.speed) % 360

        if move > 0.50:
            x, y = get_movement_vector(self.speed, self.angle)
            x += self.rect.centerx + external_force[0]
            y += self.rect.centery + external_force[1]

            if bounds[1] > x > bounds[0]:
                self.rect.centerx = x
            if max_height > y > 0:
                self.rect.centery = y

        self.image = pygame.transform.rotate(self.sprite, self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.has_ball:
            surface = pygame.Surface((10, 10))
            surface.fill((222, 184, 135))
            self.image.blit(surface, (self.rect.width / 4, self.rect.height / 2))

    def get_face_corners(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Gets the two coordinates of the corners of a players face.

        :return: two sets coordinates
        """
        size = self.sprite.get_size()
        corner_distance = math.sqrt(size[0] ** 2 + size[1] ** 2) / 2
        radian = math.radians(self.angle + 45)
        x1 = math.cos(radian) * corner_distance + self.rect.centerx
        y1 = math.sin(radian) * -corner_distance + self.rect.centery
        radian = math.radians((self.angle - 45))
        x2 = math.cos(radian) * corner_distance + self.rect.centerx
        y2 = math.sin(radian) * -corner_distance + self.rect.centery
        return (x1, y1), (x2, y2)

