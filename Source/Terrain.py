from tcod import libtcodpy as libtcod
from tcod.console import Console

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH
from Source.Palette import Palette


def TerrainMap(World, console: Console):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            hm_v = World[x][y].height
            console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('0'), libtcod.blue, libtcod.black
            if hm_v > 0.1:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('1'), libtcod.blue, libtcod.black
            if hm_v > 0.2:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('2'), Palette[0], libtcod.black
            if hm_v > 0.3:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('3'), Palette[0], libtcod.black
            if hm_v > 0.4:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('4'), Palette[0], libtcod.black
            if hm_v > 0.5:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('5'), Palette[0], libtcod.black
            if hm_v > 0.6:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('6'), Palette[0], libtcod.black
            if hm_v > 0.7:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('7'), Palette[0], libtcod.black
            if hm_v > 0.8:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('8'), libtcod.dark_sepia, libtcod.black
            if hm_v > 0.9:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord('9'), libtcod.light_gray, libtcod.black
            if hm_v > 0.99:
                console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = ord(
                    '^'), libtcod.darker_gray, libtcod.black
    return
