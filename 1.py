import pygame
import random
import sys
from enum import Enum


# ====================== КОНСТАНТЫ И НАСТРОЙКИ ======================
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


# ====================== ГРАФИКА И АССЕТЫ ======================
class PixelArt:
    @staticmethod
    def draw_cat(surface, x, y):
        # Тело кота (16x16)
        pygame.draw.rect(surface, (255, 165, 0), (x, y, 16, 16))
        # Глаза
        pygame.draw.rect(surface, Colors.BLACK, (x + 4, y + 4, 2, 2))
        pygame.draw.rect(surface, Colors.BLACK, (x + 10, y + 4, 2, 2))
        # Уши
        pygame.draw.polygon(surface, (255, 165, 0), [(x, y), (x + 4, y - 4), (x + 8, y)])
        pygame.draw.polygon(surface, (255, 165, 0), [(x + 8, y), (x + 12, y - 4), (x + 16, y)])

    @staticmethod
    def draw_car(surface, x, y, color):
        # Кузов (24x12)
        pygame.draw.rect(surface, color, (x, y + 2, 24, 12))
        # Окна
        pygame.draw.rect(surface, (200, 200, 255), (x + 2, y + 4, 8, 4))
        pygame.draw.rect(surface, (200, 200, 255), (x + 14, y + 4, 8, 4))
        # Колёса
        pygame.draw.rect(surface, Colors.BLACK, (x + 4, y + 12, 4, 4))
        pygame.draw.rect(surface, Colors.BLACK, (x + 16, y + 12, 4, 4))

    @staticmethod
    def draw_tree(surface, x, y):
        # Ствол
        pygame.draw.rect(surface, (101, 67, 33), (x + 12, y + 16, 8, 16))
        # Крона
        pygame.draw.circle(surface, (0, 80, 0), (x + 16, y + 8), 12)

    @staticmethod
    def draw_coin(surface, x, y):
        pygame.draw.circle(surface, Colors.GOLD, (x + 4, y + 4), 4)
        pygame.draw.rect(surface, (200, 150, 0), (x + 2, y + 3, 4, 2))

    @staticmethod
    def draw_road(surface, y_offset):
        # Основная дорожка
        pygame.draw.rect(surface, Colors.SIDEWALK,
                         (0, y_offset, GameSettings.SCREEN_WIDTH, GameSettings.TILE_SIZE))

        # Разметка
        for x in range(0, GameSettings.SCREEN_WIDTH, 40):
            pygame.draw.rect(surface, Colors.WHITE,
                             (x, y_offset + GameSettings.TILE_SIZE // 2 - 1, 20, 2))


# ====================== ИГРОВЫЕ ОБЪЕКТЫ ======================
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
        elif obj_type == ObjectType.COIN:
            self.width = 8
            self.height = 8

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        if self.type == ObjectType.CAR:
            PixelArt.draw_car(surface, self.x, self.y, self.color)
        elif self.type == ObjectType.TREE:
            PixelArt.draw_tree(surface, self.x, self.y)
        elif self.type == ObjectType.COIN:
            PixelArt.draw_coin(surface, self.x, self.y)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ====================== ИГРОВАЯ ЛОГИКА ======================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
        pygame.display.set_caption("Pixel Cat Road Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16)

        self.reset_game()

    def reset_game(self):
        self.player_x = GameSettings.SCREEN_WIDTH // 2
        self.player_y = GameSettings.SCREEN_HEIGHT - 100
        self.road_offset = 0
        self.score = 0
        self.level = 1
        self.obstacles = []
        self.coins = []
        self.crossroads = []
        self.game_active = True
        self.last_obstacle_time = 0
        self.last_coin_time = 0
        self.last_crossroad_time = 0

    def generate_environment(self):
        current_time = pygame.time.get_ticks()

        # Генерация препятствий
        if current_time - self.last_obstacle_time > random.randint(500, 1500):
            if random.random() < 0.7:  # 70% chance for car
                lane = random.choice([100, GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_WIDTH - 124])
                self.obstacles.append(
                    GameObject(lane, -50, ObjectType.CAR, random.randint(3, 6))
                )
            else:  # 30% chance for tree
                self.obstacles.append(
                    GameObject(random.randint(50, GameSettings.SCREEN_WIDTH - 82), -50,
                               ObjectType.TREE, random.randint(1, 3))
                )
            self.last_obstacle_time = current_time

        # Генерация монеток
        if current_time - self.last_coin_time > random.randint(300, 800):
            self.coins.append(
                GameObject(random.randint(50, GameSettings.SCREEN_WIDTH - 58), -10,
                           ObjectType.COIN, random.randint(2, 4))
            )
            self.last_coin_time = current_time

        # Генерация перекрёстков
        if current_time - self.last_crossroad_time > random.randint(5000, 10000):
            self.crossroads.append({
                "y": -GameSettings.TILE_SIZE,
                "active": True,
                "cars": []
            })
            # Добавляем машинки на перекрёсток
            for _ in range(random.randint(2, 4)):
                direction = random.choice(["left", "right"])
                if direction == "left":
                    self.crossroads[-1]["cars"].append(
                        GameObject(GameSettings.SCREEN_WIDTH,
                                   random.randint(-100, -50),
                                   ObjectType.CAR, random.randint(4, 7))
                    )
                else:
                    self.crossroads[-1]["cars"].append(
                        GameObject(-24,
                                   random.randint(-100, -50),
                                   ObjectType.CAR, random.randint(4, 7))
                    )
            self.last_crossroad_time = current_time

    def update_objects(self):
        # Обновление позиций объектов
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.y > GameSettings.SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)

        for coin in self.coins[:]:
            coin.update()
            if coin.y > GameSettings.SCREEN_HEIGHT:
                self.coins.remove(coin)

        for crossroad in self.crossroads[:]:
            crossroad["y"] += GameSettings.SCROLL_SPEED
            if crossroad["y"] > GameSettings.SCREEN_HEIGHT + GameSettings.TILE_SIZE:
                self.crossroads.remove(crossroad)
            else:
                for car in crossroad["cars"]:
                    if car.x < -50 or car.x > GameSettings.SCREEN_WIDTH + 50:
                        crossroad["cars"].remove(car)
                    else:
                        car.update()

    def check_collisions(self):
        player_rect = pygame.Rect(self.player_x, self.player_y, 16, 16)

        # Проверка столкновений с препятствиями
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                self.game_active = False

        # Проверка столкновений с машинами на перекрёстках
        for crossroad in self.crossroads:
            if abs(crossroad["y"] - self.player_y) < 32:
                for car in crossroad["cars"]:
                    if player_rect.colliderect(car.get_rect()):
                        self.game_active = False

        # Проверка сбора монеток
        for coin in self.coins[:]:
            if player_rect.colliderect(coin.get_rect()):
                self.coins.remove(coin)
                self.score += 1

                # Увеличение уровня каждые 10 монет
                if self.score % 10 == 0:
                    self.level += 1

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 20:
            self.player_x -= GameSettings.PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.player_x < GameSettings.SCREEN_WIDTH - 36:
            self.player_x += GameSettings.PLAYER_SPEED
        if keys[pygame.K_UP] and self.player_y > GameSettings.SCREEN_HEIGHT // 2:
            self.player_y -= GameSettings.PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.player_y < GameSettings.SCREEN_HEIGHT - 20:
            self.player_y += GameSettings.PLAYER_SPEED

    def draw(self):
        # Отрисовка фона
        self.screen.fill(Colors.GRASS_GREEN)

        # Отрисовка бесконечной дорожки
        for y in range(-GameSettings.TILE_SIZE, GameSettings.SCREEN_HEIGHT, GameSettings.TILE_SIZE):
            PixelArt.draw_road(self.screen, (y + self.road_offset) % GameSettings.SCREEN_HEIGHT)

        # Отрисовка перекрёстков
        for crossroad in self.crossroads:
            pygame.draw.rect(self.screen, Colors.ROAD_GRAY,
                             (0, crossroad["y"], GameSettings.SCREEN_WIDTH, GameSettings.TILE_SIZE))

            # Отрисовка машин на перекрёстке
            for car in crossroad["cars"]:
                car.draw(self.screen)

        # Отрисовка объектов
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)

        # Отрисовка игрока
        PixelArt.draw_cat(self.screen, self.player_x, self.player_y)

        # Отрисовка UI
        score_text = self.font.render(f"Score: {self.score}", True, Colors.WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, Colors.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 30))

        # Отрисовка Game Over
        if not self.game_active:
            game_over_text = pygame.font.SysFont("Arial", 32).render(
                "Game Over! Press R to restart", True, Colors.RED)
            self.screen.blit(game_over_text,
                             (GameSettings.SCREEN_WIDTH // 2 - 180, GameSettings.SCREEN_HEIGHT // 2))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and not self.game_active:
                        self.reset_game()

            if self.game_active:
                self.road_offset = (self.road_offset + GameSettings.SCROLL_SPEED) % GameSettings.TILE_SIZE
                self.generate_environment()
                self.update_objects()
                self.check_collisions()
                self.handle_input()

            self.draw()
            pygame.display.flip()
            self.clock.tick(GameSettings.FPS)


# ====================== ЗАПУСК ИГРЫ ======================
if __name__ == "__main__":
    game = Game()
    game.run()