import pygame as pg
import numpy as np
from gamemath import Vector  # Assuming this is a custom Vector class you have
from perlin import perlin
import math
#from gameloading import show_progress
from random import randint, choice


def save_noise(noise_grid):
    w, h = len(noise_grid), len(noise_grid[0])
    srf = pg.Surface((w,h))
    for x in range(w):
        for y in range(h):
            srf.set_at((x,y), [noise_grid[x][y]*255]*3)
    pg.image.save(srf, f"assets/noise/noise{nextID()}.png")


def load_noise(id_):
    img = pg.image.load(f"assets/noise/noise{id_}.png")
    w, h = img.get_size()
    return [[img.get_at((x, y))[0]/255 for x in range(h)] for y in range(w)]


NOISE_DIAMETER = 300
NOISE_LAYERS = 6
NOISE_CACHE_SIZE = 30
NOISE_CACHE = [load_noise(id_) for id_ in range(1, NOISE_CACHE_SIZE + 1)]

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

COLD = (150, 150, 255)
LUSH = (50, 220, 75)
HOT = (255, 127, 0)
LAND = interpolate_color(COLD, LUSH) + interpolate_color(LUSH, HOT)


def list_float_idx(list_: list, idx: float):
    return list_[int((len(list_)-1)*idx)]

def gen_noise_grid(size, scale_noise=0.7):
    # Generate and layer terrain noise
    base_seed = randint(0, 1_000_000_000)
    noise_grid = np.zeros((size.x, size.y))
    layers = NOISE_LAYERS

    for i in range(layers):
        scale = 0.05 * (2 ** i)  # Adjusted scale factor
        weight = 0.5 ** i  # Weight for blending
        noise_layer = gen_perlin_noise(size, scale * scale_noise, seed=base_seed + i)
        noise_grid += weight * noise_layer

    # Normalize noise values to [0, 1]
    return (noise_grid - np.min(noise_grid)) / (np.max(noise_grid) - np.min(noise_grid))

def gen_planet(size: Vector, wet, temperature):
    srf = pg.Surface(size.tuple, pg.SRCALPHA)
    srf.fill((0,0,0,0))
    water = (0, 0, 255)
    land = list_float_idx(LAND, temperature)
    radius = int(size.x // 2)

    noise_grid = choice(NOISE_CACHE)

    cx, cy = (size / 2).tuple

    def dist(x, y):
        return math.sqrt((x - cx) ** 2 + (y - cy) ** 2)

    # Apply terrain colors based on noise values
    for x in range(size.x):
        for y in range(size.y):
            if dist(x, y) > radius - 1:
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


ID = 0


def nextID():
    global ID
    ID += 1
    return ID

if __name__ == '__main__':
    for i in range(NOISE_CACHE_SIZE):
        print(f'{i}/{NOISE_CACHE_SIZE}')
        save_noise(gen_noise_grid(Vector(NOISE_DIAMETER, NOISE_DIAMETER)))