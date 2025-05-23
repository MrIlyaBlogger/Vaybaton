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
        self.width = 32
        self.height = 32

        if obj_type == ObjectType.CAR:
            self.width = 24
            self.height = 12
            self.color = random.choice(Colors.CAR_COLORS)
        elif obj_type == ObjectType.TREE:
            self.width = 32
            self.height = 32
        elif obj_type == ObjectType.HOUSE:
            self.width = 40
            self.height = 40
        elif obj_type == ObjectType.COIN:
            self.width = 8
            self.height = 8

    def update(self):
        if self.speed > 0:
            self.y += self.speed

    def draw(self, surface):
        if self.type == ObjectType.CAR:
            PixelArt.draw_car(surface, self.x, self.y, self.color)
        elif self.type == ObjectType.TREE:
            PixelArt.draw_tree(surface, self.x, self.y)
        elif self.type == ObjectType.HOUSE:
            PixelArt.draw_house(surface, self.x, self.y)
        elif self.type == ObjectType.COIN:
            PixelArt.draw_coin(surface, self.x, self.y)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)