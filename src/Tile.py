"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Tile.
"""

import pygame
import math 
import settings


class Tile:
    def __init__(self, i: int, j: int, color: int, variety: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.color = color
        self.variety = variety
        self.alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        try:
            
            pos_x = self.x + offset_x
            pos_y = self.y + offset_y
            
            shadow = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(
                shadow,
                (0, 0, 0, 120),  # Negro semitransparente
                shadow.get_rect(),
                border_radius=7
            )
            surface.blit(shadow, (pos_x + 2, pos_y + 2))  
            if hasattr(self, 'variety'):
                if self.variety == -1:  # Bomba
                    if "bomb" in settings.TEXTURES:
                        surface.blit(
                            settings.TEXTURES["bomb"],
                            (pos_x, pos_y),
                            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE)
                        )
                    else:
                       
                        pygame.draw.circle(
                            surface,
                            (255, 0, 0),  
                            (pos_x + settings.TILE_SIZE//2, pos_y + settings.TILE_SIZE//2),
                            settings.TILE_SIZE//2 - 2
                        )
                        render_text(
                            surface, "B", settings.FONTS["small"],
                            pos_x + settings.TILE_SIZE//2 - 4,
                            pos_y + settings.TILE_SIZE//2 - 8,
                            (255, 255, 255)  
                        )
                        
                elif self.variety == -2:  # Destructor de color
                    if "color_destroyer" in settings.TEXTURES:
                        surface.blit(
                            settings.TEXTURES["color_destroyer"],
                            (pos_x, pos_y),
                            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE)
                        )
                    else:
                        
                        base_color = (50, 50, 255)  
                        pygame.draw.circle(
                            surface,
                            base_color,
                            (pos_x + settings.TILE_SIZE//2, pos_y + settings.TILE_SIZE//2),
                            settings.TILE_SIZE//2 - 2
                        )
                        
                        center_x, center_y = pos_x + settings.TILE_SIZE//2, pos_y + settings.TILE_SIZE//2
                        radius = settings.TILE_SIZE//3
                        
                        
                        pygame.draw.circle(
                            surface,
                            (255, 255, 255),  
                            (center_x, center_y),
                            radius,
                            2  
                        )
                        
                       
                        pygame.draw.line(
                            surface,
                            (255, 255, 255),
                            (center_x - radius + 2, center_y),
                            (center_x + radius - 2, center_y),
                            2
                        )
                        pygame.draw.line(
                            surface,
                            (255, 255, 255),
                            (center_x, center_y - radius + 2),
                            (center_x, center_y + radius - 2),
                            2
                        )
                        
                else:  
                    if hasattr(self, 'color'):
                        surface.blit(
                            settings.TEXTURES["tiles"],
                            (pos_x, pos_y),
                            settings.FRAMES["tiles"][self.color][self.variety]
                        )
                    else:
                        
                        pygame.draw.rect(
                            surface,
                            (200, 200, 200),
                            (pos_x, pos_y, settings.TILE_SIZE, settings.TILE_SIZE),
                            border_radius=7
                        )

        except Exception as e:
            print(f"Error renderizando ficha: {e}")
            
            pygame.draw.rect(
                surface,
                (255, 0, 255),
                (pos_x, pos_y, settings.TILE_SIZE, settings.TILE_SIZE)
            )
            render_text(
                surface, "Err", settings.FONTS["tiny"],
                pos_x + 5, pos_y + 5,
                (0, 0, 0)
            )

    def __draw_star(self, surface, center, outer_radius, inner_radius, color):
        """Dibuja una estrella de 5 puntas"""
        points = []
        for i in range(10):
            angle = math.pi * 2 * i / 10 - math.pi / 2
            radius = inner_radius if i % 2 else outer_radius
            points.append((
                center[0] + radius * math.cos(angle),
                center[1] + radius * math.sin(angle)
            ))
        pygame.draw.polygon(surface, color, points)