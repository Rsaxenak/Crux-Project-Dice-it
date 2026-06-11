# initialize pygame
import pygame
pygame.init()

# Screen configurations
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# additional libraries
import random

# import classes from files
from classes.tile import Tile
from classes.cube import Cube



# Cube
dice = Cube(0, 0, 0)

# offset camera
offset = [0,0]

# Tiles

occupied_coords = [] # Keeps track of the coordinates of each tile
tiles = [
     Tile(0, 0, 0, occupied_coords),
     Tile(0, 1, 0, occupied_coords),
     Tile(1, 0, 0, occupied_coords),
     Tile(1, 1, 0, occupied_coords),
     Tile(0, -1, 0, occupied_coords),
     Tile(-1, 1, 0, occupied_coords),
     Tile(-1, -1, 0, occupied_coords),
     Tile(-1, 0, 0, occupied_coords),
     Tile(1, -1, 0, occupied_coords)
] # A whole tile list (with some starter tiles)

# Score system
score = 0

# Gamestate
game_state = 'menu'

# Level types
level_type = 'normal'

# Solution path and required face
solution_path = []
solution_face = 0 

# Function that finds the required face for a given level
def solution_giver(cube, solution_way = solution_path):
    global solution_face

    # A replica of the dice faces
    cube_sides = {'top':cube.top,
                  'bottom': cube.bottom,
                  'left': cube.left,
                  'right': cube.right,
                  'front': cube.front,
                  'back': cube.back}
    
    # The faces change according to the direction in solution_path
    for direction in solution_way:
        if direction == 'up':
            cube_sides['top'], cube_sides['bottom'], cube_sides['front'], cube_sides['back'] = cube_sides['front'], cube_sides['back'], cube_sides['bottom'], cube_sides['top']
        if direction == 'down':
            cube_sides['top'], cube_sides['bottom'], cube_sides['front'], cube_sides['back'] = cube_sides['back'], cube_sides['front'], cube_sides['top'], cube_sides['bottom']
        if direction == 'left':
            cube_sides['top'], cube_sides['bottom'], cube_sides['left'], cube_sides['right'] = cube_sides['right'], cube_sides['left'], cube_sides['top'], cube_sides['bottom']
        if direction == 'right':
            cube_sides['top'], cube_sides['bottom'], cube_sides['left'], cube_sides['right'] = cube_sides['left'], cube_sides['right'], cube_sides['bottom'], cube_sides['top']

    # Once all done, the solution face stores the top face
    solution_face = cube_sides['top']

# Next level generator
def next_level(tile, dice = dice, tiles = tiles, occupied_path = occupied_coords, solution_path = solution_path):
    global level_type


    possible_levels = ['normal', 'broken_tiles']
    tile.generate_tiles(30, dice, tiles, occupied_path, solution_path)

    # If it is possible to make a level of locked_tiles, we add it to possible levels
    if tile.can_generate_locked_tiles(tiles, occupied_path):
        possible_levels.append('locked_tiles')

    # Choose the level randomly
    level_type = random.choice(possible_levels)

    # Handles the tile type changes and in general, sets the level
    tile.level_setter(tiles, occupied_path, level_type)
    
    # Once the level is generated, the required face is calculated
    solution_giver(dice)

    print(level_type)

# Game timer
timer = 0

# Handles the font of the game
font = pygame.font.SysFont("Courier", 20, True)

# Pygame clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # background color
    screen.fill("white")

    # All the text shown in the game: -

    # Dice top side
    top_side = font.render(f'Your top side : {dice.top}', True, (128, 128, 128))
    screen.blit(top_side, (20, 20))
    # Required top side
    required_side = font.render(f'Required side : {solution_face}', True, (128, 128, 128))
    screen.blit(required_side, (20, 50))
    # Score 
    score_text = font.render(f'Score : {score}', True, (128, 128, 128))
    screen.blit(score_text, (20, 80))
    # Timer
    timer_text = font.render(f'Timer : {int(timer)}', True, (128, 128, 128))
    screen.blit(timer_text, (20, 110))
    # Lost text
    you_lost_text = font.render(f'You lost. Press G to play again', True, (128, 128, 128))
    if game_state == 'lost':
        screen.blit(you_lost_text, (160, 100))
    # Shows the level type
    level_type_text = font.render(level_type.capitalize(), True, (128, 128, 128))
    screen.blit(level_type_text, (600, 20))
    

    # Event catching loop
    for event in pygame.event.get():
        # Event type is quit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Dice movement over all the tiles
            if game_state == 'play':
                dice.movement(event, tiles, occupied_coords, offset)

            # Restart the game
            if event.key == pygame.K_g:
                if game_state != 'play': game_state = 'play'
                # Generate new tiles
                next_level(tiles[0])
                locked_tile_number = tiles[0].locked_tile_number(dice, tiles, solution_path)
                score = 0
                timer = 16

    # Tile handling functions
    for tile in tiles[:]:
        # Draw tiles
        tile.draw(screen, offset)
        # Function for broken tiles
        if level_type == 'broken_tiles': tile.broken_tiles(dice, tiles, occupied_coords)
        # Tiles should be generated everytime the player reaches the end
        if tile.type == 'end' and (tile.x, tile.y, tile.z) == (dice.x, dice.y, dice.z) and solution_face == dice.top:
            next_level(tile)
            locked_tile_number = tile.locked_tile_number(dice, tiles, solution_path)
            score += 1
            timer += 10
        if level_type == 'locked_tiles' : 
            tile.locked_tile(dice, tiles, locked_tile_number, screen, font)


    # set the game fps to 60
    clock.tick(60)

    # Timer working when game_state is 'play'
    if game_state == 'play': 
        timer -= 0.02
        if timer <= 0:
            # Game lost if hit 0
            game_state = 'lost'

    # Dice drawing
    dice.draw(screen, offset)

    # update display
    pygame.display.update()