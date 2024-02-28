import pygame

from config import *
from effects import Glow


class Slider:
    def __init__(self, text: str, current_value: int, min_value: int, max_value: int, x: int, y: int, width: int):
        self.height = 10

        # Text
        self.text_font = pygame.font.SysFont("arialblack", 15)
        self.text_color = BLACK
        self.text = self.text_font.render(text, True, self.text_color)
        self.text_x = x
        self.text_y = y - self.text.get_height()

        # Value
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = current_value

        # Create the empty rect
        self.empty_rect = pygame.Rect(x, y, width, self.height)
        self.empty_rect_color = WHITE

        # Create the filled rect
        self.filled_rect = pygame.Rect(x, y, 0, self.height)
        self.filled_rect_color = VIOLET

        # Glow
        self.glow = Glow(size=2, object_rect=self.filled_rect, color=self.filled_rect_color)

        # Create the thumb
        self.thumb = pygame.Rect(x, y - 2, 6, self.height + 4)
        self.thumb_color = BLACK

        # Set the current value
        self.set_current_value(self.current_value)

        # "True" if the user is dragging the slider thumb else "False"
        self.dragging = False

    def check_drag(self, mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            if self.empty_rect.collidepoint(mouse_pos):
                self.dragging = True
        else:
            self.dragging = False

    def drag(self, mouse_pos):
        if mouse_pos[0] < self.empty_rect.x:
            self.thumb.x = self.empty_rect.x
        elif mouse_pos[0] > self.empty_rect.x + self.empty_rect.width:
            self.thumb.x = self.empty_rect.x + self.empty_rect.width
        else:
            self.thumb.x = mouse_pos[0]

        self.filled_rect.width = self.thumb.x - self.filled_rect.x
        self.current_value = round((self.max_value-self.min_value) * self.filled_rect.width/self.empty_rect.width
                                   + self.min_value)

    def set_current_value(self, value: int):
        self.current_value = value
        self.filled_rect.width = round(((self.current_value-self.min_value) / (self.max_value-self.min_value))
                                       * self.empty_rect.width)
        self.thumb.x = self.empty_rect.x + self.filled_rect.width

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.check_drag(mouse_pos)
        if self.dragging:
            self.drag(mouse_pos)

        self.glow.update(dt)

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.empty_rect_color, self.empty_rect)
        pygame.draw.rect(pygame.display.get_surface(), self.filled_rect_color, self.filled_rect)
        pygame.draw.rect(pygame.display.get_surface(), self.thumb_color, self.thumb)
        self.glow.draw()

        pygame.display.get_surface().blit(self.text, (self.text_x, self.text_y))
        current_value_text = self.text_font.render(f"{str(self.current_value)}/{self.max_value}", True, self.text_color)
        pygame.display.get_surface().blit(current_value_text, (self.text_x + self.text.get_width(), self.text_y))
