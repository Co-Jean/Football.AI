import pygame
import field
from player import Player
import random

OFFENSE_POSITIONS = {"RB": 1, "WR": 2}
OFFENSE_STATS = {"RB": [4, 5], "WR": [5, 4]}
DEFENSE_POSITIONS = {"CB": 2, "S": 1}
DEFENSE_STATS = {"CB": [5, 4], "S": [4, 5]}


class Team:
    """
    Object for controlling a team of players
    """
    def __init__(self, positions: dict, stats: dict, color: str):
        self.players = pygame.sprite.RenderPlain()
        player_id = 0
        for role, num_of in positions.items():
            for p in range(num_of):
                # noinspection PyTypeChecker
                self.players.add(Player(role, color, stats[role], player_id))
                player_id += 1

    def mutate(self):
        """
        calls Network.mutate() on player's network for each member
        """
        for player in self.players:
            player.network.mutate()

    def set_team(self, x_bounds, y_bound, starting_angle):
        """
        PLace a teams players before the start of a play.

        :param x_bounds: x coordinate bounds for the field
        :param y_bound: y coordinate for where players may be placed
        :param starting_angle: angle players on the team face on play start
        """
        for player in self.players:
            x = random.uniform(0, (x_bounds[1] - x_bounds[0]) / 2) + 1.25 * x_bounds[0]
            player.rect.center = (x, y_bound)
            player.angle = starting_angle
            player.image = player.sprite
            if player.role == "RB":
                player.has_ball = True


class Offense(Team):
    """
    Subclass of Team representing an offense
    """
    def __init__(self):
        super().__init__(OFFENSE_POSITIONS, OFFENSE_STATS, "Red")

    def set_offense(self, x_bounds: tuple[float, float], height: float):
        """
        sets the offense by calling Team.set_team() with proper parameters

        :param x_bounds: x coordinate bounds for the field
        :param height: height of the field/window in pixels
        """
        self.set_team(x_bounds, field.yard_to_pixel(80, height), 90)


class Defense(Team):
    """
    Subclass of Team representing a defense
    """
    def __init__(self):
        super().__init__(DEFENSE_POSITIONS, DEFENSE_STATS, "Blue")

    def set_defense(self, x_bounds: tuple[float, float], height: float):
        """
        sets the defense by calling Team.set_team() with proper parameters

        :param x_bounds: x coordinate bounds for the field
        :param height: height of the field/window in pixels
        """
        self.set_team(x_bounds, field.yard_to_pixel(20, height), 270)
