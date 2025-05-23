import pygame
import asyncio
import random
from design import GameSettings, Colors, ObjectType
from game_objects import GameObject
from pixel_art import PixelArt


class Game:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.font = None
        self.reset_game()

    async def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
        pygame.display.set_caption("Pixel Cat Road Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16)

    def reset_game(self):
        self.player_x = GameSettings.SCREEN_WIDTH // 2
        self.player_y = GameSettings.SCREEN_HEIGHT - 100
        self.score = 0
        self.level = 1
        self.obstacles = []
        self.coins = []
        self.crossroads = []
        self.game_active = True
        self.last_obstacle_time = 0
        self.last_coin_time = 0
        self.last_crossroad_time = 0
        self.level_length = 3000  # Длина уровня в пикселях (можно менять)
        self.camera_offset = 0    # Сколько "пройдено" вверх
        self.level_completed = False
        self.scrolling_stopped = False
        self.start_time = pygame.time.get_ticks()

    def generate_environment(self):
        current_time = pygame.time.get_ticks()
        # Больше препятствий, домов и деревьев
        for _ in range(4):
            if current_time - self.last_obstacle_time > 200:
                obj_type = random.choice([ObjectType.TREE, ObjectType.HOUSE])
                lane = random.choice([100, GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_WIDTH - 100, 200, 300, 400, 500, 600])
                self.obstacles.append(GameObject(lane, -50 - self.camera_offset, obj_type, GameSettings.SCROLL_SPEED))
                self.last_obstacle_time = current_time
        # Больше монет
        for _ in range(3):
            if current_time - self.last_coin_time > random.randint(100, 400):
                self.coins.append(GameObject(
                    random.randint(50, GameSettings.SCREEN_WIDTH - 50),
                    -50 - self.camera_offset, ObjectType.COIN, GameSettings.SCROLL_SPEED
                ))
                self.last_coin_time = current_time
        # Больше дорог с машинами
        for _ in range(3):
            if current_time - self.last_crossroad_time > random.randint(800, 1800):
                crossroad_y = -GameSettings.TILE_SIZE - self.camera_offset
                self.crossroads.append({
                    "y": crossroad_y,
                    "cars": [self.generate_car() for _ in range(random.randint(4, 8))]
                })
                self.last_crossroad_time = current_time

    def generate_car(self):
        direction = random.choice(["left", "right"])
        # Машина появляется на дороге (по y дороги, а не вверху экрана)
        car_y_on_road = GameSettings.TILE_SIZE // 2  # Центр полосы
        if direction == "left":
            car = GameObject(GameSettings.SCREEN_WIDTH, car_y_on_road, ObjectType.CAR, 0)
            car.dir = -1
            car.speed_x = random.randint(4, 7)
        else:
            car = GameObject(-24, car_y_on_road, ObjectType.CAR, 0)
            car.dir = 1
            car.speed_x = random.randint(4, 7)
        return car

    def update_objects(self):
        if self.camera_offset < self.level_length:
            self.camera_offset += GameSettings.SCROLL_SPEED
        for obstacle in self.obstacles[:]:
            obstacle.y += GameSettings.SCROLL_SPEED
            if obstacle.y > GameSettings.SCREEN_HEIGHT + 50:
                self.obstacles.remove(obstacle)
        for coin in self.coins[:]:
            coin.y += GameSettings.SCROLL_SPEED
            if coin.y > GameSettings.SCREEN_HEIGHT + 50:
                self.coins.remove(coin)
        for crossroad in self.crossroads[:]:
            crossroad["y"] += GameSettings.SCROLL_SPEED
            if crossroad["y"] > GameSettings.SCREEN_HEIGHT + GameSettings.TILE_SIZE:
                self.crossroads.remove(crossroad)
            else:
                for car in crossroad["cars"][:]:
                    car.x += car.dir * car.speed_x
                    car.y = crossroad["y"] + GameSettings.TILE_SIZE // 2 - car.height // 2
                    if car.x < -50 or car.x > GameSettings.SCREEN_WIDTH + 50:
                        crossroad["cars"].remove(car)

    def check_collisions(self):
        player_rect = pygame.Rect(self.player_x, self.player_y, 16, 16)
        for crossroad in self.crossroads:
            if abs(crossroad["y"] - self.player_y) < 32:
                for car in crossroad["cars"]:
                    if player_rect.colliderect(car.get_rect()):
                        self.game_active = False
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                self.game_active = False
        for coin in self.coins[:]:
            if player_rect.colliderect(coin.get_rect()):
                self.coins.remove(coin)
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
        # Победа — если прошло 60 секунд
        if self.game_active:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            if elapsed >= 60:
                self.level_completed = True
                self.game_active = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 20:
            self.player_x -= GameSettings.PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.player_x < GameSettings.SCREEN_WIDTH - 36:
            self.player_x += GameSettings.PLAYER_SPEED
        if keys[pygame.K_UP] and self.player_y > 20:
            self.player_y -= GameSettings.PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.player_y < GameSettings.SCREEN_HEIGHT - 20:
            self.player_y += GameSettings.PLAYER_SPEED

    def draw(self):
        if not self.screen:
            return
        self.screen.fill(Colors.GRASS_GREEN)
        for crossroad in self.crossroads:
            pygame.draw.rect(self.screen, Colors.ROAD_GRAY,
                             (0, crossroad["y"], GameSettings.SCREEN_WIDTH, GameSettings.TILE_SIZE))
            for car in crossroad["cars"]:
                car.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        for coin in self.coins:
            coin.draw(self.screen)
        PixelArt.draw_cat(self.screen, self.player_x, self.player_y)
        if self.font:
            score_text = self.font.render(f"Score: {self.score}", True, Colors.WHITE)
            level_text = self.font.render(f"Level: {self.level}", True, Colors.WHITE)
            timer_text = self.font.render(f"Time: {int((pygame.time.get_ticks() - self.start_time) / 1000)}", True, Colors.WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (10, 30))
            self.screen.blit(timer_text, (10, 50))
        if not self.game_active and self.font:
            if self.level_completed:
                win_text = pygame.font.SysFont("Arial", 32).render(
                    "Уровень пройден! Поздравляем!", True, (0, 180, 0))
                self.screen.blit(win_text,
                                 (GameSettings.SCREEN_WIDTH // 2 - 200, GameSettings.SCREEN_HEIGHT // 2))
            else:
                game_over_text = pygame.font.SysFont("Arial", 32).render(
                    "Game Over! Press R to restart", True, Colors.RED)
                self.screen.blit(game_over_text,
                                 (GameSettings.SCREEN_WIDTH // 2 - 180, GameSettings.SCREEN_HEIGHT // 2))
        pygame.display.flip()

    async def run_web(self):
        await self.init_pygame()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not self.game_active:
                    self.reset_game()

            if self.game_active:
                self.generate_environment()
                self.update_objects()
                self.check_collisions()
                self.handle_input()
            self.draw()
            await asyncio.sleep(0)
            self.clock.tick(GameSettings.FPS)