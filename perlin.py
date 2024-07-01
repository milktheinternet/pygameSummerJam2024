import numpy as np


def lerp(a, b, x):
    return a + x * (b - a)


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def grad(hash, x, y):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else x if h in {12, 14} else 0
    return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)


def perlin(x, y, seed=None):
    if seed is not None:
        np.random.seed(seed)

    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()

    xi = int(x) & 255
    yi = int(y) & 255

    xf = x - int(x)
    yf = y - int(y)

    u = fade(xf)
    v = fade(yf)

    n00 = grad(p[p[xi] + yi], xf, yf)
    n01 = grad(p[p[xi] + yi + 1], xf, yf - 1)
    n10 = grad(p[p[xi + 1] + yi], xf - 1, yf)
    n11 = grad(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)

    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)
    return lerp(x1, x2, v)
