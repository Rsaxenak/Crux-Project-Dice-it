import pygame
import math
import random

# Dictionary to load and store all the images
tile_images = {'normal' : pygame.transform.smoothscale(
                    pygame.image.load('assets/tiles/normal_tile.png').convert_alpha(), (63, 48)),
               'broken' : pygame.transform.smoothscale(
                    pygame.image.load('assets/tiles/broken_tile.png').convert_alpha(), (63, 48)),
               'locked' : pygame.transform.smoothscale(
                    pygame.image.load('assets/tiles/locked_tile.png').convert_alpha(), (63, 48)),
                'locker' : pygame.transform.smoothscale(
                    pygame.image.load('assets/tiles/locker_tile.png').convert_alpha(), (63, 48)),
               'end' : pygame.transform.smoothscale(
                    pygame.image.load('assets/tiles/end_tile.png').convert_alpha(), (63, 48))}


class Tile:
    def __init__(self, x, y, z, occupied_list):
        # the 'x,y,z' coordinates of the game
        self.x, self.y = x, y
        self.z = z

        
        self.coords = (0, 0)
        # To control transparency
        self.alpha = 255

        # Tile of type is initially set to normal, which can be later changed to broken or locked
        self.type = 'normal'

        # To check if a tile has been stepped on already
        self.stepped_on = 0

        # Adds the tiles coordinates to the occupied list
        occupied_list.append((x, y, z))


    def draw(self, screen, offset):

        # Updates the actual coordinates on the screen according to movement
        self.coords = (400 + (self.y - offset[1]) * 17.5 * math.sqrt(3) + (self.x - offset[0]) * 17.5 * math.sqrt(3), 
                       400 - (self.y - offset[1]) * 17.5 + (self.x - offset[0]) * 17.5)
        

        # Handles image assignment based on type
        if self.type == 'normal' or self.type == 'unlocked':
            self.image = tile_images['normal'].copy()
        if self.type == 'broken':
            self.image = tile_images['broken'].copy()
        if self.type == 'locker':
            self.image = tile_images['locked'].copy()
        if self.type == 'end':
            self.image = tile_images['end'].copy()
        if self.type == 'locked':
            self.image = tile_images['locker'].copy()
        
        # Especially for broken tiles
        self.image.set_alpha(self.alpha)
        
        # Display the image on screen
        screen.blit(self.image, (self.coords[0] - tile_images['normal'].get_width()//2, self.coords[1] - tile_images['normal'].get_height()//2))


    # Handles tile generation
    def generate_tiles(self, n, cube, tile_list, occupied_list, solution_path):
        
        # Create a shallow copy to iterate over a list
        copy_of_tile_list = [el for el in tile_list]
        # Remove all elements of solution path of the previous level
        solution_path.clear()


        for el in copy_of_tile_list:
            #Remove all the tiles from tile list except the tile on which player lands
            if (el.x, el.y, el.z) != (cube.x, cube.y, cube.z): 
                tile_list.remove(el)
                occupied_list.remove((el.x, el.y, el.z))
        #print(occupied_list)

        # To get the start tile
        start_tile = tile_list[0]
        # Change the tile type from 'end' to 'normal'
        start_tile.type = 'normal'

        for i in range(0, n):
            # To find all the directions in which we can add a tile
            available_directions = []
            tile = tile_list[-1]

            # If left is available
            if (tile.x - 1, tile.y, tile.z) not in occupied_list:
                available_directions.append((tile.x - 1, tile.y, tile.z))
            # Right
            if (tile.x + 1, tile.y, tile.z) not in occupied_list:
                available_directions.append((tile.x + 1, tile.y, tile.z))
            # Down
            if (tile.x, tile.y - 1, tile.z) not in occupied_list:
                available_directions.append((tile.x, tile.y - 1, tile.z))
            # Up
            if (tile.x, tile.y + 1, tile.z) not in occupied_list:
                available_directions.append((tile.x, tile.y + 1, tile.z))

            # If there are any directions available to add a tile, add it
            if available_directions:
                new_tile_coords = random.choice(available_directions)

                # Direction identifier
                direction = 'up' if new_tile_coords == (tile.x, tile.y + 1, tile.z) else 'down' if new_tile_coords == (tile.x, tile.y - 1, tile.z) else 'left' if new_tile_coords == (tile.x - 1, tile.y, tile.z) else 'right'

                tile_list.append(Tile(new_tile_coords[0], new_tile_coords[1], new_tile_coords[2], occupied_list))
                solution_path.append(direction)
            # If no such direction exists anymore, remove it
            else :
                break
        
        # To find the end_tile
        end_tile = tile_list[-1]
        end_tile.type = 'end'


    # Handles the changing of tiles based on the level
    def level_setter(self, tile_list, occupied_list, level_type):
        if level_type == 'broken_tiles':
            for tile in tile_list:
                if tile == tile_list[0] : continue # Skip the start tile
                # 36% chance the tile would be a broken tile
                selector = random.randint(1, 10)
                if selector in range(1, 3) and tile.type != 'end':
                    tile.type = 'broken'

        if level_type == 'locked_tiles':
            available_tiles = [] # Create a list of available tiles, to choose which one should be locked

            for tile in tile_list:

                # Skip the start and end tile
                if tile == tile_list[0] or tile.type == 'end' or tile == tile_list[-2]: continue

                # If the right and left tiles are the only tiles for a specific tile (to prevent a locked door with a open window right beside it)
                if (tile.x - 1, tile.y, tile.z) in occupied_list and (tile.x + 1, tile.y, tile.z) in occupied_list:
                    if (tile.x, tile.y - 1, tile.z) not in occupied_list and (tile.x, tile.y + 1, tile.z) not in occupied_list:
                        available_tiles.append(tile)
                # If the up and down tiles are the only tiles
                elif (tile.x, tile.y - 1, tile.z) in occupied_list and (tile.x, tile.y + 1, tile.z) in occupied_list:
                    if (tile.x - 1, tile.y, tile.z) not in occupied_list and (tile.x + 1, tile.y, tile.z) not in occupied_list:
                        available_tiles.append(tile)

            # If there are any available tiles, we make a random choice and change that tile to a locked tile
            if available_tiles:
                locked_tile = random.choice(available_tiles)
                locked_tile.type = 'locked'

                # A locker tile, which helps indicate that the previous tile is locked
                for i in range(0, len(tile_list) - 1):
                    if tile_list[i].type == 'locked':
                        tile_list[i+1].type = 'locker'
                


    # A function to ensure the level can be made a locked level
    def can_generate_locked_tiles(self, tile_list, occupied_list):
        available_tiles = []

        for tile in tile_list:

            if tile == tile_list[0] : continue

            if (tile.x - 1, tile.y, tile.z) in occupied_list and (tile.x + 1, tile.y, tile.z) in occupied_list:
                if (tile.x, tile.y - 1, tile.z) not in occupied_list and (tile.x, tile.y + 1, tile.z) not in occupied_list:
                    available_tiles.append(tile)
            elif (tile.x, tile.y - 1, tile.z) in occupied_list and (tile.x, tile.y + 1, tile.z) in occupied_list:
                if (tile.x - 1, tile.y, tile.z) not in occupied_list and (tile.x + 1, tile.y, tile.z) not in occupied_list:
                    available_tiles.append(tile)

        # Returns True if the level has available tiles
        return bool(available_tiles)
    

    # Returns the locked tile number that unlocks the tile
    def locked_tile_number(self, cube, tile_list, solution_path):
        
        cube_sides = {'top':cube.top,
                    'bottom': cube.bottom,
                    'left': cube.left,
                    'right': cube.right,
                    'front': cube.front,
                    'back': cube.back}

        loop_number = 0
        for tile in tile_list:
            if tile.type != 'locked' : continue

            # Process to find the number that is required for the locked tile
            for direction in solution_path:
                
                if direction == 'up':
                    cube_sides['top'], cube_sides['bottom'], cube_sides['front'], cube_sides['back'] = cube_sides['front'], cube_sides['back'], cube_sides['bottom'], cube_sides['top']
                if direction == 'down':
                    cube_sides['top'], cube_sides['bottom'], cube_sides['front'], cube_sides['back'] = cube_sides['back'], cube_sides['front'], cube_sides['top'], cube_sides['bottom']
                if direction == 'left':
                    cube_sides['top'], cube_sides['bottom'], cube_sides['left'], cube_sides['right'] = cube_sides['right'], cube_sides['left'], cube_sides['top'], cube_sides['bottom']
                if direction == 'right':
                    cube_sides['top'], cube_sides['bottom'], cube_sides['left'], cube_sides['right'] = cube_sides['left'], cube_sides['right'], cube_sides['bottom'], cube_sides['top']

                loop_number += 1
                if tile_list[loop_number] == tile:
                    break
                
        return cube_sides['top']
    
    # Function to unlock a lock tile
    def locked_tile(self, cube, tile_list, number, screen, font):
        for i in range(0, len(tile_list)):
            if tile_list[i].type == 'locked':
                # Display the locked tile number
                text = font.render(f'{number}', True, (255, 0, 0))
                screen.blit(text, (tile_list[i].coords[0] - 5, tile_list[i].coords[1] - 10))
                # If the player's dice top matches the required number, unlock the tile
                if (cube.x, cube.y, cube.z) == (tile_list[i].x, tile_list[i].y, tile_list[i].z) and cube.top == number:
                    tile_list[i].type = 'unlocked'
                    tile_list[i+1].type = 'normal'
        


    # Function for functioning of broken tiles
    def broken_tiles(self, cube, tile_list, occupied_list):
        for tile in tile_list[1:]:

            if tile.type == 'broken':
                if (cube.x, cube.y, cube.z) == (tile.x, tile.y, tile.z):
                    tile.stepped_on = 1
            
            if tile.stepped_on and (cube.x, cube.y, cube.z) != (tile.x, tile.y, tile.z):
                # Slowly fade the tile
                tile.alpha -= 1
                # Cap to 0
                tile.alpha = max(0, tile.alpha)
                # Remove the tile once disappeared
                if tile.alpha <= 0:
                    tile_list.remove(tile)
                    occupied_list.remove((tile.x, tile.y, tile.z))
