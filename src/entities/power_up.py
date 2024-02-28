import pygame
import random
import time
from pathlib import Path

from config import *
from gui import Stats
from effects import Glow


class PowerUp:
    def __init__(self):
        # Create the powers
        self.powers = ["increase_health", "increase_max_lasers", "double_laser_height", "double_laser_speed",
                       "switch_controls", "inverse_controls", "double_player_speed"]

        # Timer properties
        self.wait = True
        self.start_time = time.perf_counter()
        self.current_time = 0
        self.default_cooldown = 10
        self.active_cooldown = 30
        self.cooldown = self.default_cooldown

        # Animations
        self.animations = {"increase_health": [], "double_player_speed": [], "double_laser_speed": [],
                           "increase_max_lasers": [], "double_laser_height": [], "inverse_controls": [],
                           "switch_controls": []}
        self.animation_index = 0
        self.animation_speed = 1
        self.import_sprites()

        # "True" if the power up was collected, else "False"
        self.visible = False

        # Initialize needed variables
        self.rect = None
        self.image = None
        self.power = None

        self.player = None
        self.player_lasers = None
        self.other_player = None

        self.glow_color = None
        self.glow = None

        # Sound
        self.collect_sound = pygame.mixer.Sound(Path("assets/sounds/powerup_collect.wav"))
        self.collect_sound_volume = config.getfloat("SOUND", "game")
        self.collect_sound.set_volume(self.collect_sound_volume)

    def import_sprites(self):
        for animation in self.animations.keys():
            for index in range(1, 5):
                self.animations[animation].append(pygame.transform.scale(pygame.image.load(
                    Path(f"assets/sprites/power_up/power_up_{animation}/power_up_{animation}_{index}.png")),
                    (48, 48)).convert_alpha())

    def check_time(self):
        self.current_time = time.perf_counter() - self.start_time
        if self.current_time >= self.cooldown:
            self.wait = False
            self.start_time = time.perf_counter()

    def reset(self):
        if self.power == "double_laser_height":
            self.player_lasers.height /= 2
        elif self.power == "double_laser_speed":
            self.player_lasers.speed /= 2
        elif self.power == "switch_controls":
            self.switch_controls(self.player, self.other_player)
        elif self.power == "inverse_controls":
            self.inverse_controls(self.other_player)
        elif self.power == "double_player_speed":
            self.player.speed /= 2
            self.player.animation_speed /= 2

    def set_power(self):
        self.power = random.choice(self.powers)

    def set_glow_color(self):
        if self.power == "increase_health" or self.power == "double_player_speed" or self.power == "double_laser_speed"\
                or self.power == "increase_max_lasers" or self.power == "double_laser_height":
            self.glow_color = GREEN
        elif self.power == "inverse_controls":
            self.glow_color = BLUE
        elif self.power == "switch_controls":
            self.glow_color = YELLOW

    def spawn(self):
        self.rect.x = random.choice(range(20, pygame.display.get_surface().get_width() - self.rect.width - 20))
        self.rect.y = random.choice(range(Stats.height + 20,
                                          pygame.display.get_surface().get_height() - self.rect.height - 20))

    def new(self):
        self.set_power()
        self.set_glow_color()

        self.animation_index = 0
        self.image = self.animations[self.power][int(self.animation_index)]
        self.rect = self.image.get_rect()

        self.spawn()

        self.visible = True
        self.wait = True
        self.cooldown = self.default_cooldown

        # Create the glow
        self.glow = Glow(size=7, object_rect=self.rect, color=self.glow_color)

    def animate(self, dt):
        self.animation_index += self.animation_speed * dt

        if self.animation_index >= 4:
            self.animation_index = 0

        self.image = self.animations[self.power][int(self.animation_index)]

    def update(self, dt):
        self.check_time()
        if not self.wait and not self.visible and self.power is not None:
            self.reset()
        if not self.wait:
            self.new()

        if self.visible:
            self.animate(dt)
        if self.visible:
            self.glow.update(dt)

    def draw(self):
        if self.visible:
            pygame.display.get_surface().blit(self.image, (self.rect.x, self.rect.y))
            # pygame.draw.rect(pygame.display.get_surface(), self.rect_color, self.rect, border_radius=100)
            self.glow.draw()

    @staticmethod
    def inverse_controls(other_player):
        other_player.key_left, other_player.key_right = other_player.key_right, other_player.key_left
        other_player.key_up, other_player.key_down = other_player.key_down, other_player.key_up

    @staticmethod
    def switch_controls(player, other_player):
        player.key_left, other_player.key_left = other_player.key_left, player.key_left
        player.key_right, other_player.key_right = other_player.key_right, player.key_right
        player.key_up, other_player.key_up = other_player.key_up, player.key_up
        player.key_down, other_player.key_down = other_player.key_down, player.key_down
        player.key_fire, other_player.key_fire = other_player.key_fire, player.key_fire

    def activate(self):
        if self.power == "increase_health":
            self.player.health += 1
        elif self.power == "increase_max_lasers":
            self.player_lasers.max_lasers += 1
        elif self.power == "double_laser_height":
            self.player_lasers.height *= 2
        elif self.power == "double_laser_speed":
            self.player_lasers.speed *= 2
        elif self.power == "switch_controls":
            self.switch_controls(self.player, self.other_player)
        elif self.power == "inverse_controls":
            self.inverse_controls(self.other_player)
        elif self.power == "double_player_speed":
            self.player.speed *= 2
            self.player.animation_speed *= 2

        self.visible = False
        self.cooldown = self.active_cooldown
        self.start_time = time.perf_counter()

    def collect(self, player, player_lasers, other_player):
        self.player = player
        self.player_lasers = player_lasers
        self.other_player = other_player

        self.collect_sound.play()
        self.activate()
