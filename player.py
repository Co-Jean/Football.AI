import pygame
from os import getcwd
import math
from neural_net import Network
from field import *

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
        self.net_input = [0.0]*10

    def update(self, playing_field: Field, max_height: int, external_force=(0, 0)):
        """
        Updates the player. Moves them according to the output of Network.feedfoward() and
        any external forces another player has applied to them.

        :param playing_field: field object of game
        :param max_height: y coordinate bound limiting players to the field
        :param external_force: any external forces being applied to the player, defaults (0, 0)
        """
        move, turn = self.network.feedforward(self.net_input)

        # for testing by controlling ball handler
        keys = pygame.key.get_pressed()
        if self.has_ball and keys[pygame.K_SPACE]:
            move = 0
            turn = 0.50
            if keys[pygame.K_w]:
                move = 1
            if keys[pygame.K_a]:
                turn = 0
            if keys[pygame.K_d]:
                turn = 1


        if turn < 0.25:
            self.angle = (self.angle + 2*self.speed) % 360
        elif turn > 0.75:
            self.angle = (self.angle - 2*self.speed) % 360

        if move > 0.50:
            x, y = get_movement_vector(self.speed, self.angle)
            x += self.rect.centerx + external_force[0]
            y += self.rect.centery + external_force[1]

            if playing_field.right_bound > x > playing_field.left_bound:
                self.rect.centerx = x
            if max_height > y > 0:
                self.rect.centery = y

        self.image = pygame.transform.rotate(self.sprite, self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.has_ball:
            surface = pygame.Surface((10, 10))
            surface.fill((222, 184, 135))
            self.image.blit(surface, (self.rect.width / 4, self.rect.height / 2))


    def update_target_input(self, target: tuple[float, float], other_id: int, max_dist):
        difference = (target[0] - self.rect.centerx, target[1] - self.rect.centery)

        magnitude = math.sqrt(difference[0] ** 2 + difference[1] ** 2) / max_dist
        self.net_input[2 * other_id] = magnitude

        vision_angle = math.radians(self.angle)
        v = (math.cos(vision_angle), -math.sin(vision_angle))

        v_dot_t = (v[0] * difference[0]) + (v[1] * difference[1])
        v_cross_t = (v[0] * difference[1]) - (v[1] * difference[0])
        angle_between = math.degrees(math.atan2(v_cross_t, v_dot_t))

        self.net_input[2 * other_id + 1] = angle_between / 180


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

    def get_corners(self, screen: pygame.Surface):

        size = self.sprite.get_size()
        corner_distance = math.sqrt(size[0] ** 2 + size[1] ** 2) / 2

        for i in range(4):
            radian = math.radians(self.angle + 45 + (90*i))
            x = math.cos(radian) * corner_distance + self.rect.centerx
            y = math.sin(radian) * -corner_distance + self.rect.centery
            pygame.draw.circle(screen, (0,0,0), (x, y), 5, width=0)
