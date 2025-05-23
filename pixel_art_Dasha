import pygame
from design import Colors, GameSettings

class PixelArt:
    @staticmethod
    def draw_shadow(surface, x, y, width, height):
        shadow = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 100), shadow.get_rect())
        surface.blit(shadow, (x + 5, y + height - 5))  # немного вниз и вправо

    @staticmethod
    def draw_cat(surface, x, y):
        PixelArt.draw_shadow(surface, x, y + 12, 16, 6)
        pygame.draw.rect(surface, (255, 165, 0), (x, y, 16, 16))
        pygame.draw.rect(surface, Colors.BLACK, (x + 4, y + 4, 2, 2))
        pygame.draw.rect(surface, Colors.BLACK, (x + 10, y + 4, 2, 2))
        pygame.draw.polygon(surface, (255, 165, 0), [(x, y), (x + 4, y - 4), (x + 8, y)])
        pygame.draw.polygon(surface, (255, 165, 0), [(x + 8, y), (x + 12, y - 4), (x + 16, y)])

    @staticmethod
    def draw_car(surface, x, y, color):
        PixelArt.draw_shadow(surface, x, y + 14, 24, 6)
        pygame.draw.rect(surface, color, (x, y + 2, 24, 12))
        pygame.draw.rect(surface, (200, 200, 255), (x + 2, y + 4, 8, 4))
        pygame.draw.rect(surface, (200, 200, 255), (x + 14, y + 4, 8, 4))
        pygame.draw.rect(surface, Colors.BLACK, (x + 4, y + 12, 4, 4))
        pygame.draw.rect(surface, Colors.BLACK, (x + 16, y + 12, 4, 4))

    @staticmethod
    def draw_tree(surface, x, y):
        PixelArt.draw_shadow(surface, x + 10, y + 62, 20, 8)
        # Ствол
        pygame.draw.rect(surface, (101, 67, 33), (x + 12, y + 16, 8, 16))
        # Крона (с легким градиентом — сверху светлее)
        pygame.draw.circle(surface, (0, 120, 0), (x + 16, y + 6), 12)
        pygame.draw.circle(surface, (0, 80, 0), (x + 16, y + 8), 12)

    @staticmethod
    def draw_house(surface, x, y):
        PixelArt.draw_shadow(surface, x + 10, y + 55, 40, 10)
        # Стены
        pygame.draw.rect(surface, (220, 180, 140), (x, y, 40, 30))
        # Крыша с бликами
        pygame.draw.polygon(surface, (150, 75, 50),
                           [(x, y), (x + 20, y - 15), (x + 40, y)])
        pygame.draw.polygon(surface, (170, 90, 60),
                           [(x + 10, y - 12), (x + 20, y - 15), (x + 30, y - 12)])
        # Дверь и окна с бликами
        pygame.draw.rect(surface, (100, 50, 0), (x + 15, y + 15, 10, 15))
        pygame.draw.rect(surface, (210, 210, 255), (x + 5, y + 5, 8, 8))
        pygame.draw.rect(surface, (230, 230, 255), (x + 6, y + 6, 6, 6))
        pygame.draw.rect(surface, (210, 210, 255), (x + 27, y + 5, 8, 8))
        pygame.draw.rect(surface, (230, 230, 255), (x + 28, y + 6, 6, 6))

    @staticmethod
    def draw_coin(surface, x, y):
        PixelArt.draw_shadow(surface, x + 2, y + 10, 12, 4)
        pygame.draw.circle(surface, Colors.GOLD, (x + 4, y + 4), 4)
        pygame.draw.rect(surface, (200, 150, 0), (x + 2, y + 3, 4, 2))
