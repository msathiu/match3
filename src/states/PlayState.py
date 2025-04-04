""" ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        self.board_highlight_i1 = -1
        self.board_highlight_j1 = -1
        self.board_highlight_i2 = -1
        self.board_highlight_j2 = -1

        self.highlighted_tile = False

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000

        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            self.timer -= 1

            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

    def render(self, surface: pygame.Surface) -> None:
       
        self.board.render(surface)


        if hasattr(self, 'row_to_clear') and hasattr(self, 'col_to_clear'):
            \
            row_y = self.row_to_clear * settings.TILE_SIZE + self.board.y
            row_rect = pygame.Rect(self.board.x, row_y, settings.BOARD_WIDTH * settings.TILE_SIZE, settings.TILE_SIZE)
            pygame.draw.rect(surface, (64, 224, 208), row_rect)  
            
            col_x = self.col_to_clear * settings.TILE_SIZE + self.board.x
            col_rect = pygame.Rect(col_x, self.board.y, settings.TILE_SIZE, settings.BOARD_HEIGHT * settings.TILE_SIZE)
            pygame.draw.rect(surface, (64, 224, 208), col_rect)  
            
        if hasattr(self, 'to_remove_pieces') and self.to_remove_pieces:
            for piece in self.to_remove_pieces:
                i, j = piece 
                x = j * settings.TILE_SIZE + self.board.x
                y = i * settings.TILE_SIZE + self.board.y
                piece_rect = pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE)
                pygame.draw.rect(surface, (64, 224, 208), piece_rect)  
                
        if hasattr(self, 'effect_pos') and self.effect_pos is not None:
            i, j = self.effect_pos
            effect_surface = pygame.Surface(
                (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT),
                pygame.SRCALPHA
            )
            color = (64, 224, 208, self.effect_alpha)   
            pygame.draw.rect(
                effect_surface,
                color,
                pygame.Rect(
                    self.board.x,
                    self.board.y + i * settings.TILE_SIZE,
                    settings.BOARD_WIDTH * settings.TILE_SIZE,
                    settings.TILE_SIZE,
                )
            )
            pygame.draw.rect(
                effect_surface,
                color,
                pygame.Rect(
                    self.board.x + j * settings.TILE_SIZE,
                    self.board.y,
                    settings.TILE_SIZE,
                    settings.BOARD_HEIGHT * settings.TILE_SIZE,
                )
            )
            surface.blit(effect_surface, (0, 0))

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

        if self.highlighted_tile:
            x = self.highlighted_j1 * settings.TILE_SIZE + self.board.x
            y = self.highlighted_i1 * settings.TILE_SIZE + self.board.y
            surface.blit(self.tile_alpha_surface, (x, y))


    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        if input_id == "click" and input_data.pressed:
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            i = (pos_y - self.board.y) // settings.TILE_SIZE
            j = (pos_x - self.board.x) // settings.TILE_SIZE

            if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                tile = self.board.tiles[i][j]
                
                if tile is None:
                    self.highlighted_tile = False
                    return
                    
                # Lógica para bomba
                if hasattr(tile, 'variety') and tile.variety == -1: 
                    self.__clear_row_and_column(tile.i, tile.j)
                    self.board.tiles[tile.i][tile.j] = None
                    self.active = False
                    Timer.tween(0.25, self.board.get_falling_tiles(), 
                            on_finish=lambda: setattr(self, 'active', True))
                    return
                    
               
                if not self.highlighted_tile:
                    self.highlighted_tile = True
                    self.highlighted_i1 = i
                    self.highlighted_j1 = j
                else:
                   
                    if i == self.highlighted_i1 and j == self.highlighted_j1:
                        self.highlighted_tile = False
                        return
                        
                    self.highlighted_i2 = i
                    self.highlighted_j2 = j
                    tile1 = self.board.tiles[self.highlighted_i1][self.highlighted_j1]
                    tile2 = self.board.tiles[self.highlighted_i2][self.highlighted_j2]
                    
                    if tile1 is None or tile2 is None:
                        self.highlighted_tile = False
                        return
                    
                    di = abs(self.highlighted_i2 - self.highlighted_i1)
                    dj = abs(self.highlighted_j2 - self.highlighted_j1)

                    if (di == 1 and dj == 0) or (di == 0 and dj == 1):
                        self.active = False
                        
                        # Lógica para Destructor
                        if hasattr(tile1, 'variety') and tile1.variety == -2: 
                            self.__destroy_color(tile1.i, tile1.j, tile2.color)
                            self.board.tiles[tile1.i][tile1.j] = None
                        elif hasattr(tile2, 'variety') and tile2.variety == -2:  
                            self.__destroy_color(tile2.i, tile2.j, tile1.color)
                            self.board.tiles[tile2.i][tile2.j] = None
                        
                        
                        def arrive():
                            self.board.tiles[tile1.i][tile1.j], self.board.tiles[tile2.i][tile2.j] = tile2, tile1
                            tile1.i, tile1.j, tile2.i, tile2.j = tile2.i, tile2.j, tile1.i, tile1.j
                            self._calculate_matches([tile1, tile2])

                        Timer.tween(
                            0.25,
                            [
                                (tile1, {"x": tile2.x, "y": tile2.y}),
                                (tile2, {"x": tile1.x, "y": tile1.y}),
                            ],
                            on_finish=arrive,
                        )

                    self.highlighted_tile = False

    def __clear_row_and_column(self, i: int, j: int) -> None:
        deleted_tiles = 0
        
        
        settings.SOUNDS["match"].play()  

        
        self.effect_alpha = 255  
        self.effect_time = 0.5  
        self.effect_pos = (i, j)  

      
        for x in range(settings.BOARD_WIDTH):
            if self.board.tiles[i][x] is not None:
                deleted_tiles += 1
                self.board.tiles[i][x] = None

        for y in range(settings.BOARD_HEIGHT):
            if self.board.tiles[y][j] is not None and y != i:
                deleted_tiles += 1
                self.board.tiles[y][j] = None

        
        self.score += deleted_tiles * 2

        
        Timer.tween(
            self.effect_time,
            [(self, {"effect_alpha": 0})],  
            on_finish=lambda: self.__finish_effect() 
        )

      
        tweens = self.board.get_falling_tiles()
        Timer.tween(0.25, tweens)

    def __finish_effect(self) -> None:
        """Limpia las variables del efecto visual."""
        self.effect_pos = None

    def render(self, surface: pygame.Surface) -> None:
        
        self.board.render(surface)

        
        if hasattr(self, 'effect_pos') and self.effect_pos is not None:
            i, j = self.effect_pos
            effect_surface = pygame.Surface(
                (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT),
                pygame.SRCALPHA
            )
            color = (64, 224, 208, self.effect_alpha)   
            pygame.draw.rect(
                effect_surface,
                color,
                pygame.Rect(
                    self.board.x,
                    self.board.y + i * settings.TILE_SIZE,
                    settings.BOARD_WIDTH * settings.TILE_SIZE,
                    settings.TILE_SIZE,
                )
            )
            pygame.draw.rect(
                effect_surface,
                color,
                pygame.Rect(
                    self.board.x + j * settings.TILE_SIZE,
                    self.board.y,
                    settings.TILE_SIZE,
                    settings.BOARD_HEIGHT * settings.TILE_SIZE,
                )
            )
            surface.blit(effect_surface, (0, 0))

        
        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )
        
        if self.highlighted_tile:
            x = self.highlighted_j1 * settings.TILE_SIZE + self.board.x
            y = self.highlighted_i1 * settings.TILE_SIZE + self.board.y
            surface.blit(self.tile_alpha_surface, (x, y))

    def __destroy_color(self, i: int, j: int, target_color: int) -> None:
        """Elimina todas las fichas del color especificado, incluyendo la ficha especial Destructor."""
        if not (0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH):
            return

        print(f"Destruyendo color {target_color} iniciando en ({i},{j})")

        deleted_tiles = 0  

        #Eliminar el Destructor en cualquier ubicación
        if hasattr(self, "destructor_position") and self.destructor_position:
            di, dj = self.destructor_position
            if self.board.tiles[di][dj] is not None:
                print(f"Eliminando Destructor en ({di},{dj})")
                self.board.tiles[di][dj] = None
                deleted_tiles += 1

        # Eliminar las fichas 
        for row in range(settings.BOARD_HEIGHT):
            for col in range(settings.BOARD_WIDTH):
                tile = self.board.tiles[row][col]
                if tile is not None and hasattr(tile, 'color') and tile.color == target_color:
                    print(f"Eliminando ficha de color {target_color} en ({row},{col})")
                    self.board.tiles[row][col] = None
                    deleted_tiles += 1

        print(f"Total fichas eliminadas: {deleted_tiles}")

        settings.SOUNDS["match"].play()

        # Actualizar puntuación
        self.score += deleted_tiles * 50
        print(f"Nuevo score: {self.score}")

        self.active = False

        falling_tiles = self.board.get_falling_tiles()
        print(f"Fichas que caerán: {len(falling_tiles)}")

        self.destructor_position = (i, j)

        def on_finish():
            print("Animación de caída completada")

            for row in range(settings.BOARD_HEIGHT):
                for col in range(settings.BOARD_WIDTH):
                    if self.board.tiles[row][col] is None:
                        if (row, col) == self.destructor_position:
                            print(f"Posición del destructor ({row},{col}) NO generará ficha nueva")
                        else:
                            self.board.tiles[row][col] = self.board.generate_tile(row, col, force_normal=True)
                            print(f"Generada ficha normal en ({row},{col})")

            self.destructor_position = None

            self.active = True
            self._calculate_matches([])

        Timer.tween(0.25, falling_tiles, on_finish=on_finish)


    def _calculate_matches(self, tiles: List) -> None:
        """Calculate matches after a move or board update."""
        matches = self.board.calculate_matches_for(tiles)

        if not matches:
            
            if not self.board.has_valid_moves():
                
                settings.SOUNDS["no-match"].play()
                self.active = False
                
                def reshuffle_and_check():
                    self.board.reshuffle_board()
                    self.active = True
                    
                    self._calculate_matches([])
                
                Timer.after(0.5, reshuffle_and_check)
            else:
                self.active = True
            return
        
        settings.SOUNDS["match"].play()
        for match in matches:
            self.score += len(match) * 50

        
        self.board.remove_matches()
        
    
        falling_tiles = self.board.get_falling_tiles()

        def on_finish():

            for row in range(settings.BOARD_HEIGHT):
                for col in range(settings.BOARD_WIDTH):
                    if self.board.tiles[row][col] is None:
                        self.board.tiles[row][col] = self.board.generate_tile(row, col)
            
          
            self._calculate_matches([])

        Timer.tween(0.25, falling_tiles, on_finish=on_finish)