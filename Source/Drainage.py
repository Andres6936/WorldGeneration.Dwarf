from tcod import libtcodpy as libtcod
from tcod.console import Console

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH


def DrainageGradMap(World, console: Console):
    """
    Print Map (Drainage Gradient) brown -> low white -> high
    """
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            drainv = World[x][y].drainage
            draincolor = libtcod.color_lerp(libtcod.darkest_orange, libtcod.white, drainv)
            console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('█'), draincolor, libtcod.black
    return
