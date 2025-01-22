import sys
import pygame
import numpy as np
from pygame.locals import *
from settings import *
from fractal_generator import FractalGenerator
from color_handler import ColorHandler
from ui_components import Button, HUD

class FractalForge:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("FractalForge: Infinite Zoom Explorer")
        self.clock = pygame.time.Clock()
        
        # Fractal state
        self.view = {
            'x': -0.5,
            'y': 0.0,
            'zoom': 1.0,
            'iterations': MAX_ITER,
            'julia': False,
            'drag_start': None,
            'julia_c': complex(-0.4, 0.6)  # Default Julia constant
        }
        
        # Initialize components
        self.generator = FractalGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.color_handler = ColorHandler()
        self.hud = HUD()
        
        # Simplified UI
        self.ui_elements = [
            Button(
                SCREEN_WIDTH - 140, 20, 120, 40, 
                "Reset", self.reset_view
            ),
            Button(
                SCREEN_WIDTH - 140, 80, 120, 40,
                "Colors", self.cycle_colormap
            ),
            Button(
                SCREEN_WIDTH - 140, 140, 120, 40,
                "Julia Explore", self.explore_julia
            ),
            Button(
                SCREEN_WIDTH - 140, 200, 120, 40,
                "Zoom In", self.zoom_in
            )
        ]

        # Automatic quality adjustment
        self.quality_timer = 0
        self.auto_quality = True
        self.needs_redraw = True

        # Pan speed for arrow key navigation
        self.pan_speed = PAN_SPEED  # Use constant from settings
        
        # Smooth dragging
        self.drag_sensitivity = 0.005

    def reset_view(self):
        self.view.update(x=-0.5, y=0.0, zoom=1.0, iterations=MAX_ITER)
        self.needs_redraw = True

    def toggle_julia(self):
        self.view['julia'] = not self.view['julia']
        self.needs_redraw = True

    def cycle_colormap(self):
        maps = ['viridis', 'plasma', 'rainbow', 'hsv']
        
        # Get the current colormap name safely
        current_map = (self.color_handler.current_cmap.name 
                       if hasattr(self.color_handler.current_cmap, 'name') 
                       else 'viridis')
        
        # Find the index of the current map or default to 0
        try:
            current_index = maps.index(current_map)
        except ValueError:
            current_index = 0
        
        # Cycle to the next map
        new_map = maps[(current_index + 1) % len(maps)]
        self.color_handler.set_colormap(new_map)
        self.needs_redraw = True

    def save_image(self):
        import os
        from datetime import datetime
        
        # Create screenshots directory if it doesn't exist
        os.makedirs('screenshots', exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'screenshots/fractal_{timestamp}.png'
        
        # Render and save the current fractal view
        fractal_surface = self.draw_fractal()
        pygame.image.save(fractal_surface, filename)

    def explore_julia(self):
        """
        Interactive Julia set parameter exploration
        Randomly generate new Julia set constants
        """
        # Generate random Julia set parameters
        real_part = np.random.uniform(-1.0, 1.0)
        imag_part = np.random.uniform(-1.0, 1.0)
        
        # Update Julia constant
        self.view['julia_c'] = complex(real_part, imag_part)
        
        # Toggle Julia mode if not already active
        if not self.view['julia']:
            self.toggle_julia()
        
        # Reset view for new Julia exploration
        self.reset_view()
        
        # Trigger redraw
        self.needs_redraw = True

    def zoom_in(self):
        """Zoom in at the center of the screen"""
        center_x = SCREEN_WIDTH / 2
        center_y = SCREEN_HEIGHT / 2
        self.zoom_to_point((center_x, center_y), ZOOM_FACTOR)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Mouse controls
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click - start drag
                    self.view['drag_start'] = event.pos
                elif event.button == 3:  # Right click - reset zoom
                    self.reset_view()
                elif event.button == 4:  # Scroll up - zoom in
                    self.zoom_to_point(event.pos, ZOOM_FACTOR)
                elif event.button == 5:  # Scroll down - zoom out
                    self.zoom_to_point(event.pos, 1/ZOOM_FACTOR)
                    
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    self.view['drag_start'] = None
            
            elif event.type == MOUSEMOTION:
                # Smooth dragging
                if self.view['drag_start']:
                    dx = (event.pos[0] - self.view['drag_start'][0]) * self.drag_sensitivity / self.view['zoom']
                    dy = (event.pos[1] - self.view['drag_start'][1]) * self.drag_sensitivity / self.view['zoom']
                    
                    # Adjust view based on drag
                    self.view['x'] -= dx * 4 / SCREEN_WIDTH
                    self.view['y'] += dy * 3 / SCREEN_HEIGHT
                    
                    # Update drag start
                    self.view['drag_start'] = event.pos
                    self.needs_redraw = True
            
            # Keyboard controls
            elif event.type == KEYDOWN:
                if event.key == K_r:    # Reset view
                    self.reset_view()
                elif event.key == K_j:  # Toggle Julia/Mandelbrot
                    self.toggle_julia()
                elif event.key == K_s:  # Save image
                    self.save_image()
                elif event.key == K_c:  # Cycle colors
                    self.cycle_colormap()
                elif event.key == K_q:  # Quit
                    pygame.quit()
                    sys.exit()
                elif event.key == K_LEFT:  # Pan left
                    self.view['x'] -= self.pan_speed / self.view['zoom']
                    self.needs_redraw = True
                elif event.key == K_RIGHT:  # Pan right
                    self.view['x'] += self.pan_speed / self.view['zoom']
                    self.needs_redraw = True
                elif event.key == K_UP:  # Pan up
                    self.view['y'] -= self.pan_speed / self.view['zoom']
                    self.needs_redraw = True
                elif event.key == K_DOWN:  # Pan down
                    self.view['y'] += self.pan_speed / self.view['zoom']
                    self.needs_redraw = True

            # Handle UI elements
            for element in self.ui_elements:
                element.handle_event(event)

    def zoom_to_point(self, mouse_pos, factor):
        """Smooth zoom centered on mouse position"""
        # Convert mouse position to fractal coordinates
        old_x = self.view['x'] + (mouse_pos[0]/SCREEN_WIDTH - 0.5) * 4/self.view['zoom']
        old_y = self.view['y'] - (mouse_pos[1]/SCREEN_HEIGHT - 0.5) * 3/self.view['zoom']
        
        # Apply zoom
        self.view['zoom'] *= factor
        
        # Adjust center to maintain mouse position
        new_x = old_x - (mouse_pos[0]/SCREEN_WIDTH - 0.5) * 4/self.view['zoom']
        new_y = old_y + (mouse_pos[1]/SCREEN_HEIGHT - 0.5) * 3/self.view['zoom']
        
        self.view['x'] = new_x
        self.view['y'] = new_y
        self.needs_redraw = True

    def draw_fractal(self):
        # Adaptive quality with smoother transitions
        base_iterations = MAX_ITER
        zoom_factor = np.log10(self.view['zoom'] + 1)
        self.view['iterations'] = int(base_iterations * (1 + zoom_factor))
        
        # Calculate view parameters with improved precision
        width_ratio = 4 / self.view['zoom']
        height_ratio = 3 / self.view['zoom']
        xmin = self.view['x'] - width_ratio/2
        xmax = self.view['x'] + width_ratio/2
        ymin = self.view['y'] - height_ratio/2
        ymax = self.view['y'] + height_ratio/2
        
        # Generate fractal
        iterations = self.generator.generate(
            xmin, xmax, ymin, ymax, 
            self.view['iterations'], 
            self.view['julia'],
            self.view['julia_c'] if self.view['julia'] else None
        )
        
        # Color mapping with stability
        colored = self.color_handler.colorize(iterations, self.view['iterations'])
        
        return pygame.surfarray.make_surface(colored)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            
            # Continuous key state checking for smooth movement
            keys = pygame.key.get_pressed()
            
            # Adjust pan amount based on zoom and shift key
            pan_amount = self.pan_speed / self.view['zoom'] * (1 if keys[K_LSHIFT] else 0.5)
            
            # Correct arrow key movement
            if keys[K_LEFT]:
                self.view['x'] -= pan_amount
                self.needs_redraw = True
            if keys[K_RIGHT]:
                self.view['x'] += pan_amount
                self.needs_redraw = True
            if keys[K_UP]:
                self.view['y'] -= pan_amount  # Corrected: move up when UP is pressed
                self.needs_redraw = True
            if keys[K_DOWN]:
                self.view['y'] += pan_amount  # Corrected: move down when DOWN is pressed
                self.needs_redraw = True
            
            # Update phase for animations
            self.color_handler.update_phase(dt)
            
            # Render if needed
            if self.needs_redraw:
                fractal_surface = self.draw_fractal()
                self.needs_redraw = False
            
            # Draw everything
            self.screen.fill(COLORS['bg'])
            self.screen.blit(fractal_surface, (0, 0))
            
            # Draw UI
            for element in self.ui_elements:
                element.draw(self.screen)
            
            # Draw HUD
            mouse_pos = pygame.mouse.get_pos()
            self.hud.draw(self.screen, mouse_pos, self.view)
            
            pygame.display.flip()

if __name__ == "__main__":
    app = FractalForge()
    app.run()
