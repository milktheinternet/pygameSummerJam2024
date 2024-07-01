import pygame as pg
import numpy as np
from gamemath import Vector  # Assuming this is a custom Vector class you have
from perlin import perlin
import math
from gameloading import show_progress


def make_shadow(radius: int):
    srf = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
    for i in range(radius, 0, -1):
        p = i / radius
        alpha = int(p ** 2 * 255)
        pos = Vector(radius * 1.5, radius * 1.5) - Vector(i, i) / 2
        pg.draw.circle(srf, (0, 0, 0, alpha), round(pos).tuple, i)
    return srf


def gen_perlin_noise(size: Vector, scale=0.1, seed=None):
    width, height = size.tuple
    grid = np.zeros((width, height))

    # Set the seed for reproducibility
    rng = np.random.default_rng(seed)

    cx, cy = (size/2).tuple
    radius = cx
    def dist(x, y):
        return math.sqrt((x-cx)**2+(y-cy)**2)

    # Generate Perlin-like noise using numpy
    for x in range(width):
        for y in range(height):
            if dist(x, y) < radius:
                grid[x][y] = perlin(x * scale, y * scale, seed)
            else:
                grid[x][y] = 0

    return grid

def interpolate_color(start_color, end_color, steps = 10):
    return [
        (
            int(start_color[0] + (end_color[0] - start_color[0]) * i / (steps - 1)),
            int(start_color[1] + (end_color[1] - start_color[1]) * i / (steps - 1)),
            int(start_color[2] + (end_color[2] - start_color[2]) * i / (steps - 1)),
        )
        for i in range(steps)
    ]

COLD = (200, 150, 255)
LUSH = (50, 220, 75)
HOT = (255, 127, 0)
LAND = interpolate_color(COLD, LUSH) + interpolate_color(LUSH, HOT)


def list_float_idx(list_: list, idx: float):
    return list_[int((len(list_)-1)*idx)]


def gen_planet(game, size: Vector, star, wet=1.0, temperature=0.5):
    srf = pg.Surface(size.tuple, pg.SRCALPHA)
    water = (0, 0, 255)
    land = list_float_idx(LAND, temperature)
    radius = int(size.x // 2)

    # Generate and layer terrain noise
    base_seed = int(star.x * 1000 + star.y)
    noise_grid = np.zeros((size.x, size.y))
    layers = 3  # Adjusted number of layers

    for i in range(layers):
        show_progress(i/layers, game.dis, msg="Scanning...")
        scale = 0.05 * (2 ** i)  # Adjusted scale factor
        weight = 0.5 ** i  # Weight for blending
        noise_layer = gen_perlin_noise(size, scale, seed=base_seed + i)
        noise_grid += weight * noise_layer

    # Normalize noise values to [0, 1]
    noise_grid = (noise_grid - np.min(noise_grid)) / (np.max(noise_grid) - np.min(noise_grid))

    cx, cy = (size / 2).tuple
    def dist(x, y):
        return math.sqrt((x - cx) ** 2 + (y - cy) ** 2)

    # Apply terrain colors based on noise values
    for x in range(size.x):
        for y in range(size.y):
            if dist(x, y) > radius - 1:
                srf.set_at((x, y), (0,0,0,0))
                continue

            elevation = noise_grid[x][y]

            if elevation > wet:
                color = [int(c*elevation) for c in land]
            else:
                color = [int(c*elevation) for c in water]
            color.append(255)
            srf.set_at((x, y), color)

    # Apply shadow
    srf.blit(make_shadow(radius), (0, 0))

    return srf
