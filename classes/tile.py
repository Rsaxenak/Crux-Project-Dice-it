import pygame
import math

class Tile:
    def __init__(self, x, y, z):
        # the 'x,y,z' coordinates of the game
        self.x, self.y = x, y
        self.z = z

        # the actual coordinates on screen
        self.coords = (400 + self.y * 17.5 * math.sqrt(3) + self.x * 17.5 * math.sqrt(3), 
                       400 - self.y * 17.5 + self.x * 17.5)

        self.color = (128, 128, 128)

        self.edge_size = 30 # Actual size of edge, not isometrically

    def draw(self, screen):
        self.polygon = [
            (self.coords[0], self.coords[1] - self.edge_size/2), # Top
            (self.coords[0] + self.edge_size/2 * math.sqrt(3), self.coords[1]), # Right
            (self.coords[0], self.coords[1] + self.edge_size/2), # Bottom
            (self.coords[0] - self.edge_size/2 * math.sqrt(3), self.coords[1]) # Left
        ]

        pygame.draw.polygon(screen, self.color, self.polygon)