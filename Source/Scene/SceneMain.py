from random import randint
from typing import List

import tcod as libtcod

from Source.Biome import BiomeMap
from Source.Civilization import Civ, SetupCivs
from Source.Context import CIVILIZED_CIVS, SCREEN_HEIGHT, SCREEN_WIDTH, TRIBAL_CIVS, Wars
from Source.Drainage import DrainageGradMap
from Source.Generation import MasterWorldGen
from Source.HeightGradient import HeightGradMap
from Source.Model.GobernmentType import GovernmentType
from Source.Model.Race import Race
from Source.Model.Tile import Tile
from Source.Normal import NormalMap
from Source.Palette import Palette
from Source.Precipitation import PrecipGradMap
from Source.Prosperity import ProsperityGradMap
from Source.Scene.IScene import IScene
from Source.Scene.TypeScene import TypeScene
from Source.Temperature import TempGradMap
from Source.Terrain import TerrainMap


def ClearConsole():
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            libtcod.console_put_char_ex(0, x, y, ' ', libtcod.black, libtcod.black)

    libtcod.console_flush()

    return


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


def ReadRaces():
    RacesFile = 'Races.txt'

    NLines = sum(1 for line in open('Races.txt'))

    NRaces = NLines // 7

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

    NGovern = NLines // 5

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


def CivGen(Races, Govern):
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


class SceneMain(IScene):
    def __init__(self):
        # Start Console and set costum font
        tileSet = libtcod.tileset.load_tilesheet("Andux_cp866ish.png", 16, 16, libtcod.tileset.CHARMAP_CP437)
        self.console = libtcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order='F')
        self.World: List[List[Tile]] = MasterWorldGen()

        # Normal Map Initialization
        self.Chars, self.Colors = NormalMap(self.World)
        # Read Races
        Races = ReadRaces()
        # Read Governments
        Govern = ReadGovern()
        # Civ Gen
        Civs = CivGen(Races, Govern)
        # Setup Civs
        Civs = SetupCivs(Civs, self.World, self.Chars, self.Colors)
        # Print Map
        BiomeMap(self.Chars, self.Colors, self.console)
        # Month 0
        Month = 0
        # Reset Wars
        del Wars[:]
        self.context = libtcod.context.new(columns=self.console.width, rows=self.console.height, tileset=tileSet)

    def events(self):
        for event in libtcod.event.get():
            self.context.convert_event(event)
            if isinstance(event, libtcod.event.Quit):
                isRunning = False
            elif isinstance(event, libtcod.event.KeyDown):
                if event.sym == libtcod.event.KeySym.ESCAPE:
                    isRunning = False
                elif event.sym == libtcod.event.KeySym.t:
                    print("Pressing T")
                    TerrainMap(self.World, self.console)
                elif event.sym == libtcod.event.KeySym.h:
                    print("Pressing H")
                    HeightGradMap(self.World, self.console)
                elif event.sym == libtcod.event.KeySym.w:
                    print("Pressing W")
                    TempGradMap(self.World, self.console)
                elif event.sym == libtcod.event.KeySym.p:
                    print("Pressing P")
                    PrecipGradMap(self.World, self.console)
                elif event.sym == libtcod.event.KeySym.d:
                    print("Pressing D")
                    DrainageGradMap(self.World, self.console)
                elif event.sym == libtcod.event.KeySym.f:
                    print("Pressing F")
                    ProsperityGradMap(self.World, self.console)
                elif event.sym == libtcod.event.KeySym.b:
                    print("Pressing B")
                    BiomeMap(self.Chars, self.Colors, self.console)
                elif event.sym == libtcod.event.KeySym.r:
                    print("Pressing R")
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
                    BiomeMap(Chars, Colors, self.console)
        return TypeScene.NONE

    def draw(self):
        self.context.present(self.console)  # Show the console.

    def clear(self):
        pass
