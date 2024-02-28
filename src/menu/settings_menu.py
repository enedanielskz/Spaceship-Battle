import pygame
import sys
from pathlib import Path

from config import *
from .game_settings_menu import GameSettingsMenu
from .sound_settings_menu import SoundSettingsMenu
from .players_settings_menu import PlayersSettingsMenu
from gui import *


class SettingsMenu:
    def __init__(self):
        self.window = pygame.display.get_surface()

        self.clock = pygame.time.Clock()
        self.current_fps = 0

        self.active = True

        self.game_settings_menu = GameSettingsMenu()
        self.sound_settings_menu = SoundSettingsMenu()
        self.players_settings_menu = PlayersSettingsMenu()

        self.background = pygame.transform.scale(pygame.image.load(Path("assets/sprites/space/space_menu.png")),
                                                 (self.window.get_width(), self.window.get_height())).convert()

        # Title
        self.title = "Settings"
        self.title_font = pygame.font.SysFont("arialblack", 50)
        self.title_text = self.title_font.render(self.title, True, BLACK)
        self.title_x = (self.window.get_width() - self.title_text.get_width()) // 2
        self.title_y = (self.window.get_height() - 390) // 2

        # Button properties
        self.button_width = 140
        self.button_height = 40
        self.button_x = (self.window.get_width() - self.button_width) // 2
        self.button_y = self.title_y + self.title_text.get_height() + 50
        self.button_y_spacing = self.button_height + 20

        # Create the buttons
        self.button_game = Button(text="Game",
                                  x=self.button_x,
                                  y=self.button_y,
                                  width=self.button_width,
                                  height=self.button_height,
                                  command=self.open_game_settings_menu)

        self.button_sound = Button(text="Sound",
                                   x=self.button_x,
                                   y=self.button_game.bottom_rect.y + self.button_y_spacing,
                                   width=self.button_width,
                                   height=self.button_height,
                                   command=self.open_sound_settings_menu)

        self.button_players = Button(text="Players",
                                     x=self.button_x,
                                     y=self.button_sound.bottom_rect.y + self.button_y_spacing,
                                     width=self.button_width,
                                     height=self.button_height,
                                     command=self.open_players_settings_menu)

        self.button_back = Button(text="Back",
                                  x=self.button_x,
                                  y=self.button_players.bottom_rect.y + self.button_y_spacing,
                                  width=self.button_width,
                                  height=self.button_height,
                                  command=self.back)

    def open(self):
        self.active = True
        while self.active:
            self.clock.tick(config.getint("WINDOW_PROPERTIES", "fps"))
            self.current_fps = int(self.clock.get_fps())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.update()
            self.draw()

    def update(self):
        self.button_game.update()
        self.button_sound.update()
        self.button_players.update()
        self.button_back.update()

    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.title_text, (self.title_x, self.title_y))
        self.button_game.draw()
        self.button_sound.draw()
        self.button_players.draw()
        self.button_back.draw()

        if config.getboolean("WINDOW_PROPERTIES", "show_fps"):
            draw_fps(self.current_fps)

        pygame.display.update()

    def update_sound_volume(self):
        self.button_game.update_sound_volume()
        self.button_sound.update_sound_volume()
        self.button_players.update_sound_volume()
        self.button_back.update_sound_volume()

    def open_game_settings_menu(self):
        self.game_settings_menu.open()

    def open_sound_settings_menu(self):
        self.sound_settings_menu.open()

        self.update_sound_volume()
        self.game_settings_menu.update_sound_volume()
        self.players_settings_menu.update_sound_volume()

    def open_players_settings_menu(self):
        self.players_settings_menu.open()

    def back(self):
        self.active = False

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
