import pygame
import random

# Decoration stars class
class Stars:
    def __init__(self, velocity_x, velocity_y):
        #Randomly choose where the start from (to prevent spawning from middle of the screen)
        self.start_pos = random.choice(['up', 'right'])

        # Star falls from above the game screen
        if self.start_pos == 'up':
            self.x = random.randint(0, 800)
            self.y = 0
        # Star falls from right side of the game screen
        if self.start_pos == 'right':    
            self.y = random.randint(0, 600)
            self.x = 800
        
        # Velocity given when called to provide random velocities
        self.velocity = [velocity_x, velocity_y]

        # Don't do much, but change the speed as per the size
        self.size = random.choice(('small', 'medium', 'large'))

    # Drawing the stars on the screen
    def draw(self, screen):

        if self.size == 'small':
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 0.2)
        if self.size == 'medium':
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 0.5)
        if self.size == 'large':
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 1)
    
    # Movement of the stars will be according to the size (my multiplying with a scale based on size)
    def movement(self):

        self.velocity_scale = 1 if self.size == 'small' else 0.75 if self.size == 'medium' else 0.5
        self.x -= self.velocity[0] * self.velocity_scale
        self.y += self.velocity[1] * self.velocity_scale