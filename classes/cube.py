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

    def draw(self, screen, offset):
        self.coords = (400 + (self.y- offset[1]) * 17.5 * math.sqrt(3) + (self.x - offset[0]) * 17.5 * math.sqrt(3), 
                       400 - (self.y - offset[1]) * 17.5 + (self.x - offset[0]) * 17.5)
        self.polygon = [
            (self.coords[0], self.coords[1] - self.edge_size/2), # Top
            (self.coords[0] + self.edge_size/2 * math.sqrt(3), self.coords[1]), # Right
            (self.coords[0], self.coords[1] + self.edge_size/2), # Bottom
            (self.coords[0] - self.edge_size/2 * math.sqrt(3), self.coords[1]) # Left
        ]

        pygame.draw.polygon(screen, self.color, self.polygon)
    
    def movement(self, event, occupied_tiles, offset):
        if event.key in (pygame.K_w, pygame.K_UP) and (self.x, self.y + 1, self.z) in occupied_tiles:
            self.y += 1
            offset[1] += 1
        if event.key in (pygame.K_s, pygame.K_DOWN) and (self.x, self.y - 1, self.z) in occupied_tiles:
            self.y -= 1
            offset[1] -= 1
        if event.key in (pygame.K_a, pygame.K_LEFT) and (self.x - 1, self.y, self.z) in occupied_tiles:
            self.x -= 1
            offset[0] -= 1
        if event.key in (pygame.K_d, pygame.K_RIGHT) and (self.x + 1, self.y, self.z) in occupied_tiles:
            self.x += 1
            offset[0] += 1
        

                