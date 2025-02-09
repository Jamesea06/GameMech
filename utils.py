import math
import random
from settings import *

def clamp(value, min_value, max_value):
    """Keep a value within a given range."""
    return max(min_value, min(value, max_value))

def handle_camera(player_rect, camera_rect, inner_dead_zone, outer_dead_zone):
    """Adjust the camera based on the player's position relative to the inner and outer dead zones."""
    if player_rect.right > inner_dead_zone.right:
        camera_rect.x += (player_rect.right - inner_dead_zone.right) * 0.1
    if player_rect.left < inner_dead_zone.left:
        camera_rect.x -= (inner_dead_zone.left - player_rect.left) * 0.1
    if player_rect.bottom > inner_dead_zone.bottom:
        camera_rect.y += (player_rect.bottom - inner_dead_zone.bottom) * 0.1
    if player_rect.top < inner_dead_zone.top:
        camera_rect.y -= (inner_dead_zone.top - player_rect.top) * 0.1

    if player_rect.right > outer_dead_zone.right:
        camera_rect.x += player_rect.right - outer_dead_zone.right
    if player_rect.left < outer_dead_zone.left:
        camera_rect.x -= outer_dead_zone.left - player_rect.left
    if player_rect.bottom > outer_dead_zone.bottom:
        camera_rect.y += player_rect.bottom - outer_dead_zone.bottom
    if player_rect.top < outer_dead_zone.top:
        camera_rect.y -= outer_dead_zone.top - player_rect.top

    camera_rect.x = clamp(camera_rect.x, 0, MAP_WIDTH - SCREEN_WIDTH)
    camera_rect.y = clamp(camera_rect.y, 0, MAP_HEIGHT - SCREEN_HEIGHT)

def calculate_direction(start, end):
    """Calculate normalized direction vector from start to end."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    distance = math.hypot(dx, dy)
    return (dx / distance, dy / distance) if distance != 0 else (0, 0)

def create_particle(x, y, particles):
    """Create a new particle at the given position."""
    particles.append({
        "pos": [x, y],
        "size": random.randint(PARTICLE_SIZE - 2, PARTICLE_SIZE + 2),
        "lifetime": PARTICLE_LIFETIME
    })
