class Tile:
    def __init__(self, height: float, temp: float, precip: float, drainage: float, biome):
        self.temp = temp
        self.height = height
        self.precip = precip
        self.drainage = drainage
        self.biome = biome

    hasRiver = False
    isCiv = False

    biomeID = 0
    prosperity = 0
