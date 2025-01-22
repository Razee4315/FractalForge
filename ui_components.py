import pygame
import numpy as np
from pygame.locals import *
from settings import COLORS

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        color = COLORS['hover'] if self.hovered else COLORS['ui']
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, COLORS['text'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN and self.hovered:
            self.callback()

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_val
        self.max = max_val
        self.value = initial_val
        self.callback = callback
        self.dragging = False

    def draw(self, surface):
        # Track
        pygame.draw.rect(surface, COLORS['ui'], self.rect, border_radius=3)
        # Thumb
        pos = self.rect.left + (self.value - self.min)/(self.max - self.min) * self.rect.width
        pygame.draw.circle(surface, COLORS['neon'], (int(pos), self.rect.centery), 8)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        if self.dragging and event.type == MOUSEMOTION:
            rel_x = event.pos[0] - self.rect.left
            self.value = np.clip(self.min + (rel_x / self.rect.width) * (self.max - self.min), 
                               self.min, self.max)
            self.callback(self.value)

class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.visible = True

    def draw(self, surface, mouse_pos, view_params):
        if not self.visible:
            return
        
        lines = [
            "FractalForge v1.0",
            "Created by Saqlain Abbas",
            "GitHub: @Razee4315",
            "",
            f"X: {view_params['x']:.8f}",
            f"Y: {view_params['y']:.8f}",
            f"Zoom: {view_params['zoom']:.1f}x",
            f"Iterations: {view_params['iterations']}",
            f"Mode: {'Julia' if view_params.get('julia', False) else 'Mandelbrot'}",
            f"Julia C: {view_params.get('julia_c', 'N/A')}" if view_params.get('julia', False) else "",
            "",
            "Controls:",
            "Left drag - Smooth Pan",
            "Scroll/S - Zoom",
            "Arrow keys - Move",
            "Shift + Arrow keys - Fast move",
            "Right click - Reset view",
            "R - Reset view",
            "J - Toggle Julia/Mandelbrot",
            "C - Cycle colors",
            "S - Save image",
            "Q - Quit"
        ]
        
        y = 10
        for line in lines:
            if line:  # Skip empty lines
                text = self.font.render(line, True, COLORS['text'])
                surface.blit(text, (10, y))
                y += 25
