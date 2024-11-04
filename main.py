import pygame
import field
import team
import gridiron
from copy import deepcopy
import random


def main():
    """
    Handle the operations of running the simulation
    """
    pygame.init()
    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("FootballAI")
    clock = pygame.time.Clock()

    # Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((24, 150, 0))
    screen.blit(background, (0, 0))

    # Get Bounds
    screen_size = screen.get_size()
    field_bounds = (screen_size[0] / 4, screen_size[0] * 3 / 4)

    # Prep first gen teams
    active_offense = []
    active_defense = []

    for i in range(350):
        active_offense.append(team.Offense())
        active_defense.append(team.Defense())

    active_games = []

    # States
    time = 0
    gen = 0
    purge = True

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw field
        screen.blit(background, (0, 0))
        field.draw_field(field_bounds[0], field_bounds[1], screen)

        # Fill Games
        if purge:

            active_games.clear()

            # Create copies of new winners now in active
            for i in range(len(active_offense)):
                new_offense, new_defense = copy(active_offense[i], active_defense[i])
                active_offense.append(new_offense)
                active_defense.append(new_defense)

            random.shuffle(active_offense)
            random.shuffle(active_defense)

            for o, d in zip(active_offense, active_defense):
                active_games.append(gridiron.Gridiron(o, d, field_bounds, screen))

            active_games[0].display = True

            # Reset time and purge
            purge = False
            gen += 1
            print(f"Generation #{gen}")
            time = 0
        else:
            # Have all active games and
            time += 1
            for i in range(len(active_games)):
                active_games[i].update()

            if time > 600:
                active_offense.clear()
                active_defense.clear()
                active_games.sort(key=lambda x: x.points, reverse=True)
                for winner_idx in range(int(len(active_games) / 2)):
                    active_offense.append(active_games[winner_idx].offense)
                for winner_idx in range(int(len(active_games) / 2), len(active_games)):
                    active_defense.append(active_games[winner_idx].defense)

                purge = True

        # print(clock.get_fps())

        pygame.display.flip()
    pygame.quit()


def copy(old_offense: team.Offense, old_defense: team.Defense) -> tuple[team.Offense, team.Defense]:
    """
    copies the given offense and defense. Creates a deep copy of their networks and runs neural_net.mutate()

    :param old_offense: offense to be copied
    :param old_defense: defense to be copied
    :return: the new offense and defense created
    """
    new_offense = team.Offense()
    new_defense = team.Defense()

    for o, n in zip(old_offense.players, new_offense.players):
        n.network.weights = deepcopy(o.network.weights)
    for o, n in zip(old_defense.players, new_defense.players):
        n.network.weights = deepcopy(o.network.weights)

    new_offense.mutate()
    new_defense.mutate()
    return new_offense, new_defense


if __name__ == "__main__":
    main()
