import pygame
import math
import random

class Tile:
    def __init__(self, x, y, z, occupied_list):
        # the 'x,y,z' coordinates of the game
        self.x, self.y = x, y
        self.z = z

        # the actual coordinates on screen

        self.color = (128, 128, 128)
        self.edge_size = 30 # Actual size of edge, not isometrically

        self.type = 'normal'
        self.stepped_on = 0

        # Adds the tiles coordinates to the occupied list
        occupied_list.append((x, y, z))


    def draw(self, screen, offset):
        self.coords = (400 + (self.y - offset[1]) * 17.5 * math.sqrt(3) + (self.x - offset[0]) * 17.5 * math.sqrt(3), 
                       400 - (self.y - offset[1]) * 17.5 + (self.x - offset[0]) * 17.5)
        self.polygon = [
            (self.coords[0], self.coords[1] - self.edge_size/2), # Top
            (self.coords[0] + self.edge_size/2 * math.sqrt(3), self.coords[1]), # Right
            (self.coords[0], self.coords[1] + self.edge_size/2), # Bottom
            (self.coords[0] - self.edge_size/2 * math.sqrt(3), self.coords[1]) # Left
        ]

        pygame.draw.polygon(screen, self.color, self.polygon)


        if self.type == 'end':
            self.color = (0, 255, 0)
        elif self.type == 'broken':
            self.color = (0, 0, 255)
        elif self.type == 'locker':
            self.color = (255, 255, 0)
        else :
            self.color = (128, 128, 128)

    def generate_tiles(self, n, cube, tile_list, occupied_list, solution_path):
        
        # Create a shallow copy to iterate over a list
        copy_of_tile_list = [el for el in tile_list]
        solution_path.clear()

        for el in copy_of_tile_list:

            #Remove all the tiles except the tile on which player lands
            if (el.x, el.y, el.z) != (cube.x, cube.y, cube.z): 
                tile_list.remove(el)
                occupied_list.remove((el.x, el.y, el.z))
        #print(occupied_list)

        # To get the start tile
        start_tile = tile_list[0]
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
        
        print(solution_path)
        # To find the end_tile
        end_tile = tile_list[-1]
        end_tile.type = 'end'


    def level_setter(self, tile_list, occupied_list, level_type):
        if level_type == 'broken_tiles':
            for tile in tile_list:
                if tile == tile_list[0] : continue
                selector = random.randint(0, 10)
                if selector in range(0, 3) and tile.type != 'end':
                    tile.type = 'broken'

        if level_type == 'locked_tiles':
            available_tiles = []

            for tile in tile_list:

                if tile == tile_list[0] : continue

                if (tile.x - 1, tile.y, tile.z) in occupied_list and (tile.x + 1, tile.y, tile.z) in occupied_list:
                    if (tile.x, tile.y - 1, tile.z) not in occupied_list and (tile.x, tile.y + 1, tile.z) not in occupied_list:
                        available_tiles.append(tile)
                elif (tile.x, tile.y - 1, tile.z) in occupied_list and (tile.x, tile.y + 1, tile.z) in occupied_list:
                    if (tile.x - 1, tile.y, tile.z) not in occupied_list and (tile.x + 1, tile.y, tile.z) not in occupied_list:
                        available_tiles.append(tile)

            if available_tiles:
                locked_tile = random.choice(available_tiles)
                locked_tile.type = 'locked'

                for i in range(0, len(tile_list) - 1):
                    if tile_list[i].type == 'locked':
                        tile_list[i+1].type = 'locker'
                
                available_tiles.remove(locked_tile)


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

        return bool(available_tiles)

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
    
    def locked_tile(self, cube, tile_list, number):
        for i in range(0, len(tile_list)):
            if tile_list[i].type == 'locked' and (cube.x, cube.y, cube.z) == (tile_list[i].x, tile_list[i].y, tile_list[i].z) and cube.top == number:
                tile_list[i].type = 'unlocked'
                tile_list[i+1].type = 'normal'
        


    # Function for functioning of broken tiles
    def broken_tiles(self, cube, tile_list, occupied_list):
        for tile in tile_list[1:]:

            if tile.type == 'broken':
                if (cube.x, cube.y, cube.z) == (tile.x, tile.y, tile.z):
                    tile.stepped_on = 1
            
            if tile.stepped_on and (cube.x, cube.y, cube.z) != (tile.x, tile.y, tile.z):
                tile_list.remove(tile)
                occupied_list.remove((tile.x, tile.y, tile.z))
