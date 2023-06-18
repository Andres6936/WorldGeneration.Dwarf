import time
from random import randint
from typing import List

from tcod import libtcodpy as libtcod

from Source.Context import WORLD_HEIGHT, WORLD_WIDTH
from Source.Geometry import PoleGen
from Source.Model.Tile import Tile
from Source.Precipitation import Percipitaion
from Source.Prosperity import Prosperity
from Source.River import RiverGen
from Source.Tectonic import TectonicGen
from Source.Temperature import Temperature
from Source.Typing import HeightmapType


def MasterWorldGen() -> List[List[Tile]]:
    print(' * World Gen START * ')
    StartTime: float = time.time()

    # Heightmap
    hm: HeightmapType = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)

    for i in range(250):
        libtcod.heightmap_add_hill(hm,
                                   randint(WORLD_WIDTH // 10, WORLD_WIDTH - WORLD_WIDTH // 10),
                                   randint(WORLD_HEIGHT // 10, WORLD_HEIGHT - WORLD_HEIGHT // 10),
                                   randint(12, 16),
                                   randint(6, 10))
    print('- Main Hills -')

    for i in range(1000):
        libtcod.heightmap_add_hill(hm,
                                   randint(WORLD_WIDTH // 10, WORLD_WIDTH - WORLD_WIDTH // 10),
                                   randint(WORLD_HEIGHT // 10, WORLD_HEIGHT - WORLD_HEIGHT // 10),
                                   randint(2, 4),
                                   randint(6, 10))
    print('- Small Hills -')

    libtcod.heightmap_normalize(hm, 0.0, 1.0)

    noisehm: HeightmapType = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    noise2d = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
    libtcod.heightmap_add_fbm(noisehm, noise2d, 6, 6, 0, 0, 32, 1, 1)
    libtcod.heightmap_normalize(noisehm, 0.0, 1.0)
    libtcod.heightmap_multiply_hm(hm, noisehm, hm)
    print('- Apply Simplex -')

    PoleGen(hm, 0)
    print('- South Pole -')

    PoleGen(hm, 1)
    print('- North Pole -')

    TectonicGen(hm, 0)
    TectonicGen(hm, 1)
    print('- Tectonic Gen -')

    libtcod.heightmap_rain_erosion(hm, WORLD_WIDTH * WORLD_HEIGHT, 0.07, 0, None)
    print('- Erosion -')

    libtcod.heightmap_clamp(hm, 0.0, 1.0)

    # Temperature
    temp: HeightmapType = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    Temperature(temp, hm)
    libtcod.heightmap_normalize(temp, 0.0, 1.0)
    print('- Temperature Calculation -')

    # Precipitation

    preciphm: HeightmapType = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    Percipitaion(preciphm, temp)
    libtcod.heightmap_normalize(preciphm, 0.0, 1.0)
    print('- Percipitaion Calculation -')

    # Drainage

    drainhm: HeightmapType = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    drain = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
    libtcod.heightmap_add_fbm(drainhm, drain, 2, 2, 0, 0, 32, 1, 1)
    libtcod.heightmap_normalize(drainhm, 0.0, 1.0)
    print('- Drainage Calculation -')

    # VOLCANISM - RARE AT SEA FOR NEW ISLANDS (?) RARE AT MOUNTAINS > 0.9 (?) RARE AT TECTONIC BORDERS (?)

    elapsed_time = time.time() - StartTime
    print(' * World Gen DONE *    in: ', elapsed_time, ' seconds')

    # Initialize Tiles with Map values
    World: List[List[Tile]] = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            World[x][y] = Tile(hm[y, x], temp[y, x], preciphm[y, x], drainhm[y, x], 0)

    print('- Tiles Initialized -')

    # Prosperity

    Prosperity(World)
    print('- Prosperity Calculation -')

    # Biome info to Tile

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):

            if World[x][y].precip >= 0.10 and World[x][y].precip < 0.33 and World[x][y].drainage < 0.5:
                World[x][y].biomeID = 3
                if randint(1, 2) == 2:
                    World[x][y].biomeID = 16

            if World[x][y].precip >= 0.10 and World[x][y].precip > 0.33:
                World[x][y].biomeID = 2
                if World[x][y].precip >= 0.66:
                    World[x][y].biomeID = 1

            if World[x][y].precip >= 0.33 and World[x][y].precip < 0.66 and World[x][y].drainage >= 0.33:
                World[x][y].biomeID = 15
                if randint(1, 5) == 5:
                    World[x][y].biomeID = 5

            if World[x][y].temp > 0.2 and World[x][y].precip >= 0.66 and World[x][y].drainage > 0.33:
                World[x][y].biomeID = 5
                if World[x][y].precip >= 0.75:
                    World[x][y].biomeID = 6
                if randint(1, 5) == 5:
                    World[x][y].biomeID = 15

            if World[x][y].precip >= 0.10 and World[x][y].precip < 0.33 and World[x][y].drainage >= 0.5:
                World[x][y].biomeID = 16
                if randint(1, 2) == 2:
                    World[x][y].biomeID = 14

            if World[x][y].precip < 0.10:
                World[x][y].biomeID = 4
                if World[x][y].drainage > 0.5:
                    World[x][y].biomeID = 16
                    if randint(1, 2) == 2:
                        World[x][y].biomeID = 14
                if World[x][y].drainage >= 0.66:
                    World[x][y].biomeID = 8

            if World[x][y].height <= 0.2:
                World[x][y].biomeID = 0

            if World[x][y].temp <= 0.2 and World[x][y].height > 0.15:
                World[x][y].biomeID = randint(11, 13)

            if World[x][y].height > 0.6:
                World[x][y].biomeID = 9
            if World[x][y].height > 0.9:
                World[x][y].biomeID = 10

    print('- BiomeIDs Atributed -')

    # River Gen
    for x in range(1):
        RiverGen(World)

    print('- River Gen -')
    print(' * Biomes/Rivers Sorted *')
    return World