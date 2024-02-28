import pygame

from config import *


class Stats:
    height = 35

    def __init__(self):
        self.rect = pygame.Rect(0, 0, pygame.display.get_surface().get_width(), Stats.height)

        self.text_spacing = 40
        self.text_y = self.rect.height // 4

        self.font_size = self.rect.height // 2
        self.font = pygame.font.SysFont("arialblack", self.font_size)

        self.bg = DARK_PURPLE
        self.fg = WHITE

    def draw(self, player1_health, player2_health, player1_available_lasers, player2_available_lasers, power_up_time):
        # Draw the stats bar
        pygame.draw.rect(pygame.display.get_surface(), self.bg, self.rect)

        # Render the health text
        player1_health_text = self.font.render(f"Health: {player1_health}", True, self.fg)
        player2_health_text = self.font.render(f"Health: {player2_health}", True, self.fg)

        # Draw the health text
        pygame.display.get_surface().blit(player1_health_text,  # text
                                          (10,                  # x
                                           self.text_y))        # y

        pygame.display.get_surface().blit(player2_health_text,                                      # text
                                          (self.rect.width - player2_health_text.get_width() - 10,  # x
                                           self.text_y))                                            # y

        # Render the available lasers text
        player1_available_lasers_text = self.font.render(f"Lasers: {player1_available_lasers}", True, self.fg)
        player2_available_lasers_text = self.font.render(f"Lasers: {player2_available_lasers}", True, self.fg)

        # Draw the available lasers text
        pygame.display.get_surface().blit(player1_available_lasers_text,                         # text
                                          (self.text_spacing + player1_health_text.get_width(),  # x
                                           self.text_y))                                         # y

        pygame.display.get_surface().blit(player2_available_lasers_text,                                   # text
                                          (self.rect.width - player2_health_text.get_width() -             # x
                                           player2_available_lasers_text.get_width() - self.text_spacing,  # x
                                           self.text_y))                                                   # y

        # Render the power-up time text
        power_up_time_text = self.font.render(f"New power-up in: {power_up_time}s", True, self.fg)

        # Draw the power-up time text
        pygame.display.get_surface().blit(power_up_time_text,                                          # text
                                          (((self.rect.width - power_up_time_text.get_width()) // 2),  # x
                                           self.text_y))                                               # y
