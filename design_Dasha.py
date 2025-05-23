import pygame
from enum import Enum
import random

class GameSettings:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    # Дорога и полосы
    ROAD_X = 200                 # отступ слева (пляж)
    ROAD_WIDTH = 400             # ширина дороги
    LANES = 3
    LANE_WIDTH = ROAD_WIDTH / LANES

    BEACH_WIDTH = ROAD_X         # пляж слева
    WATER_WIDTH = SCREEN_WIDTH - (ROAD_X + ROAD_WIDTH)  # вода справа

    PLAYER_SPEED = 5
    BASE_SCROLL_SPEED = 3        # базовая скорость прокрутки
    SPEED_INCREASE_FACTOR = 0.001 # +0.1% на каждую монету

class Colors:
    SKY_BLUE = (135, 206, 235)
    BEACH_SAND = (240, 230, 140)
    WATER_BLUE = (0, 180, 255)
    ROAD_GRAY = (50, 50, 50)
    ROAD_LINE = (255, 255, 255)
    BORDER_YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GOLD = (255, 215, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    CAR_COLORS = [(200, 0, 0), (0, 0, 200), (0, 200, 0)]
    HOUSE_WHITE = (255, 255, 255)
    HOUSE_ROOF_BLUE = (0, 0, 255)
    PALM_TRUNK = (139, 69, 19)
    PALM_LEAVES = (0, 150, 0)
    SHIP_COLOR = (50, 50, 150)
    FISH_COLOR = (255, 100, 100)

class ObjectType(Enum):
    CAR = 1
    TREE = 2
    HOUSE = 3
    COIN = 4
    PALM = 5
    SHIP = 6
    FISH = 7
