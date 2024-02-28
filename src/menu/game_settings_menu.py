import pygame
import sys
import time
from pathlib import Path

from config import *
from gui import *


class GameSettingsMenu:
    def __init__(self):
        self.window = pygame.display.get_surface()

        self.clock = pygame.time.Clock()
        self.current_fps = 0

        self.active = True

        self.background = pygame.transform.scale(pygame.image.load(Path("assets/sprites/space/space_menu.png")),
                                                 (self.window.get_width(), self.window.get_height())).convert()

        # Title
        self.title = "Game"
        self.title_font = pygame.font.SysFont("arialblack", 50)
        self.title_text = self.title_font.render(self.title, True, BLACK)
        self.title_x = (self.window.get_width() - self.title_text.get_width()) // 2
        self.title_y = (self.window.get_height() - 415) // 2

        # Slider properties
        self.slider_width = 180
        self.slider_x = (self.window.get_width() - self.slider_width) // 2
        self.slider_y = self.title_y + self.title_text.get_height() + 50

        # Create the slider
        self.slider_fps = Slider(text="Max FPS: ",
                                 current_value=config.getint("WINDOW_PROPERTIES", "fps"),
                                 min_value=60,
                                 max_value=240,
                                 x=self.slider_x,
                                 y=self.slider_y,
                                 width=self.slider_width)

        # Checkbox properties
        self.checkbox_x = self.slider_x + 35
        self.checkbox_spacing = 30
        self.checkbox_y = self.slider_y + self.checkbox_spacing

        # Create the checkboxes
        self.checkbox_show_fps = Checkbox(text="Show FPS:",
                                          text_distance=14,
                                          checked=config.getboolean("WINDOW_PROPERTIES", "show_fps"),
                                          x=self.checkbox_x,
                                          y=self.checkbox_y)

        self.checkbox_fullscreen = Checkbox(text="Fullscreen: ",
                                            text_distance=5,
                                            checked=config.getboolean("WINDOW_PROPERTIES", "fullscreen"),
                                            x=self.checkbox_x,
                                            y=self.checkbox_show_fps.rect.y + self.checkbox_spacing)

        # Key changer properties
        self.key_changer_x = self.slider_x - 20
        self.key_changer_y = self.checkbox_fullscreen.rect.y + self.checkbox_spacing + 10

        # Create the key changer
        self.key_changer_restart = KeyChanger(text="Restart: ",
                                              text_distance=5,
                                              current_key=config.get("OTHER_KEYS", "restart"),
                                              x=self.key_changer_x,
                                              y=self.key_changer_y)

        # Button properties
        self.button_width = 140
        self.button_height = 40
        self.button_x = (self.window.get_width() - self.button_width) // 2
        self.button_y_spacing = self.button_height + 20
        self.button_y = self.key_changer_y + self.button_y_spacing

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
        self.button_save.update()
        self.button_back.update()

        self.slider_fps.update(dt)

        self.checkbox_show_fps.update(dt)
        self.checkbox_fullscreen.update(dt)

        self.key_changer_restart.update()

    def draw(self):
        self.window.blit(self.background, (0, 0))

        self.window.blit(self.title_text, (self.title_x, self.title_y))

        self.button_save.draw()
        self.button_back.draw()

        self.slider_fps.draw()

        self.checkbox_show_fps.draw()
        self.checkbox_fullscreen.draw()

        self.key_changer_restart.draw()

        if config.getboolean("WINDOW_PROPERTIES", "show_fps"):
            draw_fps(self.current_fps)

        pygame.display.update()

    def update_sound_volume(self):
        self.button_save.update_sound_volume()
        self.button_back.update_sound_volume()

    def save(self):
        config.set("WINDOW_PROPERTIES", "fps", str(self.slider_fps.current_value))

        config.set("WINDOW_PROPERTIES", "show_fps", str(self.checkbox_show_fps.checked))
        config.set("WINDOW_PROPERTIES", "fullscreen", str(self.checkbox_fullscreen.checked))

        if not self.key_changer_restart.active:
            config.set("OTHER_KEYS", "restart", self.key_changer_restart.current_key)

        save_config()

    def back(self):
        self.active = False

        self.checkbox_fullscreen.set_checked(config.getboolean("WINDOW_PROPERTIES", "fullscreen"))
        self.checkbox_show_fps.set_checked(config.getboolean("WINDOW_PROPERTIES", "show_fps"))

        self.slider_fps.set_current_value(config.getint("WINDOW_PROPERTIES", "fps"))

        self.key_changer_restart.set_key(config.get("OTHER_KEYS", "restart"))

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
