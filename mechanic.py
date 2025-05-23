import random
import sys
import pygame
from design import GameSettings, Colors, ObjectType
from game_objects import GameObject
from pixel_art import PixelArt


class Game:
    def __init__(self):
        pygame.init()
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

        # Obstacle generation
        if current_time - self.last_obstacle_time > random.randint(500, 1500):
            if random.random() < 0.7:  # 70% chance for car
                lane = random.choice([100, GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_WIDTH - 124])
                self.obstacles.append(
                    GameObject(lane, -50, ObjectType.CAR, random.randint(3, 6)))
            else:  # 30% chance for tree
                self.obstacles.append(
                    GameObject(random.randint(50, GameSettings.SCREEN_WIDTH - 82), -50,
                              ObjectType.TREE, random.randint(1, 3)))
            self.last_obstacle_time = current_time

        # Coin generation
        if current_time - self.last_coin_time > random.randint(300, 800):
            self.coins.append(
                GameObject(random.randint(50, GameSettings.SCREEN_WIDTH - 58), -10,
                           ObjectType.COIN, random.randint(2, 4)))
            self.last_coin_time = current_time

        # Crossroad generation
        if current_time - self.last_crossroad_time > random.randint(5000, 10000):
            self.crossroads.append({
                "y": -GameSettings.TILE_SIZE,
                "active": True,
                "cars": []
            })
            # Add cars to crossroad
            for _ in range(random.randint(2, 4)):
                direction = random.choice(["left", "right"])
                if direction == "left":
                    self.crossroads[-1]["cars"].append(
                        GameObject(GameSettings.SCREEN_WIDTH,
                                  random.randint(-100, -50),
                                  ObjectType.CAR, random.randint(4, 7)))
                else:
                    self.crossroads[-1]["cars"].append(
                        GameObject(-24,
                                  random.randint(-100, -50),
                                  ObjectType.CAR, random.randint(4, 7)))
            self.last_crossroad_time = current_time

    def update_objects(self):
        # Update object positions
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

        # Check collisions with obstacles
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                self.game_active = False

        # Check collisions with crossroad cars
        for crossroad in self.crossroads:
            if abs(crossroad["y"] - self.player_y) < 32:
                for car in crossroad["cars"]:
                    if player_rect.colliderect(car.get_rect()):
                        self.game_active = False

        # Check coin collection
        for coin in self.coins[:]:
            if player_rect.colliderect(coin.get_rect()):
                self.coins.remove(coin)
                self.score += 1

                # Level up every 10 coins
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
        # Draw background
        self.screen.fill(Colors.GRASS_GREEN)

        # Draw infinite road
        for y in range(-GameSettings.TILE_SIZE, GameSettings.SCREEN_HEIGHT, GameSettings.TILE_SIZE):
            PixelArt.draw_road(self.screen, (y + self.road_offset) % GameSettings.SCREEN_HEIGHT)

        # Draw crossroads
        for crossroad in self.crossroads:
            pygame.draw.rect(self.screen, Colors.ROAD_GRAY,
                             (0, crossroad["y"], GameSettings.SCREEN_WIDTH, GameSettings.TILE_SIZE))

            # Draw cars on crossroad
            for car in crossroad["cars"]:
                car.draw(self.screen)

        # Draw objects
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)

        # Draw player
        PixelArt.draw_cat(self.screen, self.player_x, self.player_y)

        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, Colors.WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, Colors.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 30))

        # Draw Game Over
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


if __name__ == "__main__":
    game = Game()
    game.run()