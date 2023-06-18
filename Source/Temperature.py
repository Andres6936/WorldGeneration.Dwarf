from tcod import libtcodpy as libtcod
from tcod.console import Console

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH
from Source.Typing import HeightmapType


def TempGradMap(World, console: Console):
    """
    Print Map (Surface Temperature Gradient) white -> cold red -> warm
    """
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            tempv = World[x][y].temp
            tempcolor = libtcod.color_lerp(libtcod.white, libtcod.red, tempv)
            console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('█'), tempcolor, libtcod.black
    return


def Temperature(temp: HeightmapType, hm: HeightmapType):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            heighteffect = 0
            if y > WORLD_HEIGHT / 2:
                libtcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT - y - heighteffect)
            else:
                libtcod.heightmap_set_value(temp, x, y, y - heighteffect)
            heighteffect = libtcod.heightmap_get_value(hm, x, y)
            if heighteffect > 0.8:
                heighteffect = heighteffect * 5
                if y > WORLD_HEIGHT / 2:
                    libtcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT - y - heighteffect)
                else:
                    libtcod.heightmap_set_value(temp, x, y, y - heighteffect)
            if heighteffect < 0.25:
                heighteffect = heighteffect * 10
                if y > WORLD_HEIGHT / 2:
                    libtcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT - y - heighteffect)
                else:
                    libtcod.heightmap_set_value(temp, x, y, y - heighteffect)

    return
