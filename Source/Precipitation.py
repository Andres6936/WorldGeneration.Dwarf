import tcod as libtcod

from pyWorld import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_HEIGHT


def PrecipGradMap(
        World):  # ------------------------------------------------------------ Print Map (Precipitation Gradient) white -> low blue -> high --------------------------------
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            tempv = World[x][y].precip
            tempcolor = libtcod.color_lerp(libtcod.white, libtcod.light_blue, tempv)
            libtcod.console_put_char_ex(0, x, y + SCREEN_HEIGHT / 2 - WORLD_HEIGHT / 2, '\333', tempcolor,
                                        libtcod.black)
    libtcod.console_flush()
    return


def Percipitaion(preciphm, temphm):
    libtcod.heightmap_add(preciphm, 2)

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            temp = libtcod.heightmap_get_value(temphm, x, y)

    precip = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)

    libtcod.heightmap_add_fbm(preciphm, precip, 2, 2, 0, 0, 32, 1, 1)

    libtcod.heightmap_normalize(preciphm, 0.0, 1.0)

    return
