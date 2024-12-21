import pygame

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def draw_field(left_bound: float, right_bound: float, screen: pygame.Surface):
    """
    Draws the field onto the screen

    :param left_bound: x coordinate where field starts on screen
    :param right_bound: x coordinate where field ends on screen
    :param screen: surface object of display window
    """
    height = screen.get_height()

    pixels_per_yard = height / 120
    ten_yards = 10 * pixels_per_yard
    font = pygame.font.Font(pygame.font.get_default_font(), 25)


    # Yard markers
    for i in range(10, 100, 10):
        draw_line_from_yard(i, (left_bound, right_bound), screen)
        if i <= 50:
            number = pygame.transform.rotate(font.render(f"{i}", True, WHITE), 90)
        else:
            number = pygame.transform.rotate(font.render(f"{-i+100}", True, WHITE), 90)

        screen.blit(number, (left_bound, (i + 7.5) * pixels_per_yard))

    # Defense End Zone
    surface = pygame.Surface((right_bound - left_bound, ten_yards))
    surface.fill(BLUE)
    screen.blit(surface, (left_bound, 0))
    pygame.draw.line(screen, WHITE, (left_bound, ten_yards), (right_bound, ten_yards),2)

    # OFFENSE END ZONE
    surface.fill(RED)
    screen.blit(surface, (left_bound, 11*ten_yards))
    pygame.draw.line(screen, WHITE, (left_bound, 11*ten_yards), (right_bound, 11*ten_yards),2)

    # Bounds
    surface = pygame.Surface((10, height))
    surface.fill(WHITE)
    screen.blit(surface, (left_bound - 10, 0))
    screen.blit(surface, (right_bound, 0))


def draw_line_from_yard(yard: int, bounds: tuple[float, float], screen: pygame.Surface, offset=10, color=WHITE):
    """
    Draws a line horizontally across the field at the given yardage

    :param yard: Yard on field to draw the line across
    :param bounds: X coordinate bounding the field on screen
    :param screen: surface object of display window
    :param offset: yards added to given yards, defaults 10 to offset space used by the end zone
    :param color: RGB value of the line
    """
    pixels_per_yard = screen.get_height() / 120
    start = (bounds[0], (yard + offset) * pixels_per_yard)
    end = (bounds[1], (yard + offset) * pixels_per_yard)
    pygame.draw.line(screen, color, start, end, 2)


def draw_line_from_pixel(pixel: float, bounds: tuple[float, float], screen: pygame.Surface, color=(255, 255, 255)):
    """
    Draws a line horizontally across the field at the given y coordinate/pixel

    :param pixel: y coordinate to draw the line across
    :param bounds: X coordinates bounding the field on screen
    :param screen: surface object of display window
    :param color: RGB value of the line
    """
    start = (bounds[0], pixel)
    end = (bounds[1], pixel)
    pygame.draw.line(screen, color, start, end, 2)


def yard_to_pixel(yard: int, height: float, offset=10):
    """
    converts the given yard on the field to its coordinate

    :param yard: yard on field to convert
    :param height: height of the screen/window
    :param offset: yards added to given yards, defaults 10 to offset space used by the end zone
    :return: y coordinate
    """
    return (yard + offset) * (height / 120)
