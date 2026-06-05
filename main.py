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

font = pygame.font.SysFont("Courier", 20, True)

# Game loop
running = True
while running:
    # background color
    screen.fill("white")

    top_side = font.render(f'Your top side : {dice.top}', True, (128, 128, 128))
    screen.blit(top_side, (20, 20))
    required_side = font.render(f'Required side : {solution_face}', True, (128, 128, 128))
    screen.blit(required_side, (20, 50))

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
                        solution_giver(dice)

    pressed = pygame.key.get_pressed()
    for tile in tiles:
        tile.draw(screen, offset)
        # Tiles should be generated everytime the player reaches the end
        if tile.type == 'end' and (tile.x, tile.y, tile.z) == (dice.x, dice.y, dice.z):
            tile.generate_tiles(30, dice, tiles, occupied_coords, solution_path)
            solution_giver(dice)
        

    dice.draw(screen, offset)
    #cube.movement()

    # update display
    pygame.display.update()