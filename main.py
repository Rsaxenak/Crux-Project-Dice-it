# initialize pygame
import pygame
pygame.init()

# additional libraries
import random

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

# Score system
score = 0

# Level types
level_type = 'normal'

# Solution path and required face
solution_path = []
solution_face = 0

def solution_giver(cube, solution_way = solution_path):
    global solution_face
    cube_sides = {'top':cube.top,
                  'bottom': cube.bottom,
                  'left': cube.left,
                  'right': cube.right,
                  'front': cube.front,
                  'back': cube.back}
    for direction in solution_way:
        if direction == 'up':
            cube_sides['top'], cube_sides['bottom'], cube_sides['front'], cube_sides['back'] = cube_sides['front'], cube_sides['back'], cube_sides['bottom'], cube_sides['top']
        if direction == 'down':
            cube_sides['top'], cube_sides['bottom'], cube_sides['front'], cube_sides['back'] = cube_sides['back'], cube_sides['front'], cube_sides['top'], cube_sides['bottom']
        if direction == 'left':
            cube_sides['top'], cube_sides['bottom'], cube_sides['left'], cube_sides['right'] = cube_sides['right'], cube_sides['left'], cube_sides['top'], cube_sides['bottom']
        if direction == 'right':
            cube_sides['top'], cube_sides['bottom'], cube_sides['left'], cube_sides['right'] = cube_sides['left'], cube_sides['right'], cube_sides['bottom'], cube_sides['top']

    solution_face = cube_sides['top']

# Next level generator

def next_level(tile, dice = dice, tiles = tiles, occupied_path = occupied_coords, solution_path = solution_path):
    global level_type

    possible_levels = ['normal', 'broken_tiles']
    tile.generate_tiles(30, dice, tiles, occupied_path, solution_path)

    if tile.can_generate_locked_tiles(tiles, occupied_path):
        possible_levels.append('locked_tiles')

    level_type = random.choice(possible_levels)

    tile.level_setter(tiles, occupied_path, level_type)
    
    solution_giver(dice)

    print(level_type)

font = pygame.font.SysFont("Courier", 20, True)

# Game loop
running = True
while running:
    # background color
    screen.fill("white")

    # All the text shown in the game
    top_side = font.render(f'Your top side : {dice.top}', True, (128, 128, 128))
    screen.blit(top_side, (20, 20))
    required_side = font.render(f'Required side : {solution_face}', True, (128, 128, 128))
    screen.blit(required_side, (20, 50))
    score_text = font.render(f'Score : {score}', True, (128, 128, 128))
    screen.blit(score_text, (20, 60))

    # Event catching loop
    for event in pygame.event.get():
        # Event type is quit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                # Dice movement over all the tiles
                dice.movement(event, tiles, occupied_coords, offset)

                # Generate new tiles
                if event.key == pygame.K_g:
                        next_level(tiles[0])
                        locked_tile_number = tiles[0].locked_tile_number(dice, tiles, solution_path)
                        score = 0

    pressed = pygame.key.get_pressed()
    for tile in tiles:
        tile.draw(screen, offset)
        tile.broken_tiles(dice, tiles, occupied_coords)
        # Tiles should be generated everytime the player reaches the end
        if tile.type == 'end' and (tile.x, tile.y, tile.z) == (dice.x, dice.y, dice.z) and solution_face == dice.top:
            next_level(tile)
            locked_tile_number = tile.locked_tile_number(dice, tiles, solution_path)
            score+=1
        if level_type == 'locked_tiles' : tile.locked_tile(dice, tiles, locked_tile_number)
    

    # set the game fps to 60
    pygame.time.Clock().tick(60)

    dice.draw(screen, offset)
    #cube.movement()

    # update display
    pygame.display.update()