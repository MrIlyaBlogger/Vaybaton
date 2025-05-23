import pygame
from design import Colors, GameSettings


class PixelArt:
    @staticmethod
    def draw_cat(surface, x, y):
        # Cat body (16x16)
        pygame.draw.rect(surface, (255, 165, 0), (x, y, 16, 16))
        # Eyes
        pygame.draw.rect(surface, Colors.BLACK, (x + 4, y + 4, 2, 2))
        pygame.draw.rect(surface, Colors.BLACK, (x + 10, y + 4, 2, 2))
        # Ears
        pygame.draw.polygon(surface, (255, 165, 0), [(x, y), (x + 4, y - 4), (x + 8, y)])
        pygame.draw.polygon(surface, (255, 165, 0), [(x + 8, y), (x + 12, y - 4), (x + 16, y)])

    @staticmethod
    def draw_car(surface, x, y, color):
        # Body (24x12)
        pygame.draw.rect(surface, color, (x, y + 2, 24, 12))
        # Windows
        pygame.draw.rect(surface, (200, 200, 255), (x + 2, y + 4, 8, 4))
        pygame.draw.rect(surface, (200, 200, 255), (x + 14, y + 4, 8, 4))
        # Wheels
        pygame.draw.rect(surface, Colors.BLACK, (x + 4, y + 12, 4, 4))
        pygame.draw.rect(surface, Colors.BLACK, (x + 16, y + 12, 4, 4))

    @staticmethod
    def draw_tree(surface, x, y):
        # Trunk
        pygame.draw.rect(surface, (101, 67, 33), (x + 12, y + 16, 8, 16))
        # Crown
        pygame.draw.circle(surface, (0, 80, 0), (x + 16, y + 8), 12)

    @staticmethod
    def draw_coin(surface, x, y):
        pygame.draw.circle(surface, Colors.GOLD, (x + 4, y + 4), 4)
        pygame.draw.rect(surface, (200, 150, 0), (x + 2, y + 3, 4, 2))

    @staticmethod
    def draw_road(surface, y_offset):
        # Main road
        pygame.draw.rect(surface, Colors.SIDEWALK,
                         (0, y_offset, GameSettings.SCREEN_WIDTH, GameSettings.TILE_SIZE))

        # Road markings
        for x in range(0, GameSettings.SCREEN_WIDTH, 40):
            pygame.draw.rect(surface, Colors.WHITE,
                             (x, y_offset + GameSettings.TILE_SIZE // 2 - 1, 20, 2))