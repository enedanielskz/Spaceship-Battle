import pygame
from pathlib import Path

from config import *
from gui import Stats
from effects import Glow


class Player:
    def __init__(self, flip: bool = False):
        # Get the player side and set the player number
        self.flip = flip
        self.number = self.get_number()

        # Animations
        self.animations = {"idle": [], "move_forward": [], "move_backward": [], "move_up": [], "move_down": [],
                           "move_forward_up": [], "move_forward_down": [], "move_backward_up": [],
                           "move_backward_down": []}
        self.animation_index = 0
        self.animation_speed = 3
        self.status = "idle"
        self.import_sprites()

        # Set the image the rect
        self.image = self.animations[self.status][self.animation_index]
        self.rect = self.image.get_rect()

        # Set the spawnpoint
        self.spawnpoint = pygame.Vector2()
        self.set_spawnpoint()

        # Get the color
        self.color = self.get_color()

        # Create the color rect
        self.color_rect = pygame.Rect(self.rect.x + (self.rect.width-26) // 2,   # x
                                      self.rect.y + (self.rect.height-8) // 2,   # y
                                      26,                                        # width
                                      8)                                         # height

        # Create the glow
        self.glow = Glow(size=2, object_rect=self.color_rect, color=self.color)

        # Get the controls
        self.key_left = None
        self.key_right = None
        self.key_up = None
        self.key_down = None
        self.key_fire = None
        self.get_controls()

        # Movement properties
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Stats
        self.health = config.getint("PLAYERS_STATS", "health")
        self.speed = 150

        # Sounds
        self.hit_sound = pygame.mixer.Sound(Path("assets/sounds/spaceship_hit.wav"))
        self.hit_sound_volume = config.getfloat("SOUND", "game")
        self.hit_sound.set_volume(self.hit_sound_volume)

        # Spawn the player at the spawnpoint
        self.spawn()

    def get_number(self):
        if self.flip:
            return 2
        return 1

    def import_sprites(self):
        if self.flip:
            rotate_angle = 180
        else:
            rotate_angle = 0

        for animation in self.animations.keys():
            for index in range(1, 5):
                self.animations[animation].append(pygame.transform.rotate(pygame.image.load(
                    Path(f"assets/sprites/spaceship/{animation}/spaceship_{animation}_{index}.png")),
                    rotate_angle).convert_alpha())

    def set_spawnpoint(self):
        if self.flip:
            self.spawnpoint.x = pygame.display.get_surface().get_width() - self.rect.width - 10
        else:
            self.spawnpoint.x = 10

        self.spawnpoint.y = (pygame.display.get_surface().get_height() + Stats.height - self.rect.width) // 2

    def get_color(self):
        return (config.getint(f"PLAYER{self.number}_COLOR", "red"),
                config.getint(f"PLAYER{self.number}_COLOR", "green"),
                config.getint(f"PLAYER{self.number}_COLOR", "blue"))

    def get_controls(self):
        # Get the movement keys
        self.key_left = get_key(config.get(f"PLAYER{self.number}_CONTROLS", "left"))
        self.key_right = get_key(config.get(f"PLAYER{self.number}_CONTROLS", "right"))
        self.key_up = get_key(config.get(f"PLAYER{self.number}_CONTROLS", "up"))
        self.key_down = get_key(config.get(f"PLAYER{self.number}_CONTROLS", "down"))

        # Get the fire key
        self.key_fire = get_key(config.get(f"PLAYER{self.number}_CONTROLS", "fire"))

    def spawn(self):
        self.rect.x = self.spawnpoint.x
        self.rect.y = self.spawnpoint.y
        self.pos = pygame.math.Vector2(self.spawnpoint)

    def hit(self):
        self.health -= 1
        self.hit_sound.play()
        self.spawn()

    def get_input(self):
        keys_pressed = pygame.key.get_pressed()

        # left & right
        if keys_pressed[self.key_left]:
            self.direction.x = -1
        elif keys_pressed[self.key_right]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # up & down
        if keys_pressed[self.key_up]:
            self.direction.y = -1
        elif keys_pressed[self.key_down]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, dt):
        # Normalize the vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        if self.direction.x < 0 and self.pos.x < 0:
            self.pos.x = 0
        elif self.direction.x > 0 and self.pos.x + self.rect.width > pygame.display.get_surface().get_width():
            self.pos.x = pygame.display.get_surface().get_width() - self.rect.width

        self.rect.x = round(self.pos.x)

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        if self.direction.y < 0 and self.pos.y < Stats.height:
            self.pos.y = Stats.height
        elif self.direction.y > 0 and self.pos.y + self.rect.height > pygame.display.get_surface().get_height():
            self.pos.y = pygame.display.get_surface().get_height() - self.rect.height

        self.rect.y = round(self.pos.y)

    def update_status(self):
        if self.direction.x < 0 and self.direction.y < 0:
            if self.flip:
                self.status = "move_forward_down"
            else:
                self.status = "move_backward_up"
        elif self.direction.x > 0 > self.direction.y:
            if self.flip:
                self.status = "move_backward_down"
            else:
                self.status = "move_forward_up"
        elif self.direction.x < 0 < self.direction.y:
            if self.flip:
                self.status = "move_forward_up"
            else:
                self.status = "move_backward_down"
        elif self.direction.x > 0 and self.direction.y > 0:
            if self.flip:
                self.status = "move_backward_up"
            else:
                self.status = "move_forward_down"
        elif self.direction.x < 0:
            if self.flip:
                self.status = "move_forward"
            else:
                self.status = "move_backward"
        elif self.direction.x > 0:
            if self.flip:
                self.status = "move_backward"
            else:
                self.status = "move_forward"
        elif self.direction.y < 0:
            if self.flip:
                self.status = "move_down"
            else:
                self.status = "move_up"
        elif self.direction.y > 0:
            if self.flip:
                self.status = "move_up"
            else:
                self.status = "move_down"
        else:
            self.status = "idle"

    def animate(self, dt):
        self.animation_index += self.animation_speed * dt

        if self.animation_index >= 4:
            self.animation_index = 0

        self.image = self.animations[self.status][int(self.animation_index)]

    def update_color_rect_position(self):
        self.color_rect.x = self.rect.x + (self.rect.width-self.color_rect.width) // 2
        self.color_rect.y = self.rect.y + (self.rect.height-self.color_rect.height) // 2

    def update(self, dt):
        self.get_input()
        self.move(dt)
        self.update_status()
        self.animate(dt)
        self.update_color_rect_position()
        self.glow.update(dt)

    def draw(self):
        pygame.display.get_surface().blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.color_rect)
        self.glow.draw()
