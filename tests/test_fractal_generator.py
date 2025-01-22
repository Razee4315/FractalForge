import numpy as np
import pytest
from fractal_generator import FractalGenerator

def test_fractal_generator_initialization():
    """Test basic initialization of FractalGenerator"""
    generator = FractalGenerator(800, 600)
    assert generator.width == 800
    assert generator.height == 600

def test_mandelbrot_generation():
    """Test Mandelbrot set generation"""
    generator = FractalGenerator(800, 600)
    iterations = generator.generate(-2, 1, -1.5, 1.5, 256, False)
    
    # Check basic properties of generated iterations
    assert iterations is not None
    assert iterations.shape == (800, 600)
    assert np.min(iterations) >= 0
    assert np.max(iterations) <= 256

def test_julia_generation():
    """Test Julia set generation"""
    generator = FractalGenerator(800, 600)
    c = complex(-0.4, 0.6)  # Example Julia constant
    iterations = generator.generate(-2, 2, -2, 2, 256, True, c)
    
    # Check basic properties of generated iterations
    assert iterations is not None
    assert iterations.shape == (800, 600)
    assert np.min(iterations) >= 0
    assert np.max(iterations) <= 256

def test_invalid_parameters():
    """Test handling of invalid parameters"""
    generator = FractalGenerator(800, 600)
    
    # Test invalid iteration count
    with pytest.raises(ValueError):
        generator.generate(-2, 1, -1.5, 1.5, -100, False)
    
    # Test invalid dimensions
    with pytest.raises(ValueError):
        generator.generate(-2, 1, -1.5, 1.5, 256, False, None, width=-100)
