import pygame
from  settings import *

class ProjectileManager:
    def __init__(self, player, camera, velocity_x, velocity_y, base_speed, projectiles):
        self.player = player
        self.camera = camera
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.base_speed = base_speed
        self.projectiles = projectiles  # Use the passed projectiles list

    def calculate_direction(self, screen_pos, mouse_pos):
        dx = mouse_pos[0] - screen_pos[0]
        dy = mouse_pos[1] - screen_pos[1]
        magnitude = (dx**2 + dy**2) ** 0.5
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude
        return (dx, dy)

    def create_projectile(self, mouse_pos):
        screen_pos = (self.player.x - self.camera.x + self.player.width // 2,
                      self.player.y - self.camera.y + self.player.height // 2)
        direction = self.calculate_direction(screen_pos, mouse_pos)

        projectile_speed_x = direction[0] * self.base_speed + self.velocity_x
        projectile_speed_y = direction[1] * self.base_speed + self.velocity_y
        
        self.projectiles.append({
            "pos": [self.player.x + self.player.width // 2, self.player.y + self.player.height // 2],
            "velocity": [projectile_speed_x, projectile_speed_y]
        })

    def update_projectiles(self):
        if not self.projectiles:
            return  # Exit if there are no projectiles to update

        for projectile in self.projectiles[:]:
            # Update the position based on the velocity
            projectile["pos"][0] += projectile["velocity"][0]
            projectile["pos"][1] += projectile["velocity"][1]

        # Remove projectile if it goes off-screen
        if projectile["pos"][0] < 0 or projectile["pos"][0] > MAP_WIDTH or projectile["pos"][1] < 0 or projectile["pos"][1] > MAP_HEIGHT:
            self.projectiles.remove(projectile)

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            self.create_projectile(mouse_pos)
    

# Usage:
# Inside your game loop, you would call update_projectiles() to move projectiles
