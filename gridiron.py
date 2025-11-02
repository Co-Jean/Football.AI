from team import *
from field import *
from player import *


class Gridiron:
    """
    Object for controlling a game between two teams, an offense and defense
    """
    def __init__(self, offense: Offense, defense: Defense, screen: pygame.Surface):
        # Display
        self.screen = screen
        self.display = False

        # Teams
        self.offense = offense
        self.defense = defense

        # Field bounds and coordinates
        self.field = Field(screen)

        # Game state
        self.in_play = False
        self.points = 0

    def update(self):
        """
        Update the game object. This means either preparing a new play or
        allowing all players to update.

        This will only render updates if the Gridiron object's display attribute is True
        """
        if self.in_play:
            # allow teams to update

            self.update_net_inputs()
            if self.display:
                self.display_net_input()

            self.update_team(self.offense, self.defense)
            # self.update_team(self.defense, self.offense, half_update=True)
        else:
            # allow teams to place themselves and flip the self.in_play flag
            self.offense.set_offense(self.field)
            self.defense.set_defense(self.field)
            self.in_play = True

        if self.display:
            # render players and line of self.scrimmage
            self.field.draw_field()
            self.offense.players.draw(self.screen)
            self.defense.players.draw(self.screen)


    def update_team(self, update_team: Offense | Defense, opposing_team: Offense | Defense):
        """
        Updates each player in the team by checking if they contact the given opposing team.

        1. update players network input
        2. check player for collisions and has_ball/check_game_state
        3. if it is colliding, calculate external forces
        4. call players update function Player.update()

        :param update_team: team whose players will be updated
        :param opposing_team: team is opposing the team being updated
        """
        c = pygame.sprite.collide_rect_ratio(0.80)
        collided = pygame.sprite.groupcollide(update_team.players, opposing_team.players, False, False, collided=c)
        for player in update_team.players:

            try:
                if player.has_ball:
                    # self.check_game_state(player, collided)
                    pass

                external_force = [0, 0]
                for opponent in collided[player]:
                    corners = opponent.get_face_corners()
                    if player.rect.clipline(corners) and opponent.strength >= player.strength:
                        x, y = get_movement_vector(opponent.strength, opponent.angle)
                        external_force[0] += 2 * x
                        external_force[1] += 2 * y
                player.update(self.field, self.field.height, external_force=external_force)
            except KeyError:
                player.update(self.field, self.field.height)

            if self.display:
                player.get_corners(self.screen)

    def check_game_state(self, player: Player, collisions: dict):
        """
        checks and updates the state of the game based on the player with the ball

        :param player: Player object with the ball
        :param collisions: dict of collisions returned by pygame.sprite.groupcollide()
        """
        if player in collisions.keys():
            self.in_play = False
        if player.rect.centery <= self.field.score_endzone:
            self.in_play = False
            self.points += 7


    def update_net_inputs(self):
        """
        Update all player's input attribute for Network.feedfoward()
        """
        bounds = [self.field.left_bound, self.field.right_bound]

        for off in self.offense.players:
            paired_def = None
            for defe in self.defense.players:
                off.update_target_input(defe.rect.center, defe.player_id, self.field.max_dist)
                defe.update_target_input(off.rect.center, off.player_id, self.field.max_dist)
                if off.player_id == defe.player_id:
                    paired_def = defe

            for corner in range(len(bounds)):
                idx = -(2 - corner)
                off.update_target_input((bounds[corner], self.field.score_endzone), idx, self.field.max_dist)
                paired_def.update_target_input((bounds[corner], self.field.score_endzone), idx, self.field.max_dist)


    def display_net_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_o]:
            display_team = self.offense.players
        elif keys[pygame.K_d]:
            display_team = self.defense.players
        else:
            return

        for player in display_team:
            for i in range(0, len(player.net_input), 2):
                radian = math.radians(player.angle) - math.radians(player.net_input[i+1]*180)
                dis = player.net_input[i] * self.field.max_dist
                x = math.cos(radian) * dis
                y = math.sin(radian) * -dis
                xy = player.rect.center
                pygame.draw.line(self.screen, (255, 0, 0), xy, (xy[0]+x, xy[1]+y), 2)
