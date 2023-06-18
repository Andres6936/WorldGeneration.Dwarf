import tcod as libtcod
from tcod.console import Console

from Source.Context import SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH


def BiomeMap(Chars, Colors, console: Console):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            glyph = Chars[x][y]
            if not isinstance(glyph, int):
                glyph = ord(glyph)
            glyph = libtcod.tileset.CHARMAP_CP437[glyph]  # Converts from EASCII to Unicode.
            console.rgb[x, y + SCREEN_HEIGHT // 2 - WORLD_HEIGHT // 2] = glyph, Colors[x][y], libtcod.black
    return
