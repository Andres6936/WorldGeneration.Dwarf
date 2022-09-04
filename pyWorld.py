import cProfile
import time
from random import randint

import tcod as libtcod

from Source.Biome import BiomeMap
from Source.Civilization import SetupCivs, ProcessCivs, Civ
from Source.Context import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, CIVILIZED_CIVS, TRIBAL_CIVS
from Source.Drainage import DrainageGradMap
from Source.Generation import MasterWorldGen
from Source.GobernmentType import GovernmentType
from Source.HeightGradient import HeightGradMap
from Source.Normal import NormalMap
from Source.Precipitation import PrecipGradMap
from Source.Prosperity import ProsperityGradMap
from Source.Race import Race
from Source.Temperature import TempGradMap
from Source.Terrain import TerrainMap

pr = cProfile.Profile()
pr.enable()


##################################################################################### - Functions - #####################################################################################

# - General Functions -

def ClearConsole():
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            libtcod.console_put_char_ex(0, x, y, ' ', libtcod.black, libtcod.black)

    libtcod.console_flush()

    return


def PointDistRound(pt1x, pt1y, pt2x, pt2y):
    distance = abs(pt2x - pt1x) + abs(pt2y - pt1y);

    distance = round(distance)

    return distance


def FlagGenerator(Color):
    Flag = [[0 for a in range(4)] for b in range(12)]

    BackColor1 = Color
    BackColor2 = Palette[randint(0, len(Palette) - 1)]

    OverColor1 = Palette[randint(0, len(Palette) - 1)]
    OverColor2 = Palette[randint(0, len(Palette) - 1)]

    BackFile = open("Background.txt", 'r')
    OverlayFile = open("Overlay.txt", 'r')

    BTypes = (sum(1 for line in open('Background.txt')) + 1) / 5
    OTypes = (sum(1 for line in open('Overlay.txt')) + 1) / 5

    Back = randint(1, BTypes)
    Overlay = randint(1, OTypes)

    for a in range(53 * (Back - 1)):
        C = BackFile.read(1)

    for a in range(53 * (Overlay - 1)):
        C = OverlayFile.read(1)

    for y in range(4):
        for x in range(12):

            C = BackFile.read(1)
            while C == '\n':
                C = BackFile.read(1)

            if C == '#':
                Flag[x][y] = BackColor1
            elif C == '"':
                Flag[x][y] = BackColor2

            C = OverlayFile.read(1)
            while C == '\n':
                C = OverlayFile.read(1)

            if C == '#':
                Flag[x][y] = OverColor1
            elif C == '"':
                Flag[x][y] = OverColor2

    BackFile.close()
    OverlayFile.close()

    return Flag


def LowestNeighbour(X, Y, World):  # Diagonals are commented for rivers

    minval = 1

    x = 0
    y = 0

    if World[X + 1][Y].height < minval and X + 1 < WORLD_WIDTH:
        minval = World[X + 1][Y].height
        x = X + 1
        y = Y

    if World[X][Y + 1].height < minval and Y + 1 < WORLD_HEIGHT:
        minval = World[X][Y + 1].height
        x = X
        y = Y + 1

    # if libtcod.heightmap_get_value(hm, X + 1, Y + 1) < minval and X + 1 < WORLD_WIDTH and Y + 1 < WORLD_HEIGHT and minval > 0.2:
    # minval = libtcod.heightmap_get_value(hm, X + 1, Y + 1)
    # x = X + 1
    # y = Y + 1

    # if libtcod.heightmap_get_value(hm, X - 1, Y - 1) < minval and X - 1 > 0 and Y - 1 > 0 and minval > 0.2:
    # minval = libtcod.heightmap_get_value(hm, X - 1, Y - 1)
    # x = X - 1
    # y = Y - 1

    if World[X - 1][Y].height < minval and X - 1 > 0:
        minval = World[X - 1][Y].height
        x = X - 1
        y = Y

    if World[X][Y - 1].height < minval and Y - 1 > 0:
        minval = World[X][Y - 1].height
        x = X
        y = Y - 1

    # f libtcod.heightmap_get_value(hm, X + 1, Y - 1) < minval and X + 1 < WORLD_WIDTH and Y - 1 > 0 and minval > 0.2:
    # minval = libtcod.heightmap_get_value(hm, X + 1, Y - 1)
    # x = X + 1
    # y = Y - 1

    # if libtcod.heightmap_get_value(hm, X - 1, Y + 1) < minval and X - 1 > 0 and Y + 1 < WORLD_HEIGHT and minval > 0.2 :
    # minval = libtcod.heightmap_get_value(hm, X - 1, Y + 1)
    # x = X - 1
    # y = Y + 1

    error = 0

    if x == 0 and y == 0:
        error = 1

    return (x, y, error)


# - MapGen Functions -

def PoleGen(hm, NS):
    if NS == 0:
        rng = randint(2, 5)
        for i in range(WORLD_WIDTH):
            for j in range(rng):
                libtcod.heightmap_set_value(hm, i, WORLD_HEIGHT - 1 - j, 0.31)
            rng += randint(1, 3) - 2
            if rng > 6:
                rng = 5
            if rng < 2:
                rng = 2

    if NS == 1:
        rng = randint(2, 5)
        for i in range(WORLD_WIDTH):
            for j in range(rng):
                libtcod.heightmap_set_value(hm, i, j, 0.31)
            rng += randint(1, 3) - 2
            if rng > 6:
                rng = 5
            if rng < 2:
                rng = 2

    return


def ReadRaces():
    RacesFile = 'Races.txt'

    NLines = sum(1 for line in open('Races.txt'))

    NRaces = NLines / 7

    f = open(RacesFile)

    Races = [0 for x in range(NRaces)]

    for x in range(NRaces):  # Reads info between ']' and '\n'
        Info = [0 for a in range(7)]
        for y in range(7):
            data = f.readline()
            start = data.index("]") + 1
            end = data.index("\n", start)
            Info[y] = data[start:end]
        PreferedBiomes = [int(s) for s in str.split(Info[1]) if s.isdigit()]  # Take numbers from string
        Races[x] = Race(Info[0], PreferedBiomes, int(Info[2]), int(Info[3]), int(Info[4]), int(Info[5]), Info[6])

    f.close()

    print('- Races Read -')

    return Races


def ReadGovern():
    GovernFile = 'CivilizedGovernment.txt'

    NLines = sum(1 for line in open('CivilizedGovernment.txt'))

    NGovern = NLines / 5

    f = open(GovernFile)

    Governs = [0 for x in range(NGovern)]

    for x in range(NGovern):  # Reads info between ']' and '\n'
        Info = [0 for a in range(5)]
        for y in range(5):
            data = f.readline()
            start = data.index("]") + 1
            end = data.index("\n", start)
            Info[y] = data[start:end]
        Governs[x] = GovernmentType(Info[0], Info[1], int(Info[2]), int(Info[3]), int(Info[4]))

    f.close()

    print('- Government Types Read -')

    return Governs


def CivGen(Races,
           Govern):  # -------------------------------------------------------------------- * CIV GEN * ----------------------------------------------------------------------------------

    Civs = []

    for x in range(CIVILIZED_CIVS):

        libtcod.namegen_parse('namegen/jice_fantasy.cfg')
        Name = libtcod.namegen_generate('Fantasy male')
        libtcod.namegen_destroy()

        Name += " Civilization"

        Race = Races[randint(0, len(Races) - 1)]
        while Race.Form != "civilized":
            Race = Races[randint(0, len(Races) - 1)]

        Government = Govern[randint(0, len(Govern) - 1)]

        Color = Palette[randint(0, len(Palette) - 1)]

        Flag = FlagGenerator(Color)

        # Initialize Civ
        Civs.append(Civ(Race, Name, Government, Color, Flag, 0))

    for a in range(TRIBAL_CIVS):

        libtcod.namegen_parse('namegen/jice_fantasy.cfg')
        Name = libtcod.namegen_generate('Fantasy male')
        libtcod.namegen_destroy()

        Name += " Tribe"

        Race = Races[randint(0, len(Races) - 1)]
        while Race.Form != "tribal":
            Race = Races[randint(0, len(Races) - 1)]

        Government = GovernmentType("Tribal", "*PLACE HOLDER*", 2, 50, 0)

        Color = libtcod.Color(randint(0, 255), randint(0, 255), randint(0, 255))

        Flag = FlagGenerator(Color)

        # Initialize Civ
        Civs.append(Civ(Race, Name, Government, Color, Flag, 0))

    print('- Civs Generated -')

    return Civs


##################################################################################### - PROCESS CIVS - ##################################################################################


####################################################################################### - MAP MODES - ####################################################################################

# --------------------------------------------------------------------------------- Print Map (Terrain) --------------------------------------------------------------------------------


if __name__ == '__main__':
    # Start Console and set costum font
    libtcod.console_set_custom_font("Andux_cp866ish.png", libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'pyWorld', False,
                              libtcod.RENDERER_SDL)  # Set True for Fullscreen

    # Palette
    Palette = [libtcod.Color(255, 45, 33),  # Red
               libtcod.Color(254, 80, 0),  # Orange
               libtcod.Color(0, 35, 156),  # Blue
               libtcod.Color(71, 45, 96),  # Purple
               libtcod.Color(0, 135, 199),  # Ocean Blue
               libtcod.Color(254, 221, 0),  # Yellow
               libtcod.Color(255, 255, 255),  # White
               libtcod.Color(99, 102, 106)]  # Gray

    # libtcod.sys_set_fps(30)
    # libtcod.console_set_fullscreen(True)

    ################################################################################# - Main Cycle / Input - ##################################################################################

    isRunning: bool = False
    needUpdate: bool = False

    # World Gen
    World = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
    World = MasterWorldGen()

    # Normal Map Initialization
    Chars, Colors = NormalMap(World)

    # Read Races
    Races = ReadRaces()

    # Read Governments
    Govern = ReadGovern()

    # Civ Gen
    Civs = [0 for x in range(CIVILIZED_CIVS + TRIBAL_CIVS)]
    Civs = CivGen(Races, Govern)

    # Setup Civs
    Civs = SetupCivs(Civs, World, Chars, Colors)

    # Print Map
    BiomeMap(Chars, Colors)

    # Month 0
    Month = 0

    # Reset Wars
    Wars = []
    del Wars[:]

    # Select Map Mode
    while not libtcod.console_is_window_closed():

        # Simulation
        while isRunning == True:

            ProcessCivs(World, Civs, Chars, Colors, Month)

            # DEBUG Print Mounth
            Month += 1
            print('Month: ', Month)

            # End Simulation
            libtcod.console_check_for_keypress(True)
            if libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
                timer = 0
                isRunning = False
                print("*PAUSED*")
                time.sleep(1)

            # Flush Console
            if needUpdate:
                BiomeMap(Chars, Colors)
                needUpdate = False

        key = libtcod.console_wait_for_keypress(True)

        # Start Simulation
        if libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
            isRunning = True
            print("*RUNNING*")
            time.sleep(1)

        # Profiler
        if libtcod.console_is_key_pressed(libtcod.KEY_ESCAPE):
            isRunning = False

            pr.disable()
            pr.print_stats(sort='time')

        if key.vk == libtcod.KEY_CHAR:
            if key.c == ord('t'):
                TerrainMap(World)
            elif key.c == ord('h'):
                HeightGradMap(World)
            elif key.c == ord('w'):
                TempGradMap(World)
            elif key.c == ord('p'):
                PrecipGradMap(World)
            elif key.c == ord('d'):
                DrainageGradMap(World)
            elif key.c == ord('f'):
                ProsperityGradMap(World)
            elif key.c == ord('b'):
                BiomeMap(Chars, Colors)
            elif key.c == ord('r'):
                print("\n" * 100)
                print(" * NEW WORLD *")
                Month = 0
                Wars = []
                del Wars[:]
                World = MasterWorldGen()
                Races = ReadRaces()
                Govern = ReadGovern()
                Civs = CivGen(Races, Govern)
                Chars, Colors = NormalMap(World)
                SetupCivs(Civs, World, Chars, Colors)
                BiomeMap(Chars, Colors)
