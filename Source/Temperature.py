import tcod as libtcod

from pyWorld import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_HEIGHT


def TempGradMap(
        World):  # ------------------------------------------------------------ Print Map (Surface Temperature Gradient) white -> cold red -> warm --------------------------------
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            tempv = World[x][y].temp
            tempcolor = libtcod.color_lerp(libtcod.white, libtcod.red, tempv)
            libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT / 2 - WORLD_HEIGHT / 2, '\333', tempcolor,
                                        libtcod.black)
    libtcod.console_flush()
    return


def Temperature(temp, hm):
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
