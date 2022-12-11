from random import randint

import Source.Model.Race
from Source.Context import EXPANSION_DISTANCE
from Source.Geometry import PointDistRound


def NewSite(Civ, Origin, World, Chars, Colors):
    rand = randint(0, len(Civ.SuitableSites) - 1)

    Tries = 0

    while PointDistRound(Origin.x, Origin.y, Civ.SuitableSites[rand].x,
                         Civ.SuitableSites[rand].y) > EXPANSION_DISTANCE or World[Civ.SuitableSites[rand].x][
        Civ.SuitableSites[rand].y].isCiv:
        if Tries > 200:
            return Civ
        Tries += 1
        rand = randint(0, len(Civ.SuitableSites) - 1)

    X = Civ.SuitableSites[rand].x
    Y = Civ.SuitableSites[rand].y

    World[X][Y].isCiv = True

    FinalProsperity = World[X][Y].prosperity * 150
    if World[X][Y].hasRiver:
        FinalProsperity = FinalProsperity * 1.5
    PopCap = 3 * Source.Model.Race.Race.ReproductionSpeed + FinalProsperity
    PopCap = round(PopCap)

    Civ.Sites.append(CivSite(X, Y, "Village", 0, PopCap))

    Civ.Sites[len(Civ.Sites) - 1].Population = 20

    Chars[X][Y] = 31
    Colors[X][Y] = Civ.Color

    global needUpdate
    needUpdate = True

    return Civ


class CivSite:

    def __init__(self, x, y, category, suitable, popcap):
        self.x = x
        self.y = y
        self.category = category
        self.suitable = suitable
        self.popcap = popcap

    Population = 0

    isCapital = False
