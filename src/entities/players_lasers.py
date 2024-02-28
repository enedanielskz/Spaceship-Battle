import pygame
from pathlib import Path

from config import *
from effects import Glow


class PlayerLaser(pygame.rect.Rect):
    def __init__(self, x, y, width, height, color):
        # Initialize the main Rect class
        super().__init__(x, y, width, height)

        # Set the position
        self.pos_x = self.x

        # Set the color
        self.color = color

        # Create the glow
        self.glow = Glow(size=5, object_rect=self, color=self.color)

    def split(self, player_lasers_list, removed_laser, lasers_diff):
        laser1 = PlayerLaser(x=self.x,
                             y=self.y,
                             width=self.width,
                             height=removed_laser.y - self.y,
                             color=self.color)

        laser2 = PlayerLaser(x=self.x,
                             y=self.y + self.height - lasers_diff,
                             width=self.width,
                             height=lasers_diff,
                             color=self.color)

        # Remove the initial laser from the list and append the new lasers
        player_lasers_list.remove(self)
        player_lasers_list.append(laser1)
        player_lasers_list.append(laser2)


class PlayerLasers:
    def __init__(self, color, direction):
        # Get the color and the direction of the lasers
        self.color = color
        self.direction = direction

        # Lasers properties
        self.speed = 300
        self.width = 5
        self.height = 60

        self.max_lasers = config.getint("PLAYERS_STATS", "lasers")
        self.list = []
        self.available_lasers = 0

        # Sound
        self.laser_fired_sound = pygame.mixer.Sound(Path("assets/sounds/laser_fire.wav"))
        self.laser_fired_sound_volume = config.getfloat("SOUND", "game")
        self.laser_fired_sound.set_volume(self.laser_fired_sound_volume)

    def move(self, dt):
        for laser in self.list:
            laser.pos_x += self.direction * self.speed * dt
            laser.x = round(laser.pos_x)
            laser.glow.update(dt)

    def calculate_available_lasers(self):
        self.available_lasers = self.max_lasers - len(self.list)
        if self.available_lasers < 0:
            self.available_lasers = 0

    def update(self, dt):
        self.calculate_available_lasers()
        self.move(dt)

    def draw(self):
        for laser in self.list:
            pygame.draw.rect(pygame.display.get_surface(), self.color, laser)
            laser.glow.draw()


class Player1Lasers(PlayerLasers):
    def __init__(self):
        # Set the color of the lasers
        color = (config.getint("PLAYER1_COLOR", "red"), config.getint("PLAYER1_COLOR", "green"),
                 config.getint("PLAYER1_COLOR", "blue"))

        # Set the direction of the lasers
        direction = 1

        # Call the main PlayerLasers class
        super().__init__(color, direction)

    def spawn_laser(self, player1_rect):
        # Create the laser
        laser = PlayerLaser(x=player1_rect.x + player1_rect.width,
                            y=player1_rect.y + (player1_rect.height - self.height) // 2,
                            width=self.width,
                            height=self.height,
                            color=self.color)
        # Append the laser to the list
        self.list.append(laser)

        self.laser_fired_sound.play()


class Player2Lasers(PlayerLasers):
    def __init__(self):
        # Set the color of the lasers
        color = (config.getint("PLAYER2_COLOR", "red"), config.getint("PLAYER2_COLOR", "green"),
                 config.getint("PLAYER2_COLOR", "blue"))

        # Set the direction of the lasers
        direction = -1

        # Call the main PlayerLasers class
        super().__init__(color, direction)

    def spawn_laser(self, player2_rect):
        # Create the laser
        laser = PlayerLaser(x=player2_rect.x - self.width,
                            y=player2_rect.y + (player2_rect.height - self.height) // 2,
                            width=self.width,
                            height=self.height,
                            color=self.color)
        # Append the laser to the list
        self.list.append(laser)

        self.laser_fired_sound.play()


def modify_players_lasers(player1_lasers_list, player2_lasers_list, player1_laser, player2_laser):
    if player1_laser.y == player2_laser.y and player1_laser.height == player2_laser.height:
        player1_lasers_list.remove(player1_laser)
        player2_lasers_list.remove(player2_laser)
    else:
        # calculate the difference between the y position + the height of the lasers
        lasers_diff = abs((player1_laser.y + player1_laser.height) - (player2_laser.y + player2_laser.height))

        # check if player2_laser surrounds player1_laser
        player1_laser_y_higher = player1_laser.y > player2_laser.y
        player1_laser_height_y_lower = player1_laser.y + player1_laser.height < player2_laser.y + player2_laser.height

        # check if player1_laser surrounds player2_laser
        player2_laser_y_higher = player2_laser.y > player1_laser.y
        player2_laser_height_y_lower = player2_laser.y + player2_laser.height < player1_laser.y + player1_laser.height

        if player1_laser_y_higher and player1_laser_height_y_lower:
            player2_laser.split(player2_lasers_list, player1_laser, lasers_diff)  # split player2_laser
            player1_lasers_list.remove(player1_laser)
        elif player2_laser_y_higher and player2_laser_height_y_lower:
            player1_laser.split(player1_lasers_list, player2_laser, lasers_diff)  # split player1_laser
            player2_lasers_list.remove(player2_laser)

        else:
            # calculate the difference between the height of the lasers
            lasers_height_diff = abs(player1_laser.height - player2_laser.height)

            # Change the lasers y position and height based on how they collided with eachother
            if player1_laser.height > player2_laser.height:
                if player1_laser.y < player2_laser.y:
                    player2_laser.y += player1_laser.height - lasers_diff - lasers_height_diff

                    player1_laser.height = lasers_diff + lasers_height_diff
                    player2_laser.height = lasers_diff
                else:
                    player1_laser.y += player1_laser.height - lasers_diff

                    player1_laser.height = lasers_diff
                    player2_laser.height = lasers_diff - lasers_height_diff

                if player2_laser.height == 0:
                    player2_lasers_list.remove(player2_laser)
            else:
                if player2_laser.y < player1_laser.y:
                    player1_laser.y += player2_laser.height - lasers_diff - lasers_height_diff

                    player1_laser.height = lasers_diff
                    player2_laser.height = lasers_diff + lasers_height_diff
                else:
                    player2_laser.y += player2_laser.height - lasers_diff

                    player1_laser.height = lasers_diff - lasers_height_diff
                    player2_laser.height = lasers_diff

                if player1_laser.height == 0:
                    player1_lasers_list.remove(player1_laser)
