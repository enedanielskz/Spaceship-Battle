import pygame
import sys
import time
from pathlib import Path

from config import *
from menu import Menu
from gui import draw_fps, Stats
from entities import *


class Game:
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.fullscreen = config.getboolean("WINDOW_PROPERTIES", "fullscreen")
        if self.fullscreen:
            self.window_width = display_info.current_w
            self.window_height = display_info.current_h
        else:
            self.window_width = config.getint("WINDOW_PROPERTIES", "width")
            self.window_height = config.getint("WINDOW_PROPERTIES", "height")
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))
        if self.fullscreen:
            pygame.display.toggle_fullscreen()
        pygame.display.set_caption("Spaceship Battle")

        self.icon = pygame.image.load(
            Path("assets/sprites/spaceship/spaceship.png")).convert_alpha()
        pygame.display.set_icon(self.icon)

        self.background = pygame.transform.scale(pygame.image.load("assets/sprites/space/space.png"),
                                                 (self.window_width, self.window_height - Stats.height)).convert()

        self.clock = pygame.time.Clock()
        self.current_fps = 0

        self.game_over_text = ""
        self.game_over_text_font = pygame.font.SysFont("Arial", 100)
        self.game_over_text_color = BLACK

        self.menu = Menu()
        self.menu.open()

        self.stats = Stats()
        self.player1 = Player()
        self.player2 = Player(flip=True)
        self.player1_lasers = Player1Lasers()
        self.player2_lasers = Player2Lasers()
        self.space_laser = SpaceLaser()
        self.power_up = PowerUp()
        self.collisions = Collisions()

    def run(self):
        fps = config.getint("WINDOW_PROPERTIES", "fps")
        key_restart = get_key(config.get("OTHER_KEYS", "restart"))

        previous_time = time.perf_counter()
        while True:
            self.clock.tick(fps)
            self.current_fps = int(self.clock.get_fps())
            dt = time.perf_counter() - previous_time
            previous_time = time.perf_counter()

            if dt > 0.1:
                dt = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == key_restart:
                        self.restart()
                    if event.key == self.player1.key_fire and self.player1_lasers.available_lasers > 0:
                        self.player1_lasers.spawn_laser(self.player1.rect)
                    if event.key == self.player2.key_fire and self.player2_lasers.available_lasers > 0:
                        self.player2_lasers.spawn_laser(self.player2.rect)

            self.update(dt)
            self.draw()

            if self.game_is_over():
                self.game_over()
                self.restart()

    def update(self, dt):
        self.player1.update(dt)
        self.player2.update(dt)
        self.player1_lasers.update(dt)
        self.player2_lasers.update(dt)
        self.space_laser.update(dt)
        self.power_up.update(dt)
        self.collisions.update(self.player1, self.player2, self.player1_lasers, self.player2_lasers,
                               self.space_laser.rect, self.power_up)

    def game_is_over(self):
        if self.player1.health <= 0 and self.player2.health <= 0:
            self.game_over_text = "TIE!"
        elif self.player1.health <= 0:
            self.game_over_text = "PLAYER2 WON!"
        elif self.player2.health <= 0:
            self.game_over_text = "PLAYER1 WON!"

        if self.game_over_text != "":
            return True
        else:
            return False

    def game_over(self):
        # Render the game over text
        game_over_text = self.game_over_text_font.render(
            self.game_over_text, True, self.game_over_text_color)

        # Draw the game over text
        self.window.blit(game_over_text,                                             # text
                         ((self.window_width - game_over_text.get_width()) // 2,     # x
                          (self.window_height - game_over_text.get_height()) // 2))  # y

        pygame.display.update()
        pygame.time.delay(5000)

    def draw(self):
        self.window.blit(self.background, (0, Stats.height))
        self.power_up.draw()
        self.player1.draw()
        self.player2.draw()
        self.player1_lasers.draw()
        self.player2_lasers.draw()
        self.space_laser.draw()
        self.stats.draw(self.player1.health, self.player2.health, self.player1_lasers.available_lasers,
                        self.player2_lasers.available_lasers, round(self.power_up.cooldown-self.power_up.current_time))

        if config.getboolean("WINDOW_PROPERTIES", "show_fps"):
            draw_fps(self.current_fps)

        pygame.display.update()

    def restart(self):
        self.menu.open()

        self.player1 = Player()
        self.player2 = Player(flip=True)
        self.player1_lasers = Player1Lasers()
        self.player2_lasers = Player2Lasers()
        self.power_up = PowerUp()
        self.space_laser = SpaceLaser()
        self.game_over_text = ""

        self.run()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
