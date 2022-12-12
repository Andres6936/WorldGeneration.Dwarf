import tcod as libtcod
from tcod import Console

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH


def BiomeMap(Chars, Colors, console: Console):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            console.print(x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, str(Chars[x][y]), Colors[x][y], libtcod.black)
            libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, Chars[x][y], Colors[x][y],
                                        libtcod.black)

    libtcod.console_flush()
    return
