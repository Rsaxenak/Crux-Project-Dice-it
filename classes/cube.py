import pygame
import math

class Cube:

    def __init__(self, x, y, z):
        # Game coords
        self.x = x
        self.y = y
        self.z = z

        self.top = 1
        self.bottom = 6
        self.front = 2
        self.back = 5
        self.left = 4
        self.right = 3

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
            self.side_move('up')
        if event.key in (pygame.K_s, pygame.K_DOWN) and (self.x, self.y - 1, self.z) in occupied_tiles:
            self.y -= 1
            offset[1] -= 1
            self.side_move('down')
        if event.key in (pygame.K_a, pygame.K_LEFT) and (self.x - 1, self.y, self.z) in occupied_tiles:
            self.x -= 1
            offset[0] -= 1
            self.side_move('left')
        if event.key in (pygame.K_d, pygame.K_RIGHT) and (self.x + 1, self.y, self.z) in occupied_tiles:
            self.x += 1
            offset[0] += 1
            self.side_move('right')
        
    def side_move(self, direction):
        if direction == 'up':
            self.top, self.bottom, self.front, self.back = self.front, self.back, self.bottom, self.top
        if direction == 'down':
            self.top, self.bottom, self.front, self.back = self.back, self.front, self.top, self.bottom
        if direction == 'left':
            self.top, self.bottom, self.left, self.right = self.right, self.left, self.top, self.bottom
        if direction == 'right':
            self.top, self.bottom, self.left, self.right = self.left, self.right, self.bottom, self.top
   