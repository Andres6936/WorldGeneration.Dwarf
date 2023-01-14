from random import randint
from typing import List

from Source.Context import MIN_RIVER_LENGHT, WORLD_HEIGHT, WORLD_WIDTH
from Source.Geometry import LowestNeighbour
from Source.Model.Tile import Tile


def RiverGen(World: List[List[Tile]]):
    X = randint(0, WORLD_WIDTH - 1)
    Y = randint(0, WORLD_HEIGHT - 1)

    XCoor = []
    YCoor = []

    tries = 0

    prev = ""

    while World[X][Y].height < 0.8:
        tries += 1
        X = randint(0, WORLD_WIDTH - 1)
        Y = randint(0, WORLD_HEIGHT - 1)

        if tries > 2000:
            return

    del XCoor[:]
    del YCoor[:]

    XCoor.append(X)
    YCoor.append(Y)

    while World[X][Y].height >= 0.2:

        X, Y, error = LowestNeighbour(X, Y, World)

        if error == 1:
            return

        try:
            if World[X][Y].hasRiver or World[X + 1][Y].hasRiver or World[X - 1][Y].hasRiver or World[X][
                Y + 1].hasRiver or World[X][Y - 1].hasRiver:
                break
        except IndexError:
            return

        if X in XCoor and Y in YCoor:
            break

        XCoor.append(X)
        YCoor.append(Y)

    if len(XCoor) <= MIN_RIVER_LENGHT:
        return

    for x in range(len(XCoor)):
        if World[XCoor[x]][YCoor[x]].height < 0.2:
            break
        World[XCoor[x]][YCoor[x]].hasRiver = True
        if World[XCoor[x]][YCoor[x]].height >= 0.2 and x == len(XCoor):
            World[XCoor[x]][YCoor[x]].hasRiver = True  # Change to Lake later

    return
