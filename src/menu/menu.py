import pygame
import sys
from pathlib import Path

from config import *
from .settings_menu import SettingsMenu
from gui import *


class Menu:
    def __init__(self):
        self.window = pygame.display.get_surface()

        self.clock = pygame.time.Clock()
        self.current_fps = 0

        self.active = True

        self.settings_menu = SettingsMenu()

        self.background = pygame.transform.scale(pygame.image.load(Path("assets/sprites/space/space_menu.png")),
                                                 (self.window.get_width(), self.window.get_height())).convert()

        # Title
        self.title = "Spaceship Battle"
        self.title_font = pygame.font.SysFont("arialblack", 50)
        self.title_text = self.title_font.render(self.title, True, BLACK)
        self.title_x = (self.window.get_width() - self.title_text.get_width()) // 2
        self.title_y = (self.window.get_height() - 350) // 2

        # Button properties
        self.button_width = 140
        self.button_height = 40
        self.button_x = (self.window.get_width() - self.button_width) // 2
        self.button_y = self.title_y + self.title_text.get_height() + 50
        self.button_y_spacing = self.button_height + 20

        # Create the buttons
        self.button_play = Button(text="Play",
                                  x=self.button_x,
                                  y=self.button_y,
                                  width=self.button_width,
                                  height=self.button_height,
                                  command=self.play)

        self.button_settings = Button(text="Settings",
                                      x=self.button_x,
                                      y=self.button_play.bottom_rect.y + self.button_y_spacing,
                                      width=self.button_width,
                                      height=self.button_height,
                                      command=self.open_settings)

        self.button_quit = Button(text="Quit",
                                  x=self.button_x,
                                  y=self.button_settings.bottom_rect.y + self.button_y_spacing,
                                  width=self.button_width,
                                  height=self.button_height,
                                  command=self.quit)

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
        self.button_play.update()
        self.button_settings.update()
        self.button_quit.update()

    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.title_text, (self.title_x, self.title_y))
        self.button_play.draw()
        self.button_settings.draw()
        self.button_quit.draw()

        if config.getboolean("WINDOW_PROPERTIES", "show_fps"):
            draw_fps(self.current_fps)

        pygame.display.update()

    def update_sound_volume(self):
        self.button_play.update_sound_volume()
        self.button_settings.update_sound_volume()
        self.button_quit.update_sound_volume()

    def play(self):
        self.active = False

    def open_settings(self):
        self.settings_menu.open()

        self.update_sound_volume()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
