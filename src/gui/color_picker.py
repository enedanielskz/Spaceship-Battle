import pygame

from config import *
from .slider import Slider
from effects import Glow


class ColorPicker:
    def __init__(self, text: str, text_distance: int, red: int, green: int, blue: int, x, y):
        # Text
        self.text_font = pygame.font.SysFont("arialblack", 15)
        self.text_color = BLACK
        self.text = self.text_font.render(text, True, self.text_color)
        self.text_x = x
        self.text_y = y - 3

        # Create the rect
        self.rect = pygame.Rect(x + self.text.get_width() + text_distance, y, 15, 15)
        self.rect_color = (red, green, blue)

        # Glow
        self.glow = Glow(size=3, object_rect=self.rect, color=self.rect_color)

        # Slider properties
        self.slider_x = x
        self.slider_y = y + 45
        self.slider_spacing = 35
        self.slider_width = 255

        # Create the sliders
        self.slider_red = Slider(text="Red: ",
                                 current_value=red,
                                 min_value=0,
                                 max_value=255,
                                 x=self.slider_x,
                                 y=self.slider_y,
                                 width=self.slider_width)

        self.slider_green = Slider(text="Green: ",
                                   current_value=green,
                                   min_value=0,
                                   max_value=255,
                                   x=self.slider_x,
                                   y=self.slider_red.empty_rect.y + self.slider_spacing,
                                   width=self.slider_width)

        self.slider_blue = Slider(text="Blue: ",
                                  current_value=blue,
                                  min_value=0,
                                  max_value=255,
                                  x=self.slider_x,
                                  y=self.slider_green.empty_rect.y + self.slider_spacing,
                                  width=self.slider_width)

    def update_color(self):
        self.rect_color = (self.slider_red.current_value, self.slider_green.current_value,
                           self.slider_blue.current_value)
        self.glow.color = self.rect_color

    def set_color(self, red: int, green: int, blue: int):
        self.slider_red.set_current_value(red)
        self.slider_green.set_current_value(green)
        self.slider_blue.set_current_value(blue)

    def update(self, dt):
        self.slider_red.update(dt)
        self.slider_green.update(dt)
        self.slider_blue.update(dt)

        self.update_color()
        self.glow.update(dt)

    def draw(self):
        pygame.display.get_surface().blit(self.text, (self.text_x, self.text_y))
        pygame.draw.rect(pygame.display.get_surface(), self.rect_color, self.rect)

        self.slider_red.draw()
        self.slider_green.draw()
        self.slider_blue.draw()

        self.glow.draw()
