import pygame
import sys
import time
from pathlib import Path

from config import *
from gui import *


class SoundSettingsMenu:
    def __init__(self):
        self.window = pygame.display.get_surface()

        self.clock = pygame.time.Clock()
        self.current_fps = 0

        self.active = True

        self.background = pygame.transform.scale(pygame.image.load(Path("assets/sprites/space/space_menu.png")),
                                                 (self.window.get_width(), self.window.get_height())).convert()

        # Title
        self.title = "Sound"
        self.title_font = pygame.font.SysFont("arialblack", 50)
        self.title_text = self.title_font.render(self.title, True, BLACK)
        self.title_x = (self.window.get_width() - self.title_text.get_width()) // 2
        self.title_y = (self.window.get_height() - 440) // 2

        # Slider properties
        self.slider_width = 140
        self.slider_x = (self.window.get_width() - self.slider_width) // 2
        self.slider_y_spacing = 60
        self.slider_y = self.title_y + self.title_text.get_height() + 50

        # Create the sliders
        self.slider_music = Slider(text="Music: ",
                                   current_value=int(config.getfloat("SOUND", "music") * 100),
                                   min_value=0,
                                   max_value=100,
                                   x=self.slider_x,
                                   y=self.slider_y,
                                   width=self.slider_width)

        self.slider_game = Slider(text="Game: ",
                                  current_value=int(config.getfloat("SOUND", "game") * 100),
                                  min_value=0,
                                  max_value=100,
                                  x=self.slider_x,
                                  y=self.slider_music.empty_rect.y + self.slider_y_spacing,
                                  width=self.slider_width)

        self.slider_menu = Slider(text="Menu: ",
                                  current_value=int(config.getfloat("SOUND", "menu") * 100),
                                  min_value=0,
                                  max_value=100,
                                  x=self.slider_x,
                                  y=self.slider_game.empty_rect.y + self.slider_y_spacing,
                                  width=self.slider_width)

        # Button properties
        self.button_width = 140
        self.button_height = 40
        self.button_x = (self.window.get_width() - self.button_width) // 2
        self.button_y_spacing = self.button_height + 20
        self.button_y = self.slider_menu.empty_rect.y + self.button_y_spacing

        # Create the buttons
        self.button_save = Button(text="Save",
                                  x=self.button_x,
                                  y=self.button_y,
                                  width=self.button_width,
                                  height=self.button_height,
                                  command=self.save)

        self.button_back = Button(text="Back",
                                  x=self.button_x,
                                  y=self.button_save.bottom_rect.y + self.button_y_spacing,
                                  width=self.button_width,
                                  height=self.button_height,
                                  command=self.back)

    def open(self):
        self.active = True

        previous_time = time.perf_counter()
        while self.active:
            self.clock.tick(config.getint("WINDOW_PROPERTIES", "fps"))
            self.current_fps = int(self.clock.get_fps())
            dt = time.perf_counter() - previous_time
            previous_time = time.perf_counter()

            if dt > 0.1:
                dt = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.update(dt)
            self.draw()

    def update(self, dt):
        self.slider_music.update(dt)
        self.slider_game.update(dt)
        self.slider_menu.update(dt)

        self.button_save.update()
        self.button_back.update()

    def draw(self):
        self.window.blit(self.background, (0, 0))

        self.window.blit(self.title_text, (self.title_x, self.title_y))

        self.slider_music.draw()
        self.slider_game.draw()
        self.slider_menu.draw()

        self.button_save.draw()
        self.button_back.draw()

        if config.getboolean("WINDOW_PROPERTIES", "show_fps"):
            draw_fps(self.current_fps)

        pygame.display.update()

    def update_sound_volume(self):
        self.button_save.update_sound_volume()
        self.button_back.update_sound_volume()

    def save(self):
        config.set("SOUND", "music", str(self.slider_music.current_value / 100))
        config.set("SOUND", "game", str(self.slider_game.current_value / 100))
        config.set("SOUND", "menu", str(self.slider_menu.current_value / 100))
        save_config()

        self.update_sound_volume()

    def back(self):
        self.slider_music.set_current_value(int(config.getfloat("SOUND", "music") * 100))
        self.slider_game.set_current_value(int(config.getfloat("SOUND", "game") * 100))
        self.slider_menu.set_current_value(int(config.getfloat("SOUND", "menu") * 100))

        self.active = False

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
