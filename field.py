import pygame
import math

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Field:
    def __init__(self, bounds, height):
        self.left_bound = bounds[0]
        self.right_bound = bounds[1]

        self.height = height
        self.score_endzone = self.yard_to_pixel(10, offset=0)
        saftey_endzone = self.yard_to_pixel(110, offset=0)
        self.max_dist = math.sqrt((bounds[1] - bounds[0]) ** 2 + (self.score_endzone - saftey_endzone) ** 2)
        self.scrimmage = self.yard_to_pixel(70)

    def draw_field(self, screen: pygame.Surface):
        """
        Draws the field onto the screen

        :param screen: surface object of display window
        """
        height = screen.get_height()

        pixels_per_yard = height / 120
        ten_yards = 10 * pixels_per_yard
        font = pygame.font.Font(pygame.font.get_default_font(), 25)


        # Yard markers
        for i in range(10, 100, 10):
            self.draw_line_from_yard(i, screen)
            if i <= 50:
                number = pygame.transform.rotate(font.render(f"{i}", True, WHITE), 90)
            else:
                number = pygame.transform.rotate(font.render(f"{-i+100}", True, WHITE), 90)

            screen.blit(number, (self.left_bound, (i + 7.5) * pixels_per_yard))

        # Defense End Zone
        surface = pygame.Surface((self.right_bound - self.left_bound, ten_yards))
        surface.fill(BLUE)
        screen.blit(surface, (self.left_bound, 0))
        self.draw_line_from_yard(0, screen)

        # OFFENSE END ZONE
        surface.fill(RED)
        screen.blit(surface, (self.left_bound, 11*ten_yards))
        pygame.draw.line(screen, WHITE, (self.left_bound, 11*ten_yards), (self.right_bound, 11*ten_yards),2)

        # Bounds
        surface = pygame.Surface((10, height))
        surface.fill(WHITE)
        screen.blit(surface, (self.left_bound - 10, 0))
        screen.blit(surface, (self.right_bound, 0))


    def draw_line_from_yard(self, yard: int, screen: pygame.Surface, offset=10, color=WHITE):
        """
        Draws a line horizontally across the field at the given yardage

        :param yard: Yard on field to draw the line across
        :param screen: surface object of display window
        :param offset: yards added to given yards, defaults 10 to offset space used by the end zone
        :param color: RGB value of the line
        """
        pixels_per_yard = screen.get_height() / 120
        start = (self.left_bound, (yard + offset) * pixels_per_yard)
        end = (self.right_bound, (yard + offset) * pixels_per_yard)
        pygame.draw.line(screen, color, start, end, 2)


    def draw_line_from_pixel(self, pixel: float, screen: pygame.Surface, color=WHITE):
        """
        Draws a line horizontally across the field at the given y coordinate/pixel

        :param pixel: y coordinate to draw the line across
        :param screen: surface object of display window
        :param color: RGB value of the line
        """
        start = (self.left_bound, pixel)
        end = (self.right_bound, pixel)
        pygame.draw.line(screen, color, start, end, 2)


    def yard_to_pixel(self, yard: int, offset=10):
        """
        converts the given yard on the field to its coordinate

        :param yard: yard on field to convert
        :param offset: yards added to given yards, defaults 10 to offset space used by the end zone
        :return: y coordinate
        """
        return (yard + offset) * (self.height / 120)
