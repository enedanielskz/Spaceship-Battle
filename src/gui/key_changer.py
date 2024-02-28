import pygame

from config import *


class KeyChanger:
    def __init__(self, text: str, text_distance: int, current_key: str, x: int, y: int):
        # Text
        self.text_font = pygame.font.SysFont("arialblack", 15)
        self.text_color = BLACK
        self.text = self.text_font.render(text, True, self.text_color)
        self.text_x = x
        self.text_y = y - 3

        # Create the rect
        self.rect = pygame.Rect(x + self.text.get_width() + text_distance, y, 140, 15)
        self.rect_border = pygame.Rect(0, 0, 148, 23)
        self.rect_border.center = self.rect.center

        # Key
        self.current_key = current_key
        self.active = False
        self.pressed = False

        # Key text
        self.key_text_font = pygame.font.SysFont("arial", 14, italic=True, bold=True)
        self.key_text = self.key_text_font.render(self.current_key, True, BLACK)
        self.key_text_rect = self.key_text.get_rect(center=self.rect.center)

    def check_click(self, disabled):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not disabled:
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif self.pressed:
                self.activate()
                self.pressed = False
        else:
            self.pressed = False

    def update_key_text(self):
        self.key_text = self.key_text_font.render(self.current_key, True, BLACK)
        self.key_text_rect = self.key_text.get_rect(center=self.rect.center)

    def activate(self):
        self.current_key = "Press a key"
        self.update_key_text()
        self.active = True

    def change_key(self):
        keys_pressed = pygame.key.get_pressed()
        self.current_key = get_key_name(keys_pressed)
        if self.current_key:
            self.update_key_text()
            self.active = False

    def set_key(self, key: str):
        self.active = False
        self.current_key = key
        self.update_key_text()

    def update(self, disabled: bool = False):
        self.check_click(disabled)
        if self.active:
            self.change_key()

    def draw(self):
        pygame.display.get_surface().blit(self.text, (self.text_x, self.text_y))
        if self.active:
            pygame.draw.rect(pygame.display.get_surface(), BLACK, self.rect_border)
        pygame.draw.rect(pygame.display.get_surface(), WHITE, self.rect)
        pygame.display.get_surface().blit(self.key_text, self.key_text_rect)
