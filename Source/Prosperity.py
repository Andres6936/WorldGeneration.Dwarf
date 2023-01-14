from typing import List

import tcod as libtcod

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH
from Source.Model.Tile import Tile


def ProsperityGradMap(
        World):  # ------------------------------------------------------------ Print Map (Prosperity Gradient) white -> low green -> high --------------------------------
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            prosperitynv = World[x][y].prosperity
            prosperitycolor = libtcod.color_lerp(libtcod.white, libtcod.darker_green, prosperitynv)
            libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '\333', prosperitycolor,
                                        libtcod.black)
    libtcod.console_flush()
    return


def Prosperity(World: List[List[Tile]]):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            World[x][y].prosperity = (1.0 - abs(World[x][y].precip - 0.6) + 1.0 - abs(World[x][y].temp - 0.5) +
                                      World[x][y].drainage) / 3

    return
