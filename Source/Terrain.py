import tcod as libtcod

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH
from Source.Palette import Palette


def TerrainMap(World):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            hm_v = World[x][y].height
            libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '0', libtcod.blue,
                                        libtcod.black)
            if hm_v > 0.1:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '1', libtcod.blue,
                                            libtcod.black)
            if hm_v > 0.2:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '2', Palette[0],
                                            libtcod.black)
            if hm_v > 0.3:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '3', Palette[0],
                                            libtcod.black)
            if hm_v > 0.4:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '4', Palette[0],
                                            libtcod.black)
            if hm_v > 0.5:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '5', Palette[0],
                                            libtcod.black)
            if hm_v > 0.6:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '6', Palette[0],
                                            libtcod.black)
            if hm_v > 0.7:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '7', Palette[0],
                                            libtcod.black)
            if hm_v > 0.8:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '8', libtcod.dark_sepia,
                                            libtcod.black)
            if hm_v > 0.9:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '9', libtcod.light_gray,
                                            libtcod.black)
            if hm_v > 0.99:
                libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '^', libtcod.darker_gray,
                                            libtcod.black)
    libtcod.console_flush()
    return
