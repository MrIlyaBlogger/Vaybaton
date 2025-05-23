import pygame
from enum import Enum
import random


class GameSettings:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TILE_SIZE = 64
    FPS = 60
    SCROLL_SPEED = 3
    PLAYER_SPEED = 5


class Colors:
    SKY_BLUE = (135, 206, 235)
    GRASS_GREEN = (100, 200, 100)
    ROAD_GRAY = (50, 50, 50)
    SIDEWALK = (200, 200, 200)
    RED = (255, 0, 0)
    GOLD = (255, 215, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    CAR_COLORS = [(200, 0, 0), (0, 0, 200), (0, 200, 0), (200, 200, 0)]


class ObjectType(Enum):
    CAR = 1
    TREE = 2
    BUSH = 3
    LAMP = 4
    COIN = 5