import pygame

from config import *


class Glow:
    enabled = config.getboolean("EFFECTS", "glow")

    def __init__(self, size: int, object_rect, color: tuple[int, int, int]):
        # Set the size
        self.size = size

        # Set the object rect
        self.object_rect = object_rect

        # Set the color
        self.color = color

        # Create the rect
        self.rect = pygame.Rect(self.object_rect.x - self.size,         # x
                                self.object_rect.y - self.size,         # y
                                self.object_rect.width + self.size*2,   # width
                                self.object_rect.height + self.size*2)  # height

        # Create the surface
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Alpha properties
        self.min_alpha = 60
        self.max_alpha = 160
        self.alpha = self.min_alpha
        self.add_alpha = True
        self.alpha_speed = 100
        self.alpha_dt_speed = 0

    def update_position(self):
        self.rect.x = self.object_rect.x - self.size
        self.rect.y = self.object_rect.y - self.size

    def update_size(self):
        self.rect.width = self.object_rect.width + self.size*2
        self.rect.height = self.object_rect.height + self.size*2
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    def check_alpha(self):
        if self.alpha > self.max_alpha:
            self.add_alpha = False
            self.alpha = self.max_alpha
            self.alpha_dt_speed = 0
        elif self.alpha < self.min_alpha:
            self.add_alpha = True
            self.alpha = self.min_alpha
            self.alpha_dt_speed = 0

    def update_alpha(self, dt):
        if self.add_alpha:
            self.alpha_dt_speed += dt * self.alpha_speed
            self.alpha = self.min_alpha + round(self.alpha_dt_speed)
        else:
            self.alpha_dt_speed += dt * self.alpha_speed
            self.alpha = self.max_alpha - round(self.alpha_dt_speed)

    def update(self, dt):
        self.update_position()
        self.update_size()
        self.check_alpha()
        self.update_alpha(dt)

    def draw(self):
        if Glow.enabled:
            pygame.draw.rect(self.surface, self.color + (self.alpha,), self.surface.get_rect(), border_radius=100)
            pygame.display.get_surface().blit(self.surface, self.rect, special_flags=pygame.BLEND_ALPHA_SDL2)
