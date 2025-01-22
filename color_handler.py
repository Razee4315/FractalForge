import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class ColorHandler:
    def __init__(self):
        # Predefined color maps with smooth transitions
        self.colormaps = {
            'viridis': cm.viridis,
            'plasma': cm.plasma,
            'rainbow': cm.rainbow,
            'hsv': cm.hsv
        }
        
        # Default colormap
        self.current_cmap = self.colormaps['viridis']
        
        # Animation phase
        self.phase = 0.0
        self.phase_speed = 0.1

    def set_colormap(self, map_name):
        """Set current colormap with error handling"""
        try:
            self.current_cmap = self.colormaps[map_name]
        except KeyError:
            # Fallback to default
            self.current_cmap = self.colormaps['viridis']

    def update_phase(self, dt):
        """Update color animation phase"""
        self.phase += self.phase_speed * dt
        self.phase %= 1.0

    def colorize(self, iterations, max_iter):
        """
        Advanced color mapping with smooth transitions
        Uses logarithmic scaling for better detail
        """
        # Prevent division by zero
        max_iter = max(max_iter, 1)
        
        # Logarithmic scaling for better color distribution
        log_iter = np.log(iterations + 1) / np.log(max_iter + 1)
        
        # Smooth color mapping
        colored = self.current_cmap(log_iter)
        
        # Convert to 8-bit color with RGB channels
        colored = (colored[:, :, :3] * 255).astype(np.uint8)
        
        # Ensure correct channel order for Pygame (RGB -> BGR)
        colored = colored[..., [2, 1, 0]]
        
        return colored
