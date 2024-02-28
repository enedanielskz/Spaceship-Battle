import pygame

from config import *

pygame.font.init()
FONT = pygame.font.SysFont("arialblack", 15)
COLOR_ABOVE_60 = GREEN
COLOR_BELOW_60 = RED


def draw_fps(current_fps: int):
    if current_fps >= 60:
        color = COLOR_ABOVE_60
    else:
        color = COLOR_BELOW_60

    # Render the text
    text = FONT.render(f"FPS: {current_fps}", True, color)
    # Draw the text
    pygame.display.get_surface().blit(text,                                                                  # text
                                      (10,                                                                   # x
                                       pygame.display.get_surface().get_height() - text.get_height() - 10))  # y
