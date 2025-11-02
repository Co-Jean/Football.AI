import pygame
import math

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (24, 150, 0)
SIDELINE_WIDTH = 10
TOTAL_YARDS = 120
YARD_TO_GAIN = 10

class Field:
    def __init__(self, screen):

        screen_size = screen.get_size()
        field_bounds = (screen_size[0] / 4, screen_size[0] * 3 / 4)

        self.left_bound = field_bounds[0]
        self.right_bound = field_bounds[1]

        self.height = screen.get_height()
        self.score_endzone = self.yard_to_pixel(0)
        saftey_endzone = self.yard_to_pixel(100)
        self.max_dist = math.sqrt((field_bounds[1] - field_bounds[0]) ** 2 + (self.score_endzone - saftey_endzone) ** 2)
        self.scrimmage = self.yard_to_pixel(70)

        self.screen = screen

    def draw_field(self):
        """
        Draws the field onto the screen
        """
        pixels_per_yard = self.height / TOTAL_YARDS
        ten_yards = YARD_TO_GAIN * pixels_per_yard
        font = pygame.font.Font(pygame.font.get_default_font(), 25)

        self.screen.fill(GREEN)

        # End Zones
        zone_width = self.right_bound - self.left_bound
        self.draw_rectangle((self.left_bound, 0), ten_yards, zone_width, color=BLUE)
        self.draw_rectangle((self.left_bound, 11 * ten_yards+1), ten_yards, zone_width, color=RED)

        for i in range(10, 100, YARD_TO_GAIN):
            number = pygame.transform.rotate(font.render(f"{-abs(i-50)+50}", True, WHITE), 90)
            self.screen.blit(number, (self.left_bound, (i + 7.5) * pixels_per_yard))

        for i in range(0, 110, YARD_TO_GAIN):
            self.draw_line_from_yard(i)

        # Bounds
        self.draw_rectangle((self.left_bound - SIDELINE_WIDTH, 0), self.height, SIDELINE_WIDTH)
        self.draw_rectangle((self.right_bound, 0), self.height, SIDELINE_WIDTH)


    def draw_line_from_yard(self, yard: int, offset=10, color=WHITE):
        """
        Draws a line horizontally across the field at the given yardage

        :param yard: Yard on field to draw the line across
        :param offset: yards added to given yards, defaults 10 to offset space used by the end zone
        :param color: RGB value of the line
        """
        pixels_per_yard = self.height / TOTAL_YARDS
        start = (self.left_bound, (yard + offset) * pixels_per_yard)
        end = (self.right_bound, (yard + offset) * pixels_per_yard)
        pygame.draw.line(self.screen, color, start, end, 2)


    def draw_line_from_pixel(self, pixel: float, color=WHITE):
        """
        Draws a line horizontally across the field at the given y coordinate/pixel

        :param pixel: y coordinate to draw the line across
        :param color: RGB value of the line
        """
        start = (self.left_bound, pixel)
        end = (self.right_bound, pixel)
        pygame.draw.line(self.screen, color, start, end, 2)


    def draw_rectangle(self, topleft: tuple[float, float], height: float, width: float, color=WHITE):
        surface = pygame.Surface((width, height))
        surface.fill(color)
        self.screen.blit(surface, topleft)


    def yard_to_pixel(self, yard: int, offset=10):
        """
        converts the given yard on the field to its coordinate

        :param yard: yard on field to convert
        :param offset: yards added to given yards, defaults 10 to offset space used by the end zone
        :return: y coordinate
        """
        return (yard + offset) * (self.height / TOTAL_YARDS)
