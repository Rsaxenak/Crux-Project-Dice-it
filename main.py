# initialize pygame
import pygame
pygame.init()

# import classes from files
from classes.tile import Tile
from classes.cube import Cube

# Screen configurations
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Cube
dice = Cube(0, 0, 0)

# Tiles
Tiles = []
tile_1 = Tile(0, 0, 0)

# Game loop
running = True
while running:
    # background color
    screen.fill("white")

    # Event catching loop
    for event in pygame.event.get():
        # Event type is quit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    dice.y += 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    dice.y -= 1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    dice.x -= 1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    dice.x += 1
    
    tile_1.draw(screen)

    dice.draw(screen)
    #cube.movement()

    # update display
    pygame.display.update()