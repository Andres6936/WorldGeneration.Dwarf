class Tile:
    def __init__(self, height: float, temp: float, precip: float, drainage: float, biome: int):
        self.temp = temp
        self.height = height
        self.precip = precip
        self.drainage = drainage
        self.biome = biome
        self.hasRiver = False
        self.isCiv = False
        self.biomeID = 0
        self.prosperity = 0
