import pygame
import math

class Cube:

    def __init__(self, x, y, z):
        # Game coords
        self.x = x
        self.y = y
        self.z = z

        
        self.color = (255, 0, 0)
        self.edge_size = 30

    def draw(self, screen):
        self.coords = (400 + self.y * 17.5 * math.sqrt(3) + self.x * 17.5 * math.sqrt(3), 
                       400 - self.y * 17.5 + self.x * 17.5)
        self.polygon = [
            (self.coords[0], self.coords[1] - self.edge_size/2), # Top
            (self.coords[0] + self.edge_size/2 * math.sqrt(3), self.coords[1]), # Right
            (self.coords[0], self.coords[1] + self.edge_size/2), # Bottom
            (self.coords[0] - self.edge_size/2 * math.sqrt(3), self.coords[1]) # Left
        ]

        pygame.draw.polygon(screen, self.color, self.polygon)
    
    def movement(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.y += 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.y -= 1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.x -= 1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.x += 1
                