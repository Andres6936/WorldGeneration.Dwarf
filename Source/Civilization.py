from random import randint

import Source.Army
import Source.Race
from Source.Army import Army
from Source.Generation import NewSite
from Source.War import War
from pyWorld import WORLD_WIDTH, WORLD_HEIGHT, CIVILIZED_CIVS, TRIBAL_CIVS, CIV_MAX_SITES, PointDistRound, WAR_DISTANCE, \
    Wars


def SetupCivs(Civs, World, Chars, Colors):
    for x in range(len(Civs)):

        Civs[x].Sites = []
        Civs[x].SuitableSites = []

        del Civs[x].SuitableSites[:]

        # Civs[x].PrintInfo()

        for i in range(WORLD_WIDTH):
            for j in range(WORLD_HEIGHT):
                for g in range(len(Source.Race.Race.PrefBiome)):
                    if World[i][j].biomeID == Source.Race.Race.PrefBiome[g]:
                        Civs[x].SuitableSites.append(CivSite(i, j, "", 1, 0))

        rand = randint(0, len(Civs[x].SuitableSites) - 1)
        while World[Civs[x].SuitableSites[rand].x][Civs[x].SuitableSites[rand].y].isCiv == True:
            del Civs[x].SuitableSites[rand]
            rand = randint(0, len(Civs[x].SuitableSites) - 1)

        X = Civs[x].SuitableSites[rand].x
        Y = Civs[x].SuitableSites[rand].y

        World[X][Y].isCiv = True

        FinalProsperity = World[X][Y].prosperity * 150
        if World[X][Y].hasRiver:
            FinalProsperity = FinalProsperity * 1.5
        PopCap = 4 * Source.Race.Race.ReproductionSpeed + FinalProsperity
        PopCap = PopCap * 2  # Capital Bonus
        PopCap = round(PopCap)

        Civs[x].Sites.append(CivSite(X, Y, "Village", 0, PopCap))

        Civs[x].Sites[0].isCapital = True

        Civs[x].Sites[0].Population = 20

        Chars[X][Y] = 31
        Colors[X][Y] = Civs[x].Color

        Civs[x].PrintInfo()

    print('- Civs Setup -')

    print(' * Civ Gen DONE *')

    return Civs


def ProcessCivs(World, Civs, Chars, Colors, Month):
    print("------------------------------------------")

    for x in range(CIVILIZED_CIVS + TRIBAL_CIVS):

        print(Civs[x].Name)
        print(Source.Race.Race.Name)

        Civs[x].TotalPopulation = 0

        # Site
        for y in range(len(Civs[x].Sites)):

            # Population
            NewPop = int(round(Civs[x].Sites[y].Population * Source.Race.Race.ReproductionSpeed / 1500))

            if Civs[x].Sites[y].Population > Civs[x].Sites[y].popcap / 2:
                NewPop /= 6

            Civs[x].Sites[y].Population += NewPop

            # Expand
            if Civs[x].Sites[y].Population > Civs[x].Sites[y].popcap:
                Civs[x].Sites[y].Population = int(round(Civs[x].Sites[y].popcap))
                if len(Civs[x].Sites) < CIV_MAX_SITES:
                    Civs[x].Sites[y].Population = int(round(Civs[x].Sites[y].popcap / 2))
                    Civs[x] = NewSite(Civs[x], Civs[x].Sites[y], World, Chars, Colors)

            Civs[x].TotalPopulation += Civs[x].Sites[y].Population

            # Diplomacy
            for a in range(CIVILIZED_CIVS + TRIBAL_CIVS):
                for b in range(len(Civs[a].Sites)):
                    if x == a:
                        break
                    if PointDistRound(Civs[x].Sites[y].x, Civs[x].Sites[y].y, Civs[a].Sites[b].x,
                                      Civs[a].Sites[b].y) < WAR_DISTANCE:
                        AlreadyWar = False
                        for c in range(len(Wars)):
                            if (Wars[c].Side1 == Civs[x] and Wars[c].Side2 == Civs[a]) or (
                                    Wars[c].Side1 == Civs[a] and Wars[c].Side2 == Civs[x]):
                                # Already at War
                                AlreadyWar = True
                        if AlreadyWar == False:
                            # Start War and form armies if dot have army yet
                            Wars.append(War(Civs[x], Civs[a]))
                            if Civs[a].atWar == False:  # if not already at war form new army
                                Source.Army.Army = Army(Civs[a].Sites[0].x,
                                                        Civs[a].Sites[0].y,
                                                        Civs[a],
                                                        Civs[a].TotalPopulation * Civs[
                                                            a].Government.Militarization / 100)
                                Civs[a].atWar = True
                            if Civs[x].atWar == False:  # if not already at war form new army
                                Source.Army.Army = Army(Civs[x].Sites[0].x,
                                                        Civs[x].Sites[0].y,
                                                        Civs[x],
                                                        Civs[x].TotalPopulation * Civs[
                                                            x].Government.Militarization / 100)
                                Civs[x].atWar = True

            print("X:", Civs[x].Sites[y].x, "Y:", Civs[x].Sites[y].y, "Population:", Civs[x].Sites[y].Population)

        print(Source.Army.Army.x, Source.Army.Army.y, Source.Army.Army.Size, '\n')

    return


class CivSite:

    def __init__(self, x, y, category, suitable, popcap):
        self.x = x
        self.y = y
        self.category = category
        self.suitable = suitable
        self.popcap = popcap

    Population = 0

    isCapital = False


class Civ:

    def __init__(self, Race, Name, Government, Color, Flag, Aggression):
        self.Name = Name
        self.Race = Race
        self.Government = Government
        self.Color = Color
        self.Flag = Flag
        self.Aggression = Race.Aggressiveness + Government.Aggressiveness

    def PrintInfo(self):
        print(self.Name)
        print(self.Race.Name)
        print(self.Government.Name)
        print('Aggression:', self.Aggression)
        print('Suitable Sites:', len(self.SuitableSites), '\n')

    Sites = []
    SuitableSites = []

    atWar = False

    Army = Army(None, None, None, None)
    TotalPopulation = 0
