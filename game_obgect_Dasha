import pygame
import random
from design import Colors, ObjectType
from pixel_art import PixelArt

class GameObject:
    def __init__(self, x, y, obj_type, speed=0):
        self.x = x
        self.y = y
        self.type = obj_type
        self.speed = speed
        self.color = None

        # Размеры и цвет для каждого типа
        if obj_type == ObjectType.CAR:
            self.width = 60
            self.height = 30
            self.color = random.choice(Colors.CAR_COLORS)
        elif obj_type == ObjectType.TREE:
            self.width = 40
            self.height = 60
        elif obj_type == ObjectType.HOUSE:
            self.width = 60
            self.height = 60
        elif obj_type == ObjectType.COIN:
            self.width = 20
            self.height = 20
        elif obj_type == ObjectType.PALM:
            self.width = 40
            self.height = 80
        elif obj_type == ObjectType.SHIP:
            self.width = 60
            self.height = 30
        elif obj_type == ObjectType.FISH:
            self.width = 40
            self.height = 20
        else:
            self.width = 32
            self.height = 32

    def update(self):
        # Двигаем по Y с учётом скорости
        self.y += self.speed

    def draw(self, surface):
        if self.type == ObjectType.CAR:
            PixelArt.draw_car(surface, self.x - self.width // 2, self.y - self.height // 2, self.color)
        elif self.type == ObjectType.TREE:
            PixelArt.draw_tree(surface, self.x - self.width // 2, self.y - self.height // 2)
        elif self.type == ObjectType.HOUSE:
            PixelArt.draw_house(surface, self.x - self.width // 2, self.y - self.height // 2)
        elif self.type == ObjectType.COIN:
            PixelArt.draw_coin(surface, self.x - self.width // 2, self.y - self.height // 2)
        elif self.type == ObjectType.PALM:
            PixelArt.draw_palm(surface, self.x - self.width // 2, self.y - self.height // 2)
        elif self.type == ObjectType.SHIP:
            PixelArt.draw_ship(surface, self.x - self.width // 2, self.y - self.height // 2)
        elif self.type == ObjectType.FISH:
            PixelArt.draw_fish(surface, self.x - self.width // 2, self.y - self.height // 2)

    def get_rect(self):
        # Центрируем коллизию по центру объекта
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
