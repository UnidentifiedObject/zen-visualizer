import pygame
import random
import math
import colorsys

pygame.init()

#Screen setup
WIDTH, HEIGHT = 1200, 780
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Zen Visualizer")

#clock for frame rate
clock = pygame.time.Clock()

#Colors
PARTICLE_COLORS = [
    (255,100,100), #Red
    (100,255,100), #Green
    (100,100,255), #Blue
    (255,200,100), #Orange
    (200,180,255), #Lavender
]

#Particle class
class Particle:
    def __init__(self):
        self.x = random.uniform(0,WIDTH)
        self.y = random.uniform(0,HEIGHT)
        self.radius = random.choices(
            [4, 6, 8, 10, 12],
            weights=[15, 20, 25, 20, 10],  # More balance
            k=1
        )[0]

        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(0.2,0.5)
        self.color = random.choice(PARTICLE_COLORS)

        r, g, b = self.color
        self.h, self.s, self.v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        self.hue_speed = random.uniform(0.001, 0.005)

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        #wrap around screen
        if self.x < 0: self.x = WIDTH
        if self.x > WIDTH: self.x = 0
        if self.y < 0: self.y = HEIGHT
        if self.y > HEIGHT: self.y = 0

        # Update hue
        self.h += self.hue_speed
        if self.h > 1:
            self.h -= 1

        # Convert HSV back to RGB for drawing
        r, g, b = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        self.color = (int(r * 255), int(g * 255), int(b * 255))


    def draw(self, surface):
        # Create a temporary surface with alpha (transparency)
        temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        # Randomize alpha based on size (larger = more transparent)
        if self.radius >= 9:
            alpha = 150
        elif self.radius >= 6:
            alpha = 150
        else:
            alpha = 200

        # Draw the circle on the temp surface
        color_with_alpha = (*self.color, alpha)
        pygame.draw.circle(temp_surface, color_with_alpha, (self.radius, self.radius), self.radius)

        # Blit it to the main screen
        surface.blit(temp_surface, (self.x - self.radius, self.y - self.radius))


#generate particles
particles = [Particle() for _ in  range(255)]

#Main loop
running = True
while running:
    time = pygame.time.get_ticks() / 1000  # seconds
    pulse = 20 * math.sin(time * 0.5)  # slower pulse

    base_color = (5, 5, 30)
    pulsing_bg = tuple(min(255, max(0, int(c + pulse))) for c in base_color)
    screen.fill(pulsing_bg)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()

    if mouse_pressed:
        for particle in particles:
            dx = particle.x - mouse_pos[0]
            dy = particle.y - mouse_pos[1]
            dist = math.hypot(dx, dy)

            if 0 < dist < 150:  # Increase effect radius
                # Normalize direction
                push_x = dx / dist
                push_y = dy / dist

                # Stronger push closer to cursor
                strength = (1 - dist / 150) ** 2  # smooth falloff
                push_strength = 12 * strength  # max strength: 8 (tweak as needed)

                particle.x += push_x * push_strength
                particle.y += push_y * push_strength

    for particle in particles:
        particle.move()
        particle.draw(screen)

    if mouse_pressed:
        pygame.draw.circle(screen, (180, 180, 180, 50), mouse_pos, 30, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
