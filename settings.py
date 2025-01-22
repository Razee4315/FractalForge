import pygame
import numpy

# Display Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Color Scheme
COLORS = {
    "bg": (0x0F, 0x0F, 0x17),
    "ui": (0x1F, 0x1F, 0x2F),
    "neon": (0x0F, 0xE7, 0xDC),
    "text": (0xE0, 0xE0, 0xE0),
    "hover": (0x2F, 0xAF, 0xFF),
}

# Panning and Zooming
PAN_SPEED = 0.2  # Adjust this value to control movement sensitivity
ZOOM_FACTOR = 1.1  # More granular zoom

# Fractal Defaults
MAX_ITER = 512  # Increased from 256 for more detail
PRECISION = numpy.float64  # High-precision floating point

# UI Layout
UI_MARGIN = 20
BUTTON_SIZE = (120, 40)
SLIDER_SIZE = (200, 20)

# Progressive Quality Settings
QUALITY_PROFILES = {
    'interactive': {'scale': 0.5, 'iterations': 128},
    'static': {'scale': 1.0, 'iterations': 512}
}
