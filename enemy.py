import pygame
import random
from utils import clamp
from projectile import create_projectile

class Enemy:
    def __init__(self, x, y, width, height, color, health, projectile_speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = health
        self.projectile_speed = projectile_speed
        self.projectiles = []  # List of projectiles fired by the enemy

    def take_damage(self, damage):
        """Reduce health by damage amount."""
        self.health -= damage

    def shoot_projectile(self, target_x, target_y):
        """Shoot a projectile toward the player."""
        direction = (target_x - self.rect.centerx, target_y - self.rect.centery)
        distance = max(1, (direction[0]**2 + direction[1]**2)**0.5)  # Avoid division by zero
        velocity = (
            direction[0] / distance * self.projectile_speed,
            direction[1] / distance * self.projectile_speed,
        )
        self.projectiles.append({
            "pos": [self.rect.centerx, self.rect.centery],
            "velocity": list(velocity),
        })

    def update_projectiles(self, screen_width, screen_height):
        """Update projectile positions and remove off-screen ones."""
        for projectile in self.projectiles[:]:
            projectile["pos"][0] += projectile["velocity"][0]
            projectile["pos"][1] += projectile["velocity"][1]
            if not (0 <= projectile["pos"][0] <= screen_width and 0 <= projectile["pos"][1] <= screen_height):
                self.projectiles.remove(projectile)

    def draw(self, screen, camera):
        """Draw the enemy and its projectiles."""
        pygame.draw.rect(screen, self.color, (
            self.rect.x - camera.x,
            self.rect.y - camera.y,
            self.rect.width,
            self.rect.height,
        ))
        for projectile in self.projectiles:
            pygame.draw.circle(screen, (255, 0, 0), (
                int(projectile["pos"][0] - camera.x),
                int(projectile["pos"][1] - camera.y),
            ), 5)
