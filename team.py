import pygame
from field import Field
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
        self.players = pygame.sprite.Group()
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

    def set_team(self, playing_field: Field, y_bound, starting_angle):
        """
        PLace a teams players before the start of a play.

        :param playing_field: field object of game
        :param y_bound: y coordinate for where players may be placed
        :param starting_angle: angle players on the team face on play start
        """
        for player in self.players:
            x = random.uniform(0, (playing_field.right_bound - playing_field.left_bound) / 2) + 1.25 * playing_field.left_bound
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

    def set_offense(self, playing_field: Field):
        """
        sets the offense by calling Team.set_team() with proper parameters

        :param playing_field: field object team plays on
        """
        self.set_team(playing_field, playing_field.yard_to_pixel(80), 90)


class Defense(Team):
    """
    Subclass of Team representing a defense
    """
    def __init__(self):
        super().__init__(DEFENSE_POSITIONS, DEFENSE_STATS, "Blue")

    def set_defense(self, playing_field: Field):
        """
        sets the defense by calling Team.set_team() with proper parameters

        :param playing_field: field object team plays on
        """
        self.set_team(playing_field, playing_field.yard_to_pixel(20), 270)
