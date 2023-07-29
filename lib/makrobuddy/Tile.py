import displayio
import adafruit_imageload

ZERO = 0


class Tile:
    def __init__(self, tile_sheet_path: str, quantity_x: int, quantity_y: int, width: int, height: int, scene: dict):
        self.bitmap, self.bitmap_palette = adafruit_imageload.load(
            tile_sheet_path, bitmap=displayio.Bitmap, palette=displayio.Palette)

        # 00ff00: used as transparent.
        self.bitmap_palette.make_transparent(ZERO)

        self.tile = displayio.TileGrid(
            self.bitmap, pixel_shader=self.bitmap_palette, width=quantity_x, height=quantity_y, tile_width=width, tile_height=height)

        # Since our display is mounted upside down,
        # we have to flip it here on the code.
        self.tile.flip_y = True
        self.type = type
        self.width = width
        self.height = height

        # PLEASE, refactor me!
        for idx, scenes in enumerate(scene):
            for idx_x, x in enumerate(scenes):
                for idx_y, y in enumerate(x.split(";")):
                    self.tile[idx_x, idx_y] = int(y)
