from team import *
import field
from player import *


class Gridiron:
    """
    Object for controlling a game between two teams, an offense and defense
    """
    def __init__(self, offense: Offense, defense: Defense, bounds: tuple[float, float], screen: pygame.Surface):
        # Display
        self.screen = screen
        self.display = False

        # Teams
        self.offense = offense
        self.defense = defense

        # Field bounds and coordinates
        self.bounds = bounds
        self.height = screen.get_height()
        self.score_endzone = field.yard_to_pixel(10, self.height, offset=0)
        saftey_endzone = field.yard_to_pixel(110, self.height, offset=0)
        self.max_dist = math.sqrt((self.bounds[1] - self.bounds[0]) ** 2 + (self.score_endzone - saftey_endzone) ** 2)
        self.scrimmage = field.yard_to_pixel(70, self.height)

        # Game state
        self.in_play = False
        self.points = 0

    def update(self):
        """
        Update the game object. This means either preparing a new play or
        allowing all players to update.

        This will only render updates if the Gridiron object's display attribute is True
        """
        offense_players = self.offense.players
        defensive_players = self.defense.players
        if self.in_play:
            # allow teams to update
            self.update_team(self.offense, self.defense)
            self.update_team(self.defense, self.offense, half_update=True)
        else:
            # allow teams to place themselves and flip the self.in_play flag
            self.offense.set_offense(self.bounds, self.height)
            self.defense.set_defense(self.bounds, self.height)
            self.in_play = True

        if self.display:
            # render players and line of self.scrimmage
            field.draw_line_from_pixel(self.scrimmage, self.bounds, self.screen, color=(0, 0, 255))
            offense_players.draw(self.screen)
            defensive_players.draw(self.screen)

    def update_team(self, update_team: Offense | Defense, opposing_team: Offense | Defense, half_update=False):
        """
        Updates each player in the team by checking if they contact the given opposing team.

        1. update players network input
        2. check player for collisions and has_ball/check_game_state
        3. if it is colliding, calculate external forces
        4. call players update function Player.update()

        :param update_team: team whose players will be updated
        :param opposing_team: team is opposing the team being updated
        :param half_update: whether to use the half_update argument of gridiron.net_input()
        """
        c = pygame.sprite.collide_rect_ratio(0.80)
        collided = pygame.sprite.groupcollide(update_team.players, opposing_team.players, False, False, collided=c)

        for player in update_team.players:
            self.net_input(player, opposing_team, half_update)

            try:
                if player.has_ball:
                    self.check_game_state(player, collided)

                external_force = [0, 0]
                for opponent in collided[player]:
                    corners = opponent.get_face_corners()
                    if player.rect.clipline(corners) and opponent.strength >= player.strength:
                        x, y = get_movement_vector(opponent.strength, opponent.angle)
                        external_force[0] += 2 * x
                        external_force[1] += 2 * y
                player.update(self.bounds, self.height, external_force=external_force)
            except KeyError:
                player.update(self.bounds, self.height)

    def check_game_state(self, player: Player, collisions: dict):
        """
        checks and updates the state of the game based on the player with the ball

        :param player: Player object with the ball
        :param collisions: dict of collisions returned by pygame.sprite.groupcollide()
        """
        if player in collisions.keys():
            self.in_play = False
        if player.rect.centery <= self.score_endzone:
            self.in_play = False
            self.points += 7

    def net_input(self, player: Player, opposing_team: Offense | Defense, half_update=False):
        """
        Update a player's input attribute for Network.feedfoward()

        :param player: the player updating their neural network input
        :param opposing_team: the team opposing the giving player
        :param half_update: whether to run the function as a half update, when net_input() is run.
        One component of a player's network input is their distance to another opposing player.
        Players will share this with the opposing player as it will come out to the same number.
        If all players of a team have run net_input(), half_update can be used to skip those calculations for the next.
        """

        def vision_to_obj(v, d):
            v_dot_t = (v[0] * d[0]) + (v[1] * d[1])
            v_cross_t = (v[0] * d[1]) - (v[1] * d[0])
            angle_between = math.degrees(math.atan2(v_cross_t, v_dot_t))
            return angle_between / 180

        vision_angle = math.radians(player.angle)
        vision = (math.cos(vision_angle), -math.sin(vision_angle))

        for other in opposing_team.players:
            diff = (other.rect.centerx - player.rect.centerx, other.rect.centery - player.rect.centery)
            if not half_update:
                magnitude = math.sqrt(diff[0] ** 2 + diff[1] ** 2) / self.max_dist
                player.net_input[2 * other.player_id] = magnitude
                other.net_input[2 * player.player_id] = magnitude
            player.net_input[2 * other.player_id + 1] = vision_to_obj(vision, diff)

        for corner in range(len(self.bounds)):
            diff = (self.bounds[corner] - player.rect.centerx, self.score_endzone - player.rect.centery)
            player.net_input[-2 * (2 - corner)] = math.sqrt(diff[0] ** 2 + diff[1] ** 2) / self.max_dist
            player.net_input[-2 * (2 - corner) + 1] = vision_to_obj(vision, diff)
