import tcod as libtcod

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH


def HeightGradMap(
        World):  # ------------------------------------------------------------ Print Map (Heightmap Gradient) -------------------------------------------------------------------
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            hm_v = World[x][y].height
            HeightColor = libtcod.Color(255, 255, 255)
            libtcod.color_set_hsv(HeightColor, 0, 0,
                                  hm_v)  # Set lightness to hm_v so higher heightmap value -> "whiter"
            libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2, '\333', HeightColor,
                                        libtcod.black)
    libtcod.console_flush()
    return
