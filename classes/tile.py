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
    
        # To find the end_tile
        end_tile = tile_list[-1]
        
        end_tile.type = 'end'
