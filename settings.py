import pygame 

# Screen and map settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 2500, 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Dead zones
OUTER_DEAD_ZONE_WIDTH, OUTER_DEAD_ZONE_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
outer_dead_zone = pygame.Rect(0, 0, OUTER_DEAD_ZONE_WIDTH, OUTER_DEAD_ZONE_HEIGHT)
INNER_DEAD_ZONE_WIDTH, INNER_DEAD_ZONE_HEIGHT = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
inner_dead_zone = pygame.Rect(0, 0, INNER_DEAD_ZONE_WIDTH, INNER_DEAD_ZONE_HEIGHT)

# Player settings
PLAYER_COLOR = (255, 0, 0)
player = pygame.Rect(200, 150, 50, 50)  # Start at the center of the map

# Physics settings
base_max_speed = 5  # Normal max speed
boost_max_speed = 10  # Max speed during boost
acceleration = 0.3
friction = 0.1
velocity_x, velocity_y = 0, 0  # Initial velocity

# Boost settings
BOOST_DURATION = 2
BOOST_COOLDOWN = 5
boost_timer = 0  # Remaining time for boost
cooldown_timer = 0  # Remaining cooldown time
is_boosting = False

# Projectile settings
PROJECTILE_COLOR = (0, 0, 255)
PROJECTILE_BASE_SPEED = 10

# Particle settings
PARTICLE_LIFETIME = 30
PARTICLE_COLOR = (255, 255, 0)
PARTICLE_SIZE = 5
