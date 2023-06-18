from tcod import libtcodpy as libtcod
from tcod.console import Console

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH


def HeightGradMap(World, console: Console):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            hm_v = World[x][y].height
            HeightColor = libtcod.Color(255, 255, 255)
            # Set lightness to hm_v so higher heightmap value -> "whiter"
            libtcod.color_set_hsv(HeightColor, 0, 0, hm_v)
            console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('█'), HeightColor, libtcod.black
    return
