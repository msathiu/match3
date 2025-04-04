"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Board.
"""

from typing import List, Optional, Tuple, Any, Dict, Set

import pygame

import random

import settings
from src.Tile import Tile


class Board:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.matches: List[List[Tile]] = []
        self.tiles: List[List[Tile]] = []
        self.__initialize_tiles()
        
    def render(self, surface: pygame.Surface) -> None:
        for row in self.tiles:
            for tile in row:
                if tile is not None:  
                    tile.render(surface, self.x, self.y)

    def __is_match_generated(self, i: int, j: int, color: int) -> bool:
        if (
            i >= 2
            and self.tiles[i - 1][j].color == color
            and self.tiles[i - 2][j].color == color
        ):
            return True

        return (
            j >= 2
            and self.tiles[i][j - 1].color == color
            and self.tiles[i][j - 2].color == color
        )

    def __initialize_tiles(self) -> None:
        self.tiles = [
            [None for _ in range(settings.BOARD_WIDTH)]
            for _ in range(settings.BOARD_HEIGHT)
        ]
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                color = random.randint(0, settings.NUM_COLORS - 1)
                while self.__is_match_generated(i, j, color):
                    color = random.randint(0, settings.NUM_COLORS - 1)

                self.tiles[i][j] = Tile(
                    i, j, color, random.randint(0, settings.NUM_VARIETIES - 1)
                )

    def __calculate_match_rec(self, tile: Tile) -> Set[Tile]:
        if tile in self.in_stack:
            return []

        self.in_stack.add(tile)

        color_to_match = tile.color

       
        h_match: List[Tile] = []

        if tile.j > 0:
            left = max(0, tile.j - 2)
            for j in range(tile.j - 1, left - 1, -1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

    
        if tile.j < settings.BOARD_WIDTH - 1:
            right = min(settings.BOARD_WIDTH - 1, tile.j + 2)
            for j in range(tile.j + 1, right + 1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        
        v_match: List[Tile] = []

       
        if tile.i > 0:
            top = max(0, tile.i - 2)
            for i in range(tile.i - 1, top - 1, -1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        
        if tile.i < settings.BOARD_HEIGHT - 1:
            bottom = min(settings.BOARD_HEIGHT - 1, tile.i + 2)
            for i in range(tile.i + 1, bottom + 1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        match: List[Tile] = []

        if len(h_match) >= 2:
            for t in h_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(v_match) >= 2:
            for t in v_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(match) > 0:
            if tile not in self.in_match:
                self.in_match.add(tile)
                match.append(tile)

        for t in match:
            match += self.__calculate_match_rec(t)

        self.in_stack.remove(tile)
        return match

    def calculate_matches_for(
        self, new_tiles: List[Tile]
    ) -> Optional[List[List[Tile]]]:
        self.in_match: Set[Tile] = set()
        self.in_stack: Set[Tile] = set()

        for tile in new_tiles:
            if tile in self.in_match:
                continue
            match = self.__calculate_match_rec(tile)
            if len(match) > 0:
                self.matches.append(match)

        delattr(self, "in_match")
        delattr(self, "in_stack")

        return self.matches if len(self.matches) > 0 else None

    

    def remove_matches(self) -> None:
        for match in self.matches:
            if len(match) >= 5:  # Match de 5+ fichas
                last_tile = match[-1]  
                i, j = last_tile.i, last_tile.j
                color = match[0].color
                
                if self.tiles[i][j] is None or self.tiles[i][j].variety != -2:
                    self.tiles[i][j] = Tile(i, j, color, -2)  
                
                
                for tile in match[:-1]:
                    self.tiles[tile.i][tile.j] = None
                    
            elif len(match) == 4:  # Match de 4 (para la bomba)
                first_tile = match[0]
                i, j = first_tile.i, first_tile.j
                
                
                if self.tiles[i][j] is None or self.tiles[i][j].variety != -1:
                    self.tiles[i][j] = Tile(i, j, -1, -1)
                
                
                for tile in match[1:]:
                    self.tiles[tile.i][tile.j] = None
            else:
                
                for tile in match:
                    self.tiles[tile.i][tile.j] = None
        self.matches = []


    def get_falling_tiles(self) -> Tuple[Any, Dict[str, Any]]:
       
        tweens: Tuple[Tile, Dict[str, Any]] = []


        for j in range(settings.BOARD_WIDTH):
            space = False
            space_i = -1
            i = settings.BOARD_HEIGHT - 1

            while i >= 0:
                tile = self.tiles[i][j]

               
                if space:
                   
                    if tile is not None:
                        self.tiles[space_i][j] = tile
                        tile.i = space_i

                        
                        self.tiles[i][j] = None

                        tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))
                        space = False
                        i = space_i
                        space_i = -1
                elif tile is None:
                    space = True

                    if space_i == -1:
                        space_i = i

                i -= 1


        for j in range(settings.BOARD_WIDTH):
            for i in range(settings.BOARD_HEIGHT):
                tile = self.tiles[i][j]

                if tile is None:
                    
                    tile = Tile(
                        i,
                        j,
                        random.randint(0, settings.NUM_COLORS - 1),
                        0  
                    )
                    tile.y -= settings.TILE_SIZE
                    self.tiles[i][j] = tile
                    tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))

        return tweens

    def generate_tile(self, i: int, j: int, force_normal: bool = False) -> 'Tile':
        """Genera una nueva ficha en la posición (i,j)"""
        
        import random
        
        if force_normal:
            
            color = random.randint(0, settings.NUM_COLORS - 1)
            return Tile(i, j, color, variety=0)
        else:
            
            if random.random() < settings.SPECIAL_TILE_PROBABILITY:  
                variety = random.choice([-1, -2])
                return Tile(i, j, color=None, variety=variety)
            else:
                color = random.randint(0, settings.NUM_COLORS - 1)
                return Tile(i, j, color, variety=0)
            
    def has_valid_moves(self) -> bool:
        """Check if there are any valid moves left on the board."""
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                if j < settings.BOARD_WIDTH - 1 and self.__check_potential_match(i, j, i, j + 1):
                    return True
                if i < settings.BOARD_HEIGHT - 1 and self.__check_potential_match(i, j, i + 1, j):
                    return True
        return False

    def __check_potential_match(self, i1: int, j1: int, i2: int, j2: int) -> bool:
        """Check if swapping two tiles would create a match."""
        
        self.tiles[i1][j1], self.tiles[i2][j2] = self.tiles[i2][j2], self.tiles[i1][j1]
        
        tile1_has_match = self.__check_tile_for_match(i1, j1)
        tile2_has_match = self.__check_tile_for_match(i2, j2)
        
        self.tiles[i1][j1], self.tiles[i2][j2] = self.tiles[i2][j2], self.tiles[i1][j1]
        
        return tile1_has_match or tile2_has_match

    def __check_tile_for_match(self, i: int, j: int) -> bool:
        """Check if the tile at (i,j) is part of any potential match."""
        tile = self.tiles[i][j]
        if tile is None or not hasattr(tile, 'color'):
            return False
        
        color = tile.color
        
        horizontal_matches = 1
        
        x = j - 1
        while x >= 0:
            other_tile = self.tiles[i][x]
            if other_tile is None or not hasattr(other_tile, 'color') or other_tile.color != color:
                break
            horizontal_matches += 1
            x -= 1
            
        x = j + 1
        while x < settings.BOARD_WIDTH:
            other_tile = self.tiles[i][x]
            if other_tile is None or not hasattr(other_tile, 'color') or other_tile.color != color:
                break
            horizontal_matches += 1
            x += 1
        
        if horizontal_matches >= 3:
            return True
        
        
        vertical_matches = 1
        y = i - 1
        while y >= 0:
            other_tile = self.tiles[y][j]
            if other_tile is None or not hasattr(other_tile, 'color') or other_tile.color != color:
                break
            vertical_matches += 1
            y -= 1
        y = i + 1
        while y < settings.BOARD_HEIGHT:
            other_tile = self.tiles[y][j]
            if other_tile is None or not hasattr(other_tile, 'color') or other_tile.color != color:
                break
            vertical_matches += 1
            y += 1
        
        return vertical_matches >= 3

    def reshuffle_board(self) -> None:
        """Reorganiza completamente el tablero manteniendo las fichas especiales."""
        
        normal_tiles = []
        special_tiles = []
        
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                tile = self.tiles[i][j]
                if tile is not None:
                    if tile.variety >= 0:  
                        normal_tiles.append(tile)
                    else: 
                        special_tiles.append((i, j, tile))
        
        
        random.shuffle(normal_tiles)
        
       
        tile_index = 0
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                
                special_tile = next((t for t in special_tiles if t[0] == i and t[1] == j), None)
                if special_tile:
                    self.tiles[i][j] = special_tile[2]
                else:
                    if tile_index < len(normal_tiles):
                        tile = normal_tiles[tile_index]
                        tile.i = i
                        tile.j = j
                        tile.x = j * settings.TILE_SIZE
                        tile.y = i * settings.TILE_SIZE
                        self.tiles[i][j] = tile
                        tile_index += 1
                    else:
                        self.tiles[i][j] = None
        
       
        while True:
            matches = self.calculate_matches_for([t for row in self.tiles for t in row if t is not None])
            if matches is None:
                break
            self.remove_matches()
            for i in range(settings.BOARD_HEIGHT):
                for j in range(settings.BOARD_WIDTH):
                    if self.tiles[i][j] is None:
                        self.tiles[i][j] = Tile(i, j, random.randint(0, settings.NUM_COLORS - 1), 0)