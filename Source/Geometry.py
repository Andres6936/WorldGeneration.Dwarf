from random import randint
from typing import List, Literal

from tcod import libtcodpy as libtcod

from Source.Context import WORLD_HEIGHT, WORLD_WIDTH
from Source.Model.Tile import Tile
from Source.Typing import HeightmapType


def PointDistRound(pt1x, pt1y, pt2x, pt2y):
    distance = abs(pt2x - pt1x) + abs(pt2y - pt1y);

    distance = round(distance)

    return distance


def LowestNeighbour(X: int, Y: int, World: List[List[Tile]]):  # Diagonals are commented for rivers

    minval = 1

    x = 0
    y = 0

    if World[X + 1][Y].height < minval and X + 1 < WORLD_WIDTH:
        minval = World[X + 1][Y].height
        x = X + 1
        y = Y

    if World[X][Y + 1].height < minval and Y + 1 < WORLD_HEIGHT:
        minval = World[X][Y + 1].height
        x = X
        y = Y + 1

    # if libtcod.heightmap_get_value(hm, X + 1, Y + 1) < minval and X + 1 < WORLD_WIDTH and Y + 1 < WORLD_HEIGHT and minval > 0.2:
    # minval = libtcod.heightmap_get_value(hm, X + 1, Y + 1)
    # x = X + 1
    # y = Y + 1

    # if libtcod.heightmap_get_value(hm, X - 1, Y - 1) < minval and X - 1 > 0 and Y - 1 > 0 and minval > 0.2:
    # minval = libtcod.heightmap_get_value(hm, X - 1, Y - 1)
    # x = X - 1
    # y = Y - 1

    if World[X - 1][Y].height < minval and X - 1 > 0:
        minval = World[X - 1][Y].height
        x = X - 1
        y = Y

    if World[X][Y - 1].height < minval and Y - 1 > 0:
        minval = World[X][Y - 1].height
        x = X
        y = Y - 1

    # f libtcod.heightmap_get_value(hm, X + 1, Y - 1) < minval and X + 1 < WORLD_WIDTH and Y - 1 > 0 and minval > 0.2:
    # minval = libtcod.heightmap_get_value(hm, X + 1, Y - 1)
    # x = X + 1
    # y = Y - 1

    # if libtcod.heightmap_get_value(hm, X - 1, Y + 1) < minval and X - 1 > 0 and Y + 1 < WORLD_HEIGHT and minval > 0.2 :
    # minval = libtcod.heightmap_get_value(hm, X - 1, Y + 1)
    # x = X - 1
    # y = Y + 1

    error = 0

    if x == 0 and y == 0:
        error = 1

    return x, y, error


def PoleGen(hm: HeightmapType, NS: Literal[0, 1]):
    if NS == 0:
        rng = randint(2, 5)
        for i in range(WORLD_WIDTH):
            for j in range(rng):
                libtcod.heightmap_set_value(hm, i, WORLD_HEIGHT - 1 - j, 0.31)
            rng += randint(1, 3) - 2
            if rng > 6:
                rng = 5
            if rng < 2:
                rng = 2

    if NS == 1:
        rng = randint(2, 5)
        for i in range(WORLD_WIDTH):
            for j in range(rng):
                libtcod.heightmap_set_value(hm, i, j, 0.31)
            rng += randint(1, 3) - 2
            if rng > 6:
                rng = 5
            if rng < 2:
                rng = 2

    return
