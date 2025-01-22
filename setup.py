from setuptools import setup, find_packages

setup(
    name='fractal-forge',
    version='1.0.0',
    description='An interactive fractal visualization application',
    author='Saqlain Abbas',
    author_email='saqlainrazee@gmail.com',
    url='https://github.com/Razee4315/FractalForge',
    packages=find_packages(),
    install_requires=[
        'pygame==2.6.1',
        'numpy==1.24.3',
        'numba==0.57.0',
        'matplotlib==3.7.1',
    ],
    extras_require={
        'dev': [
            'pytest==8.0.0',
            'flake8',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='fractal visualization pygame',
)
