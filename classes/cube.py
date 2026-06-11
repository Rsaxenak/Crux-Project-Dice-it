import pygame
import math

# Load all the cube faces
cube_face_images = {
    1 : pygame.transform.smoothscale(pygame.image.load('assets/dice/1.png'), (31, 25.5)),
    2 : pygame.transform.smoothscale(pygame.image.load('assets/dice/2.png'), (31, 25.5)),
    3 : pygame.transform.smoothscale(pygame.image.load('assets/dice/3.png'), (31, 25.5)),
    4 : pygame.transform.smoothscale(pygame.image.load('assets/dice/4.png'), (31, 25.5)),
    5 : pygame.transform.smoothscale(pygame.image.load('assets/dice/5.png'), (31, 25.5)),
    6 : pygame.transform.smoothscale(pygame.image.load('assets/dice/6.png'), (31, 25.5))
}

class Cube:

    def __init__(self, x, y, z):
        # Game coords
        self.x = x
        self.y = y
        self.z = z

        # Faces 
        self.top = 1
        self.bottom = 6
        self.front = 2
        self.back = 5
        self.left = 4
        self.right = 3

        # Load the base image of dice
        self.base_img = pygame.transform.smoothscale(pygame.image.load('assets/dice/base_redone.png'), (68, 51))
        # Intialize the image variables
        self.top_img = cube_face_images[self.top].copy()
        self.front_img = cube_face_images[self.front].copy()
        self.right_img = cube_face_images[self.right].copy()

        # For the tile on which dice stays
        self.color = (255, 0, 0)
        self.edge_size = 30

    def draw(self, screen, offset):


        # Draws a red color tile which is the dice position
        self.coords = (400 + (self.y- offset[1]) * 17.5 * math.sqrt(3) + (self.x - offset[0]) * 17.5 * math.sqrt(3), 
                       400 - (self.y - offset[1]) * 17.5 + (self.x - offset[0]) * 17.5)

        self.polygon = [
            (self.coords[0], self.coords[1] - self.edge_size/2), # Top
            (self.coords[0] + self.edge_size/2 * math.sqrt(3), self.coords[1]), # Right
            (self.coords[0], self.coords[1] + self.edge_size/2), # Bottom
            (self.coords[0] - self.edge_size/2 * math.sqrt(3), self.coords[1]) # Left
        ]

        pygame.draw.polygon(screen, self.color, self.polygon)     

        # Draw the base image on the top of the tile
        screen.blit(self.base_img, (self.coords[0] - self.base_img.get_width()//2, self.coords[1] - self.base_img.get_height()//2 - 10))

        # Set the visible faces' images as per the dice orientation 
        self.top_img = cube_face_images[self.top].copy()

        self.front_img = pygame.transform.rotate(cube_face_images[self.front].copy(), 60)
        self.front_img = pygame.transform.flip(self.front_img, True, False)
        self.right_img = pygame.transform.rotate(cube_face_images[self.right].copy(), -120)

        # Function that handles the orientation (rotation) according to dice movement
        self.orientation_corrector()

        # Display all the face images on top of base
        screen.blit(self.top_img, (self.coords[0] - self.top_img.get_width()//2 - 1, self.coords[1] - self.top_img.get_height()//2 - 20))        
        screen.blit(self.front_img, (self.coords[0] - self.front_img.get_width()//2 - 12, self.coords[1] - self.front_img.get_height()//2 - 4))
        screen.blit(self.right_img, (self.coords[0] - self.right_img.get_width()//2 + 10, self.coords[1] - self.right_img.get_height()//2 - 4))

    
    def movement(self, event, tile_list, occupied_tiles, offset):

        # movement of dice, which requires a tile to be in occupied tiles (to exist) and is restricted if encountered a locked tile

        if event.key in (pygame.K_w, pygame.K_UP) and (self.x, self.y + 1, self.z) in occupied_tiles:
            tile_coords = (self.x, self.y + 1, self.z)

            if tile_list[occupied_tiles.index(tile_coords)].type != 'locker':
                self.y += 1
                offset[1] += 1
                self.side_move('up')

        if event.key in (pygame.K_s, pygame.K_DOWN) and (self.x, self.y - 1, self.z) in occupied_tiles:
            tile_coords = (self.x, self.y - 1, self.z)

            if tile_list[occupied_tiles.index(tile_coords)].type != 'locker':
                self.y -= 1
                offset[1] -= 1
                self.side_move('down')
        if event.key in (pygame.K_a, pygame.K_LEFT) and (self.x - 1, self.y, self.z) in occupied_tiles:
            tile_coords = (self.x - 1, self.y, self.z)

            if tile_list[occupied_tiles.index(tile_coords)].type != 'locker':
                self.x -= 1
                offset[0] -= 1
                self.side_move('left')
        if event.key in (pygame.K_d, pygame.K_RIGHT) and (self.x + 1, self.y, self.z) in occupied_tiles:
            tile_coords = (self.x + 1, self.y, self.z)

            if tile_list[occupied_tiles.index(tile_coords)].type != 'locker':
                self.x += 1
                offset[0] += 1
                self.side_move('right')

        
    # Function that takes care of dice orientations
    def side_move(self, direction):
        if direction == 'up':
            self.top, self.bottom, self.front, self.back = self.front, self.back, self.bottom, self.top
        if direction == 'down':
            self.top, self.bottom, self.front, self.back = self.back, self.front, self.top, self.bottom
        if direction == 'left':
            self.top, self.bottom, self.left, self.right = self.right, self.left, self.top, self.bottom
        if direction == 'right':
            self.top, self.bottom, self.left, self.right = self.left, self.right, self.bottom, self.top
   
    def orientation_corrector(self):
        # 1, 4, 5 can be skipped since they are symmetric

        # For the top face
        if self.top == 2  and (self.front + self.right)%2 == 0 : 
            self.top_img = pygame.transform.flip(self.top_img, True, False)
        if self.top == 3 and (self.front + self.right) % 2 == 0:
            self.top_img = pygame.transform.smoothscale(pygame.transform.rotate(self.top_img, 90), (31, 21.5))
        if self.top == 6 and (self.front + self.right) % 2 == 1: 
            self.top_img = pygame.transform.flip(self.top_img, True, False)

        # For the front face
        if self.front == 2 and (self.top + self.right) % 2 == 1:
            self.front_img = pygame.transform.flip(pygame.transform.rotate(self.front_img, 120), True, False)
        if self.front == 3 and (self.top + self.right) % 2 == 0:
            self.front_img = pygame.transform.rotate(pygame.transform.smoothscale(self.front_img, (45, 19.5)), 70)
        if self.front == 6 and (self.top + self.right) % 2 == 0:
            self.front_img = pygame.transform.flip(pygame.transform.rotate(self.front_img, 120), True, False)

        # For the right face
        if self.right == 2 and (self.top + self.front) % 2 == 0:
            self.right_img = pygame.transform.flip(pygame.transform.rotate(self.right_img, 60), False, True)
        if self.right == 3 and (self.top + self.front) % 2 == 0:
            self.right_img = pygame.transform.rotate(pygame.transform.smoothscale(self.right_img, (45, 21.5)), 120)
        if self.right == 6 and (self.top + self.front) % 2 == 1:
            self.right_img = pygame.transform.flip(pygame.transform.rotate(self.right_img, 55), False, True)
            
        