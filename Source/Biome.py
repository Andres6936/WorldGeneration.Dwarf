import tcod as libtcod

from pyWorld import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_HEIGHT


def BiomeMap(Chars, Colors):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT / 2 - WORLD_HEIGHT / 2, Chars[x][y], Colors[x][y],
                                        libtcod.black)

    libtcod.console_flush()
    return
