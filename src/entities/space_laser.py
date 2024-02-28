import pygame

from config import *
from gui import Stats
from effects import Glow


class SpaceLaser:
    def __init__(self):
        self.width = 10

        # Create the space laser
        self.rect = pygame.Rect((pygame.display.get_surface().get_width() + self.width) // 2,  # x
                                Stats.height,                                                  # y
                                self.width,                                                    # width
                                pygame.display.get_surface().get_height() - Stats.height)      # height

        # Properties
        self.color = RED
        self.direction = -1
        self.pos_x = self.rect.x
        self.range = 225
        self.speed = 150

        # Create the glow
        self.glow = Glow(size=7, object_rect=self.rect, color=self.color)

    def set_direction(self):
        if self.rect.x <= self.range:
            self.direction = 1
        elif self.rect.x + self.rect.width >= pygame.display.get_surface().get_width() - self.range:
            self.direction = -1

    def move(self, dt):
        self.pos_x += self.direction * self.speed * dt
        self.rect.x = round(self.pos_x)

    def update(self, dt):
        self.set_direction()
        self.move(dt)
        self.glow.update(dt)

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.rect)
        self.glow.draw()
