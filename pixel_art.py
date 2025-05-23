import pygame
from design import Colors, GameSettings


class PixelArt:
    @staticmethod
    def draw_cat(surface, x, y):
        pygame.draw.rect(surface, (255, 165, 0), (x, y, 16, 16))
        pygame.draw.rect(surface, Colors.BLACK, (x + 4, y + 4, 2, 2))
        pygame.draw.rect(surface, Colors.BLACK, (x + 10, y + 4, 2, 2))
        pygame.draw.polygon(surface, (255, 165, 0), [(x, y), (x + 4, y - 4), (x + 8, y)])
        pygame.draw.polygon(surface, (255, 165, 0), [(x + 8, y), (x + 12, y - 4), (x + 16, y)])

    @staticmethod
    def draw_car(surface, x, y, color):
        pygame.draw.rect(surface, color, (x, y + 2, 24, 12))
        pygame.draw.rect(surface, (200, 200, 255), (x + 2, y + 4, 8, 4))
        pygame.draw.rect(surface, (200, 200, 255), (x + 14, y + 4, 8, 4))
        pygame.draw.rect(surface, Colors.BLACK, (x + 4, y + 12, 4, 4))
        pygame.draw.rect(surface, Colors.BLACK, (x + 16, y + 12, 4, 4))

    @staticmethod
    def draw_tree(surface, x, y):
        pygame.draw.rect(surface, (101, 67, 33), (x + 12, y + 16, 8, 16))
        pygame.draw.circle(surface, (0, 80, 0), (x + 16, y + 8), 12)  # Исправлено здесь

    @staticmethod
    def draw_house(surface, x, y):
        pygame.draw.rect(surface, (200, 150, 100), (x, y, 40, 30))
        pygame.draw.polygon(surface, (150, 75, 50),
                           [(x, y), (x + 20, y - 15), (x + 40, y)])
        pygame.draw.rect(surface, (100, 50, 0), (x + 15, y + 15, 10, 15))
        pygame.draw.rect(surface, (200, 200, 255), (x + 5, y + 5, 8, 8))
        pygame.draw.rect(surface, (200, 200, 255), (x + 27, y + 5, 8, 8))

    @staticmethod
    def draw_coin(surface, x, y):
        pygame.draw.circle(surface, Colors.GOLD, (x + 4, y + 4), 4)  # Исправлено здесь
        pygame.draw.rect(surface, (200, 150, 0), (x + 2, y + 3, 4, 2))