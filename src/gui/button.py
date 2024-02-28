import pygame
from pathlib import Path
from typing import Callable

from config import *


class Button:
    def __init__(self, text: str, x: int, y: int, width: int, height: int, command: Callable = None):
        # Set the elevation and get the original y pos of the top rect
        self.elevation = 10
        self.dynamic_elevation = self.elevation
        self.top_rect_original_y = y + self.elevation

        # Create the top rect
        self.top_rect = pygame.Rect(x, self.top_rect_original_y, width, height)
        self.top_rect_elevated = pygame.Rect(x, y, width, height)  # invisible, only used for hover check
        self.top_rect_default_color = DARK_PURPLE
        self.top_rect_hover_color = VIOLET
        self.top_rect_color = self.top_rect_default_color

        # Create the bottom rect
        self.bottom_rect = pygame.Rect(x, self.top_rect_original_y, width, height)
        self.bottom_rect_default_color = DARK_BLUE
        self.bottom_rect_hover_color = PURPLE
        self.bottom_rect_color = self.bottom_rect_default_color

        # Create and render the text
        self.font = pygame.font.SysFont("arialblack", 20)
        self.text = self.font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect(center=self.top_rect.center)

        # Mouse interact
        self.command = command
        self.presed = False
        self.new_hover = True

        # Sound
        self.hover_sound = pygame.mixer.Sound(Path("assets/sounds/laser_fire.wav"))
        self.click_sound = pygame.mixer.Sound(Path("assets/sounds/spaceship_hit.wav"))
        self.update_sound_volume()

    def set_elevation(self):
        self.top_rect.y = self.top_rect_original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

    def check_mouse_interact(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect_elevated.collidepoint(mouse_pos) or self.bottom_rect.collidepoint(mouse_pos):
            self.top_rect_color = self.top_rect_hover_color
            self.bottom_rect_color = self.bottom_rect_hover_color

            if self.new_hover:
                self.hover_sound.play()
                self.new_hover = False

            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.presed = True
            elif self.presed:
                self.click_sound.play()
                self.presed = False
                if self.command is not None:
                    self.command()
            else:
                self.dynamic_elevation = self.elevation
        else:
            self.presed = False
            self.new_hover = True
            self.dynamic_elevation = self.elevation
            self.top_rect_color = self.top_rect_default_color
            self.bottom_rect_color = self.bottom_rect_default_color

    def update_sound_volume(self):
        volume = config.getfloat("SOUND", "menu")
        self.hover_sound.set_volume(volume)
        self.click_sound.set_volume(volume)

    def update(self):
        self.set_elevation()
        self.check_mouse_interact()

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.bottom_rect_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(pygame.display.get_surface(), self.top_rect_color, self.top_rect, border_radius=12)
        pygame.display.get_surface().blit(self.text, self.text_rect)
