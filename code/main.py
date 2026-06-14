# initialize pygame
import pygame
pygame.init()
# initialize sound mixer
pygame.mixer.init()

# Screen configurations
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Dice it - Game")
pygame.display.set_icon(pygame.image.load('assets/dice/icon.ico'))

# additional libraries
import random

# import classes from files
from classes.tile import Tile
from classes.cube import Cube
from classes.stars import Stars
from classes.buttons import Buttons

# Cube
dice = Cube(0, 0, 0)

# offset camera
offset = [0,0]

# Tiles

occupied_coords = [] # Keeps track of the coordinates of each tile

# Tile list
tiles = [Tile(0, 0, 0, occupied_coords),
     Tile(0, 1, 0, occupied_coords),
     Tile(1, 0, 0, occupied_coords),
     Tile(1, 1, 0, occupied_coords),
     Tile(0, -1, 0, occupied_coords),
     Tile(-1, 1, 0, occupied_coords),
     Tile(-1, -1, 0, occupied_coords),
     Tile(-1, 0, 0, occupied_coords),
     Tile(1, -1, 0, occupied_coords)]

# Decoration stars list
stars = []

# Score system
level_no = 1

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
def next_level(tile, dice = dice):
    global level_type

    possible_levels = ['normal', 'broken_tiles']
    tile.generate_tiles(30, dice, tiles, occupied_coords, solution_path)

    # If it is possible to make a level of locked_tiles, we add it to possible levels
    if tile.can_generate_locked_tiles(tiles, occupied_coords):
        possible_levels.append('locked_tiles')

    # Choose the level randomly
    level_type = random.choice(possible_levels)

    # Handles the tile type changes and in general, sets the level
    tile.level_setter(tiles, occupied_coords, level_type)
    
    # Once the level is generated, the required face is calculated
    solution_giver(dice)


# Game timer
timer = 0

# Handles the font of the game
font = pygame.font.SysFont("Courier", 20, True)

# just a small watermark
author_text = font.render("Made by : Rishabh Saxena", True, (255, 255, 255))

# Pygame clock
clock = pygame.time.Clock()

# All the images required to load
background_img = pygame.transform.smoothscale(pygame.image.load('assets/background.jpg'), (800, 600))
dice_it_logo = pygame.transform.smoothscale(pygame.image.load('assets/Dice_it_logo.png'), (510,280))
# Displays when pressed How to play button
how_to_play_img = pygame.transform.smoothscale(pygame.image.load('assets/How_to_play.png'), (387, 440))

# Game state sounds
end_sound = pygame.mixer.Sound("assets/sound effects/end_level.wav")
end_sound.set_volume(0.5)
lost_sound = pygame.mixer.Sound("assets/sound effects/lost.wav")
lost_sound.set_volume(0.5)

# Menu buttons
start_button = Buttons(200, 270, 'START', True)
quit_button = Buttons(600, 500, 'QUIT', True)
how_to_play_button = Buttons(420, 270, 'HOW TO PLAY', True)

# How to play screen button
close_htp_button = Buttons(550, 500, "CLOSE", True)

# UI texts (shown during gameplay)
required_number_text = Buttons(270, 50, "Required no. : ", False)
timer_text = Buttons(20, 50, "Timer : ", False)
level_text = Buttons(600, 50, "Level : ", False)

# lost screen texts and buttons
you_lost_text = Buttons (320, 80, 'GAME OVER', False, (255, 0, 0))
your_score_text = Buttons(290, 150, 'Your score : ', False)
# Restart button to play again
restart_button = Buttons(570, 500, "RESTART", True)
# Back to main menu
back_to_menu_button = Buttons(50, 500, "Back to main menu", True)
# Give solution button
solution_button = Buttons(350, 500, "GIVE SOLUTION", True)
# a variable that ensures if the solution should be shown or not
show_solution = False

# Game loop
running = True
while running:
    # background image
    screen.blit(background_img, (0, 0))

    # Add decorative stars
    if len(stars) < 30:
        vel = random.randint(1, 3)
        stars.append(Stars(vel, vel))

    # Stars functions
    for star in stars[:]:
        star.draw(screen)
        star.movement()
        # if the star is out of screen, remove it
        if star.x < 0 or star.x > 800 or star.y < 0 or star.y > 600:
            stars.remove(star)

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
            level_no += 1
            timer += 15
            end_sound.play()
        # locked tile function
        if level_type == 'locked_tiles' : 
            tile.locked_tile(dice, tiles, locked_tile_number, screen, font)

    # Dice drawing
    dice.draw(screen, offset)


    # When gamestate is 'menu' (mainly to draw)
    if game_state == 'menu':
        # Display game logo
        screen.blit(dice_it_logo, (400 - dice_it_logo.get_width()//2, 20))
        # Draw the buttons
        start_button.draw(screen)
        quit_button.draw(screen)
        how_to_play_button.draw(screen)
        # show watermark
        screen.blit(author_text, (10, 580))

    # How to play screen
    if game_state == 'htp':
        screen.blit(how_to_play_img, (400 - how_to_play_img.get_width()//2, 250 - how_to_play_img.get_height()//2))
        close_htp_button.draw(screen)

    # Gamestate play functions
    if game_state == 'play': 

        # Text elements (update with the game)
        required_number_text.draw(screen)
        required_number_text.text = f'Required no. : {solution_face}'
        timer_text.draw(screen)
        timer_text.text = f'Time left : {int(timer)}'
        level_text.draw(screen)
        level_text.text = f'Level : {level_no}'

        # Changes the timer color when less than 10 to warn the player
        if timer <= 10:
            timer_text.text_color = (255, 0, 0)
        else :
            timer_text.text_color = (255, 255, 255)

        # Timer working when game_state is 'play'
        timer -= 0.02
        if timer <= 0:
            # Game lost if hit 0
            game_state = 'lost'
            lost_sound.play()

        
        # if the player has no more directions to go to, he loses (mostly in broken tile maps)
        if (dice.x + 1, dice.y, dice.z) not in occupied_coords and (dice.x, dice.y + 1, dice.z) not in occupied_coords and (dice.x - 1, dice.y, dice.z) not in occupied_coords and (dice.x, dice.y - 1, dice.z) not in occupied_coords:
            if (dice.x, dice.y) == (tiles[-1].x, tiles[-1].y) and dice.top != solution_face:
                game_state = 'lost'
            if (dice.x, dice.y) != (tiles[-1].x, tiles[-1].y):
                game_state = 'lost'
                
    # Shown when game over
    if game_state == 'lost':
            you_lost_text.draw(screen)
            your_score_text.draw(screen)
            # Shows your score
            your_score_text.text = f'Your score : {level_no}'
            back_to_menu_button.draw(screen)
            restart_button.draw(screen)
            solution_button.draw(screen)

            

    # Event catching loop
    for event in pygame.event.get():
        # Event type is quit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Dice movement over all the tiles
            if game_state == 'play':
                dice.movement(event, tiles, occupied_coords, offset)

        # Button functions when game state is menu
        if game_state == 'menu':
            start_button.clickable_func(event)
            quit_button.clickable_func(event)
            how_to_play_button.clickable_func(event)
            # If start button is pressed, start the game
            if start_button.status:
                game_state = 'play'
                next_level(tiles[0])
                locked_tile_number = tiles[0].locked_tile_number(dice, tiles, solution_path)
                level_no = 1
                timer = 16     
                # reset the button to false status
                start_button.status = False
            # To quit the game
            if quit_button.status :
                running = False
            # To show the How to play instructions
            if how_to_play_button.status:
                game_state = 'htp'
                how_to_play_button.status = False

        # When how to play instructions are shown
        if game_state == 'htp':
            # To close and go back to main menu
            close_htp_button.clickable_func(event)
            if close_htp_button.status:
                game_state = 'menu'
                close_htp_button.status = False

        # When game is over
        if game_state == 'lost':
            back_to_menu_button.clickable_func(event)
            restart_button.clickable_func(event)
            solution_button.clickable_func(event)

            # On pressing back to menu button, reset the tiles list, dice position, offset, occupied coords and solution path 
            if back_to_menu_button.status:
                game_state = 'menu'
                dice.x, dice.y = 0, 0
                offset[0], offset[1] = 0, 0
                occupied_coords.clear()
                solution_path.clear()
                tiles = [Tile(0, 0, 0, occupied_coords),
                         Tile(0, 1, 0, occupied_coords),
                         Tile(1, 0, 0, occupied_coords),
                         Tile(1, 1, 0, occupied_coords),
                         Tile(0, -1, 0, occupied_coords),
                         Tile(-1, 1, 0, occupied_coords),
                         Tile(-1, -1, 0, occupied_coords),
                         Tile(-1, 0, 0, occupied_coords),
                         Tile(1, -1, 0, occupied_coords)]

                back_to_menu_button.status = False
                # hide the solution when back to menu button is pressed
                show_solution = False
            # On pressing restart button, restart the game
            if restart_button.status:
                game_state = 'play'
                next_level(tiles[0])
                locked_tile_number = tiles[0].locked_tile_number(dice, tiles, solution_path)
                level_no = 1
                timer = 21      
                restart_button.status = False
                # Hide solution 
                show_solution = False
            # when give solution button is pressed, show solution
            if solution_button.status:
                show_solution = True
                solution_button.status = False
    
    # Writes down the solution of that level on pressing show solution
    if show_solution:
        for i in range(1, len(solution_path) + 1):
            if i <= 15:
                screen.blit(font.render(solution_path[i-1].capitalize(), True, (255, 255, 255)), (610, 20*i))

            # Divided into 2 columns
            else:
                screen.blit(font.render(solution_path[i-1].capitalize(), True, (255, 255, 255)), (700, 20*(i-15)))

    # set the game fps to 60
    clock.tick(60)

    # update display
    pygame.display.update()