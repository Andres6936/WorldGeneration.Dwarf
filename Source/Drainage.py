import tcod as libtcod

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH


def DrainageGradMap(
        World):  # ------------------------------------------------------------ Print Map (Drainage Gradient) brown -> low white -> high --------------------------------
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            drainv = World[x][y].drainage
            draincolor = libtcod.color_lerp(libtcod.darkest_orange, libtcod.white, drainv)
            libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '\333', draincolor,
                                        libtcod.black)
    libtcod.console_flush()
    return
