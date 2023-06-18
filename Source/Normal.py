from random import randint
from typing import List

from tcod import libtcodpy as libtcod

from Source.Context import WORLD_HEIGHT, WORLD_WIDTH
from Source.Model.Tile import Tile


def NormalMap(World: List[List[Tile]]):
    Chars = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
    Colors = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]

    def SymbolDictionary(x):
        char = ''
        if x == 15 or x == 8:
            if randint(1, 2) == 2:
                char = 251
            else:
                char = ','
        if x == 1:
            if randint(1, 2) == 2:
                char = 244
            else:
                char = 131
        if x == 2:
            if randint(1, 2) == 2:
                char = '"'
            else:
                char = 163
        return {
            0: '\367',
            1: char,
            2: char,
            3: 'n',
            4: '\367',
            5: 24,
            6: 6 - randint(0, 1),
            8: char,
            9: 127,
            10: 30,
            11: 176,
            12: 177,
            13: 178,
            14: 'n',
            15: char,
            16: 139
        }[x]

    def ColorDictionary(x):
        badlands = libtcod.Color(204, 159, 81)
        icecolor = libtcod.Color(176, 223, 215)
        darkgreen = libtcod.Color(68, 158, 53)
        lightgreen = libtcod.Color(131, 212, 82)
        water = libtcod.Color(13, 103, 196)
        mountain = libtcod.Color(185, 192, 162)
        desert = libtcod.Color(255, 218, 90)
        return {
            0: water,
            1: darkgreen,
            2: lightgreen,
            3: lightgreen,
            4: desert,
            5: darkgreen,
            6: darkgreen,
            8: badlands,
            9: mountain,
            10: mountain,
            11: icecolor,
            12: icecolor,
            13: icecolor,
            14: darkgreen,
            15: lightgreen,
            16: darkgreen
        }[x]

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            Chars[x][y] = SymbolDictionary(World[x][y].biomeID)
            Colors[x][y] = ColorDictionary(World[x][y].biomeID)
            if World[x][y].hasRiver:
                Chars[x][y] = 'o'
                Colors[x][y] = libtcod.light_blue

    return Chars, Colors
