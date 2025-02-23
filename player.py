import pygame
from settings import *
from utils import *

class Ship:
    def __init__(self, rect):
        self.rect = rect  # The player is represented by a Rect (position and size)
        self.velocity_x = 0
        self.velocity_y = 0

    def handle_input(self, keys, boost_max_speed, base_max_speed, is_boosting, acceleration, friction):
        input_x = (keys[pygame.K_d] - keys[pygame.K_a])  # Right and left movement
        input_y = (keys[pygame.K_s] - keys[pygame.K_w])  # Down and up movement
        max_speed = boost_max_speed if is_boosting else base_max_speed

        # Update the velocity based on input
        if input_x != 0:
            self.velocity_x += input_x * acceleration
        else:
            # Apply friction when no input is given
            self.velocity_x = self.velocity_x - friction * (1 if self.velocity_x > 0 else -1) if abs(self.velocity_x) > friction else 0

        if input_y != 0:
            self.velocity_y += input_y * acceleration
        else:
            # Apply friction when no input is given
            self.velocity_y = self.velocity_y - friction * (1 if self.velocity_y > 0 else -1) if abs(self.velocity_y) > friction else 0

        # Clamp the velocities to the max speed
        self.velocity_x = clamp(self.velocity_x, -max_speed, max_speed)
        self.velocity_y = clamp(self.velocity_y, -max_speed, max_speed)

        # Update the rect's position based on velocity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Clamp the player's rect within the map boundaries
        self.rect.x = clamp(self.rect.x, 0, MAP_WIDTH - self.rect.width)
        self.rect.y = clamp(self.rect.y, 0, MAP_HEIGHT - self.rect.height)