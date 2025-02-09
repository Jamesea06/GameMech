import pygame
from settings import PROJECTILE_COLOR, PROJECTILE_BASE_SPEED
from utils import calculate_direction

class Projectile:
    def __init__(self, x, y, target_x, target_y, player_velocity):
        direction = calculate_direction((x, y), (target_x, target_y))
        self.pos = [x, y]
        self.velocity = [
            direction[0] * PROJECTILE_BASE_SPEED + player_velocity[0],
            direction[1] * PROJECTILE_BASE_SPEED + player_velocity[1],
        ]

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def draw(self, screen, camera):
        screen_x = self.pos[0] - camera.x
        screen_y = self.pos[1] - camera.y
        pygame.draw.circle(screen, PROJECTILE_COLOR, (int(screen_x), int(screen_y)), 5)