import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy as np

# Constants
WIDTH = 1000
HEIGHT = 1000
NUM_STARS = 1000
Z_MAX = -1000  # Farthest z-depth
Z_MIN = 0      # Closest z-depth (camera position)
SPEED = 10     # Base speed of stars
ACCEL = 0.1    # Acceleration factor
FPS = 60       # Frames per second

# Initialize Pygame and OpenGL
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 2000.0)
glTranslatef(0.0, 0.0, 0.0)  # Camera at origin
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Additive blending for star glow
glEnable(GL_POINT_SMOOTH)

# Star class
class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        # Random position in 3D space, starting far away
        self.pos = np.array([
            random.uniform(-WIDTH / 2, WIDTH / 2),
            random.uniform(-HEIGHT / 2, HEIGHT / 2),
            random.uniform(Z_MAX, Z_MAX + 100)  # Start slightly beyond Z_MAX
        ])
        self.speed = SPEED

    def update(self, dt, accel):
        # Move star toward camera (increase z)
        self.speed += accel * dt  # Accelerate over time
        self.pos[2] += self.speed * dt
        # Reset if past camera
        if self.pos[2] > Z_MIN:
            self.reset()

    def draw(self):
        glPointSize(2.0 + self.speed * 0.1)  # Size increases with speed
        glBegin(GL_POINTS)
        glColor4f(1.0, 1.0, 1.0, 0.8)  # White with slight transparency
        glVertex3fv(self.pos)
        glEnd()

# Create stars
stars = [Star() for _ in range(NUM_STARS)]

# Main loop
running = True
clock = pygame.time.Clock()
time_elapsed = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(FPS) / 1000.0
    time_elapsed += dt

    # Increase acceleration over time for "ludicrous" effect
    accel = ACCEL * (1 + time_elapsed * 0.5)  # Acceleration ramps up

    # Update stars
    for star in stars:
        star.update(dt, accel)

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background

    # Draw stars
    for star in stars:
        star.draw()

    pygame.display.flip()

pygame.quit()