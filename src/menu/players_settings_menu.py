import pygame
import sys
import time
from pathlib import Path

from config import *
from gui import *


class PlayersSettingsMenu:
    def __init__(self):
        self.window = pygame.display.get_surface()

        self.clock = pygame.time.Clock()
        self.current_fps = 0

        self.active = True

        self.background = pygame.transform.scale(pygame.image.load(Path("assets/sprites/space/space_menu.png")),
                                                 (self.window.get_width(), self.window.get_height())).convert()

        # Title
        self.title_font = pygame.font.SysFont("arialblack", 50)
        self.title_text = self.title_font.render("Players", True, BLACK)
        self.title_x = (self.window.get_width() - self.title_text.get_width()) // 2
        self.title_y = (self.window.get_height() - 480) // 2

        # Sub-Titles
        self.sub_title_font = pygame.font.SysFont("arialblack", 35)
        self.sub_title_color = BLACK

        self.stats_text = self.sub_title_font.render("Stats", True, self.sub_title_color)
        self.stats_x = (self.window.get_width() - self.stats_text.get_width()) // 2
        self.stats_y = self.title_y + self.title_text.get_height() + 35

        self.player1_text = self.sub_title_font.render("Player1", True, self.sub_title_color)
        self.player1_x = 50
        self.player1_y = self.title_y + 30

        self.player2_text = self.sub_title_font.render("Player2", True, self.sub_title_color)
        self.player2_x = self.window.get_width() - self.player2_text.get_width() - 50
        self.player2_y = self.title_y + 30

        # Slider properties
        self.slider_width = 140
        self.slider_x = (self.window.get_width() - self.slider_width) // 2
        self.slider_y_spacing = 60
        self.slider_y = self.stats_y + self.stats_text.get_height() + 50

        # Create the sliders
        self.slider_health = Slider(text="Health: ",
                                    current_value=config.getint("PLAYERS_STATS", "health"),
                                    min_value=1,
                                    max_value=100,
                                    x=self.slider_x,
                                    y=self.slider_y,
                                    width=self.slider_width)

        self.slider_lasers = Slider(text="Lasers: ",
                                    current_value=config.getint("PLAYERS_STATS", "lasers"),
                                    min_value=1,
                                    max_value=100,
                                    x=self.slider_x,
                                    y=self.slider_health.empty_rect.y + self.slider_y_spacing,
                                    width=self.slider_width)

        # Button properties
        self.button_width = 140
        self.button_height = 40
        self.button_x = (self.window.get_width() - self.button_width) // 2
        self.button_y_spacing = self.button_height + 20
        self.button_y = self.slider_lasers.empty_rect.y + self.button_y_spacing

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

        # Key changer properties
        self.key_changer_y = self.player1_y + self.player1_text.get_height() + 30
        self.key_changer_spacing = 30
        self.key_changer_player1_x = self.player1_x
        self.key_changer_player2_x = self.window.get_width() - 50 - 196
        self.key_changer_active = False

        # Create the player1 key changers
        self.key_changer_player1_left = KeyChanger(text="Left:",
                                                   text_distance=18,
                                                   current_key=config.get("PLAYER1_CONTROLS", "left"),
                                                   x=self.key_changer_player1_x,
                                                   y=self.key_changer_y)

        self.key_changer_player1_right = KeyChanger(text="Right:",
                                                    text_distance=7,
                                                    current_key=config.get("PLAYER1_CONTROLS", "right"),
                                                    x=self.key_changer_player1_x,
                                                    y=self.key_changer_player1_left.rect.y + self.key_changer_spacing)

        self.key_changer_player1_up = KeyChanger(text="Up:",
                                                 text_distance=28,
                                                 current_key=config.get("PLAYER1_CONTROLS", "up"),
                                                 x=self.key_changer_player1_x,
                                                 y=self.key_changer_player1_right.rect.y + self.key_changer_spacing)

        self.key_changer_player1_down = KeyChanger(text="Down:",
                                                   text_distance=5,
                                                   current_key=config.get("PLAYER1_CONTROLS", "down"),
                                                   x=self.key_changer_player1_x,
                                                   y=self.key_changer_player1_up.rect.y + self.key_changer_spacing)

        self.key_changer_player1_fire = KeyChanger(text="Fire:",
                                                   text_distance=19,
                                                   current_key=config.get("PLAYER1_CONTROLS", "fire"),
                                                   x=self.key_changer_player1_x,
                                                   y=self.key_changer_player1_down.rect.y + self.key_changer_spacing)

        # Create the player2 key changers
        self.key_changer_player2_left = KeyChanger(text="Left:",
                                                   text_distance=18,
                                                   current_key=config.get("PLAYER2_CONTROLS", "left"),
                                                   x=self.key_changer_player2_x,
                                                   y=self.key_changer_y)

        self.key_changer_player2_right = KeyChanger(text="Right:",
                                                    text_distance=7,
                                                    current_key=config.get("PLAYER2_CONTROLS", "right"),
                                                    x=self.key_changer_player2_x,
                                                    y=self.key_changer_player2_left.rect.y + self.key_changer_spacing)

        self.key_changer_player2_up = KeyChanger(text="Up:",
                                                 text_distance=28,
                                                 current_key=config.get("PLAYER2_CONTROLS", "up"),
                                                 x=self.key_changer_player2_x,
                                                 y=self.key_changer_player2_right.rect.y + self.key_changer_spacing)

        self.key_changer_player2_down = KeyChanger(text="Down:",
                                                   text_distance=5,
                                                   current_key=config.get("PLAYER2_CONTROLS", "down"),
                                                   x=self.key_changer_player2_x,
                                                   y=self.key_changer_player2_up.rect.y + self.key_changer_spacing)

        self.key_changer_player2_fire = KeyChanger(text="Fire:",
                                                   text_distance=19,
                                                   current_key=config.get("PLAYER2_CONTROLS", "fire"),
                                                   x=self.key_changer_player2_x,
                                                   y=self.key_changer_player2_down.rect.y + self.key_changer_spacing)

        # Color picker properties
        self.color_picker_y = self.key_changer_player1_fire.rect.y + 40
        self.color_picker_player1_x = self.player1_x
        self.color_picker_player2_x = self.window.get_width() - 50 - 255

        self.color_picker_player1_laser = ColorPicker(text="Color:",
                                                      text_distance=5,
                                                      red=config.getint("PLAYER1_COLOR", "red"),
                                                      green=config.getint("PLAYER1_COLOR", "green"),
                                                      blue=config.getint("PLAYER1_COLOR", "blue"),
                                                      x=self.color_picker_player1_x,
                                                      y=self.color_picker_y)

        self.color_picker_player2_laser = ColorPicker(text="Color:",
                                                      text_distance=5,
                                                      red=config.getint("PLAYER2_COLOR", "red"),
                                                      green=config.getint("PLAYER2_COLOR", "green"),
                                                      blue=config.getint("PLAYER2_COLOR", "blue"),
                                                      x=self.color_picker_player2_x,
                                                      y=self.color_picker_y)

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

            self.key_changer_active = self.key_changer_is_active()

            self.update(dt)
            self.draw()

    def update(self, dt):
        self.slider_health.update(dt)
        self.slider_lasers.update(dt)

        self.button_save.update()
        self.button_back.update()

        self.key_changer_player1_left.update(self.key_changer_active)
        self.key_changer_player1_right.update(self.key_changer_active)
        self.key_changer_player1_up.update(self.key_changer_active)
        self.key_changer_player1_down.update(self.key_changer_active)
        self.key_changer_player1_fire.update(self.key_changer_active)

        self.key_changer_player2_left.update(self.key_changer_active)
        self.key_changer_player2_right.update(self.key_changer_active)
        self.key_changer_player2_up.update(self.key_changer_active)
        self.key_changer_player2_down.update(self.key_changer_active)
        self.key_changer_player2_fire.update(self.key_changer_active)

        self.color_picker_player1_laser.update(dt)
        self.color_picker_player2_laser.update(dt)

    def draw(self):
        self.window.blit(self.background, (0, 0))

        self.window.blit(self.title_text, (self.title_x, self.title_y))
        self.window.blit(self.stats_text, (self.stats_x, self.stats_y))
        self.window.blit(self.player1_text, (self.player1_x, self.player1_y))
        self.window.blit(self.player2_text, (self.player2_x, self.player2_y))

        self.slider_health.draw()
        self.slider_lasers.draw()

        self.button_save.draw()
        self.button_back.draw()

        self.key_changer_player1_left.draw()
        self.key_changer_player1_right.draw()
        self.key_changer_player1_up.draw()
        self.key_changer_player1_down.draw()
        self.key_changer_player1_fire.draw()

        self.key_changer_player2_left.draw()
        self.key_changer_player2_right.draw()
        self.key_changer_player2_up.draw()
        self.key_changer_player2_down.draw()
        self.key_changer_player2_fire.draw()

        self.color_picker_player1_laser.draw()
        self.color_picker_player2_laser.draw()

        if config.getboolean("WINDOW_PROPERTIES", "show_fps"):
            draw_fps(self.current_fps)

        pygame.display.update()

    def update_sound_volume(self):
        self.button_back.update_sound_volume()
        self.button_save.update_sound_volume()

    def key_changer_is_active(self):
        if self.key_changer_player1_left.active or self.key_changer_player1_right.active or \
                self.key_changer_player1_up.active or self.key_changer_player1_down.active or \
                self.key_changer_player1_fire.active or self.key_changer_player2_left.active or \
                self.key_changer_player2_right.active or self.key_changer_player2_up.active or \
                self.key_changer_player2_down.active or self.key_changer_player2_fire.active:
            return True
        else:
            return False

    def save(self):
        config.set("PLAYERS_STATS", "health", str(self.slider_health.current_value))
        config.set("PLAYERS_STATS", "lasers", str(self.slider_lasers.current_value))

        if not self.key_changer_player1_left.active:
            config.set("PLAYER1_CONTROLS", "left", self.key_changer_player1_left.current_key)
        if not self.key_changer_player1_right.active:
            config.set("PLAYER1_CONTROLS", "right", self.key_changer_player1_right.current_key)
        if not self.key_changer_player1_up.active:
            config.set("PLAYER1_CONTROLS", "up", self.key_changer_player1_up.current_key)
        if not self.key_changer_player1_down.active:
            config.set("PLAYER1_CONTROLS", "down", self.key_changer_player1_down.current_key)
        if not self.key_changer_player1_fire.active:
            config.set("PLAYER1_CONTROLS", "fire", self.key_changer_player1_fire.current_key)

        if not self.key_changer_player2_left.active:
            config.set("PLAYER2_CONTROLS", "left", self.key_changer_player2_left.current_key)
        if not self.key_changer_player2_right.active:
            config.set("PLAYER2_CONTROLS", "right", self.key_changer_player2_right.current_key)
        if not self.key_changer_player2_up.active:
            config.set("PLAYER2_CONTROLS", "up", self.key_changer_player2_up.current_key)
        if not self.key_changer_player2_down.active:
            config.set("PLAYER2_CONTROLS", "down", self.key_changer_player2_down.current_key)
        if not self.key_changer_player2_fire.active:
            config.set("PLAYER2_CONTROLS", "fire", self.key_changer_player2_fire.current_key)

        config.set("PLAYER1_COLOR", "red", str(self.color_picker_player1_laser.slider_red.current_value))
        config.set("PLAYER1_COLOR", "green", str(self.color_picker_player1_laser.slider_green.current_value))
        config.set("PLAYER1_COLOR", "blue", str(self.color_picker_player1_laser.slider_blue.current_value))

        config.set("PLAYER2_COLOR", "red", str(self.color_picker_player2_laser.slider_red.current_value))
        config.set("PLAYER2_COLOR", "green", str(self.color_picker_player2_laser.slider_green.current_value))
        config.set("PLAYER2_COLOR", "blue", str(self.color_picker_player2_laser.slider_blue.current_value))

        save_config()

    def back(self):
        self.active = False

        self.slider_health.set_current_value(config.getint("PLAYERS_STATS", "health"))
        self.slider_lasers.set_current_value(config.getint("PLAYERS_STATS", "lasers"))

        self.key_changer_player1_left.set_key(config.get("PLAYER1_CONTROLS", "left"))
        self.key_changer_player1_right.set_key(config.get("PLAYER1_CONTROLS", "right"))
        self.key_changer_player1_up.set_key(config.get("PLAYER1_CONTROLS", "up"))
        self.key_changer_player1_down.set_key(config.get("PLAYER1_CONTROLS", "down"))
        self.key_changer_player1_fire.set_key(config.get("PLAYER1_CONTROLS", "fire"))

        self.key_changer_player2_left.set_key(config.get("PLAYER2_CONTROLS", "left"))
        self.key_changer_player2_right.set_key(config.get("PLAYER2_CONTROLS", "right"))
        self.key_changer_player2_up.set_key(config.get("PLAYER2_CONTROLS", "up"))
        self.key_changer_player2_down.set_key(config.get("PLAYER2_CONTROLS", "down"))
        self.key_changer_player2_fire.set_key(config.get("PLAYER2_CONTROLS", "fire"))

        self.color_picker_player1_laser.set_color(red=config.getint("PLAYER1_COLOR", "red"),
                                                  green=config.getint("PLAYER1_COLOR", "green"),
                                                  blue=config.getint("PLAYER1_COLOR", "blue"))

        self.color_picker_player2_laser.set_color(red=config.getint("PLAYER2_COLOR", "red"),
                                                  green=config.getint("PLAYER2_COLOR", "green"),
                                                  blue=config.getint("PLAYER2_COLOR", "blue"))

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
