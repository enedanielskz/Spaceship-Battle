import pygame

from config import *
from effects import Glow


class Checkbox:
    def __init__(self, text: str, text_distance: int, checked: bool, x: int, y: int):
        # Text
        self.text_font = pygame.font.SysFont("arialblack", 15)
        self.text_color = BLACK
        self.text = self.text_font.render(text, True, self.text_color)
        self.text_x = x
        self.text_y = y - 3

        # "True" if checkbox is checked else "False"
        self.checked = checked

        # Create the rect
        self.rect = pygame.Rect(x + self.text.get_width() + text_distance, y, 15, 15)
        self.rect_color = self.set_rect_color()

        # Glow
        self.glow = Glow(size=3, object_rect=self.rect, color=self.rect_color)

        self.pressed = False

    def set_rect_color(self):
        return GREEN if self.checked else RED

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif self.pressed:
                self.checked = not self.checked
                self.rect_color = self.set_rect_color()
                self.glow.color = self.rect_color
                self.pressed = False
        else:
            self.pressed = False

    def set_checked(self, checked: bool):
        self.checked = checked
        self.rect_color = self.set_rect_color()
        self.glow.color = self.rect_color

    def update(self, dt):
        self.check_click()
        self.glow.update(dt)

    def draw(self):
        pygame.display.get_surface().blit(self.text, (self.text_x, self.text_y))
        pygame.draw.rect(pygame.display.get_surface(), self.rect_color, self.rect)
        self.glow.draw()
