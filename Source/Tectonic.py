from random import randint, uniform
from typing import Literal

from tcod import libtcodpy as libtcod

from Source.Context import WORLD_HEIGHT, WORLD_WIDTH
from Source.Typing import HeightmapType


def TectonicGen(hm: HeightmapType, hor: Literal[0, 1]):
    TecTiles = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]

    # Define Tectonic Borders
    if hor == 1:
        pos = randint(WORLD_HEIGHT // 10, WORLD_HEIGHT - WORLD_HEIGHT // 10)
        for x in range(WORLD_WIDTH):
            TecTiles[x][pos] = 1
            pos += randint(1, 5) - 3
            if pos < 0:
                pos = 0
            if pos > WORLD_HEIGHT - 1:
                pos = WORLD_HEIGHT - 1
    if hor == 0:
        pos = randint(WORLD_WIDTH // 10, WORLD_WIDTH - WORLD_WIDTH // 10)
        for y in range(WORLD_HEIGHT):
            TecTiles[pos][y] = 1
            pos += randint(1, 5) - 3
            if pos < 0:
                pos = 0
            if pos > WORLD_WIDTH - 1:
                pos = WORLD_WIDTH - 1

                # Apply elevation to borders
    for x in range(WORLD_WIDTH // 10, WORLD_WIDTH - WORLD_WIDTH // 10):
        for y in range(WORLD_HEIGHT // 10, WORLD_HEIGHT - WORLD_HEIGHT // 10):
            if TecTiles[x][y] == 1 and libtcod.heightmap_get_value(hm, x, y) > 0.3:
                libtcod.heightmap_add_hill(hm, x, y, randint(2, 4), uniform(0.15, 0.18))

    return
