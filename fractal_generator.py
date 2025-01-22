import numpy as np
import numba
from numba import njit, prange

class FractalGenerator:
    def __init__(self, width, height):
        # Pre-allocate high-precision buffers
        self.width = width
        self.height = height
        self.iterations_buffer = np.zeros((height, width), dtype=np.uint32)
        
        # Use higher precision for calculations
        self.dtype = np.float64

    @staticmethod
    @njit(parallel=True, fastmath=True)
    def generate_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
        """
        High-precision Mandelbrot set generation with parallel processing
        Uses float64 for maximum precision
        """
        div_time = np.zeros((height, width), dtype=np.uint32)
        
        for i in prange(height):
            for j in prange(width):
                # Map pixel coordinates to complex plane
                real = xmin + (xmax - xmin) * j / (width - 1)
                imag = ymin + (ymax - ymin) * i / (height - 1)
                
                c = complex(real, imag)
                z = 0j
                
                for k in range(max_iter):
                    z = z * z + c
                    if z.real * z.real + z.imag * z.imag > 4.0:
                        div_time[i, j] = k
                        break
                else:
                    div_time[i, j] = max_iter - 1
        
        return div_time

    @staticmethod
    @njit(parallel=True, fastmath=True)
    def generate_julia(xmin, xmax, ymin, ymax, width, height, max_iter, c):
        """
        High-precision Julia set generation with parallel processing
        Uses float64 for maximum precision
        """
        div_time = np.zeros((height, width), dtype=np.uint32)
        
        for i in prange(height):
            for j in prange(width):
                # Map pixel coordinates to complex plane
                real = xmin + (xmax - xmin) * j / (width - 1)
                imag = ymin + (ymax - ymin) * i / (height - 1)
                
                z = complex(real, imag)
                
                for k in range(max_iter):
                    z = z * z + c
                    if z.real * z.real + z.imag * z.imag > 4.0:
                        div_time[i, j] = k
                        break
                else:
                    div_time[i, j] = max_iter - 1
        
        return div_time

    def generate(self, xmin, xmax, ymin, ymax, max_iter, is_julia=False, julia_c=None):
        """
        Generate fractal with adaptive precision and parallel processing
        """
        # Default Julia constant if not provided
        if is_julia and julia_c is None:
            julia_c = complex(-0.4, 0.6)
        
        # Choose generation method
        if is_julia:
            self.iterations_buffer = self.generate_julia(
                xmin, xmax, ymin, ymax, 
                self.width, self.height, 
                max_iter, julia_c
            )
        else:
            self.iterations_buffer = self.generate_mandelbrot(
                xmin, xmax, ymin, ymax, 
                self.width, self.height, 
                max_iter
            )
        
        return self.iterations_buffer
