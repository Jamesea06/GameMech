import pygame
import sys
from settings import *
from utils import *
from projectile import *
from player import *

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Space Explorer 2")

# Load and scale the background image
background = pygame.image.load("assets/paul-volkmer-qVotvbsuM_c-unsplash.jpg").convert_alpha()
background = pygame.transform.scale(background, (MAP_WIDTH, MAP_HEIGHT))

# Object lists
projectiles = []  # List to hold active projectiles
particles = []  # List of active particles


# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse click to shoot projectile
        projectile_manager = ProjectileManager(player, camera, velocity_x, velocity_y, PROJECTILE_BASE_SPEED, projectiles)
        projectile_manager.handle_mouse_event(event)

    # Check boost input
    keys = pygame.key.get_pressed()
    space_pressed = keys[pygame.K_SPACE]

    if keys[pygame.K_SPACE] and cooldown_timer <= 0 and boost_timer <= 0:
        is_boosting = True
        boost_start_time = pygame.time.get_ticks()  # Record the time boost started
        boost_timer = BOOST_DURATION
        cooldown_timer = BOOST_COOLDOWN
    
        
    if not space_pressed and is_boosting:
        elapsed_boost_time = (pygame.time.get_ticks() - boost_start_time) / 1000  # Convert to seconds
        boost_timer = 0  # Stop the boost
        is_boosting = False

        # Set cooldown proportional to boost duration
        cooldown_timer = (elapsed_boost_time / BOOST_DURATION) * BOOST_COOLDOWN

    # Handle boost timers
    if boost_timer > 0:
        boost_timer -= 1 / 60  # Decrease with respect to frame rate
        if boost_timer <= 0:
            is_boosting = False
    elif cooldown_timer > 0:
        cooldown_timer -= 1 / 60  # Decrease with respect to frame rate

    # Update player movement
    input_x = (keys[pygame.K_d] - keys[pygame.K_a])
    input_y = (keys[pygame.K_s] - keys[pygame.K_w])
    max_speed = boost_max_speed if is_boosting else base_max_speed

    if input_x != 0:
        velocity_x += input_x * acceleration
    else:
        velocity_x = velocity_x - friction * (1 if velocity_x > 0 else -1) if abs(velocity_x) > friction else 0

    if input_y != 0:
        velocity_y += input_y * acceleration
    else:
        velocity_y = velocity_y - friction * (1 if velocity_y > 0 else -1) if abs(velocity_y) > friction else 0

    velocity_x = clamp(velocity_x, -max_speed, max_speed)
    velocity_y = clamp(velocity_y, -max_speed, max_speed)

    player.x += velocity_x
    player.y += velocity_y
    player.x = clamp(player.x, 0, MAP_WIDTH - player.width)
    player.y = clamp(player.y, 0, MAP_HEIGHT - player.height)

    handle_camera(player, camera, inner_dead_zone, outer_dead_zone)

    outer_dead_zone.x, outer_dead_zone.y = camera.x, camera.y
    inner_dead_zone.x = camera.x + (SCREEN_WIDTH - INNER_DEAD_ZONE_WIDTH) // 2
    inner_dead_zone.y = camera.y + (SCREEN_HEIGHT - INNER_DEAD_ZONE_HEIGHT) // 2

    # Update projectiles
    for projectile in projectiles:
        projectile_screen_x = projectile["pos"][0] - camera.x
        projectile_screen_y = projectile["pos"][1] - camera.y
        pygame.draw.circle(screen, PROJECTILE_COLOR, (int(projectile_screen_x), int(projectile_screen_y)), 5)


    # Create particles during boost
    if is_boosting:
        create_particle(player.x + player.width // 2, player.y + player.height // 2,particles)

    # Update particles
    for particle in particles[:]:
        particle["lifetime"] -= 1
        if particle["lifetime"] <= 0:
            particles.remove(particle)

    # Draw the background
    screen.blit(background, (-camera.x, -camera.y))

    # Draw particles
    for particle in particles:
        particle_screen_x = particle["pos"][0] - camera.x
        particle_screen_y = particle["pos"][1] - camera.y
        pygame.draw.circle(screen, PARTICLE_COLOR, (int(particle_screen_x), int(particle_screen_y)), particle["size"])

    # Draw the player
    player_screen_x = player.x - camera.x
    player_screen_y = player.y - camera.y
    pygame.draw.rect(screen, PLAYER_COLOR, (player_screen_x, player_screen_y, player.width, player.height))

    projectile_manager.update_projectiles()
    # Draw projectiles
    for projectile in projectiles:
        projectile_screen_x = projectile["pos"][0] - camera.x
        projectile_screen_y = projectile["pos"][1] - camera.y
        pygame.draw.circle(screen, PROJECTILE_COLOR, (int(projectile_screen_x), int(projectile_screen_y)), 5)
    
    
    # Draw boost meter
    meter_width, meter_height = 20, 200
    meter_x, meter_y = SCREEN_WIDTH - meter_width - 10, 10
    cooldown_ratio = max(0, cooldown_timer / BOOST_COOLDOWN)
    boost_ratio = max(0, boost_timer / BOOST_DURATION)

    # Cooldown bar
    pygame.draw.rect(screen, (100, 100, 100), (meter_x, meter_y, meter_width, meter_height))
    pygame.draw.rect(screen, (0, 255, 0), (meter_x, meter_y + meter_height * cooldown_ratio, meter_width, meter_height * (1 - cooldown_ratio)))

    # Boost bar
    pygame.draw.rect(screen, (0, 255, 0), (meter_x, meter_y + meter_height * (1 - boost_ratio), meter_width, meter_height * boost_ratio))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
