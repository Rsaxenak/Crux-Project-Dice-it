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

# offset camera
offset = [0,0]

# Tiles
occupied_coords = []
tiles = [
     Tile(0, 0, 0, occupied_coords),
     Tile(0, 1, 0, occupied_coords),
     Tile(1, 0, 0, occupied_coords),
     Tile(1, 1, 0, occupied_coords)
]

solution_path = []

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
                # Dice movement over all the tiles
                dice.movement(event, occupied_coords, offset)

                # Generate new tiles
                if event.key == pygame.K_g:
                    for tile in tiles:
                        tile.generate_tiles(30, dice, tiles, occupied_coords, solution_path)

    pressed = pygame.key.get_pressed()
    for tile in tiles:
        tile.draw(screen, offset)
        # Tiles should be generated everytime the player reaches the end
        if tile.type == 'end' and (tile.x, tile.y, tile.z) == (dice.x, dice.y, dice.z):
            tile.generate_tiles(30, dice, tiles, occupied_coords, solution_path)
            print(solution_path)
        

    dice.draw(screen, offset)
    #cube.movement()

    # update display
    pygame.display.update()