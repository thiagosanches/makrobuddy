import displayio
import adafruit_imageload

ZERO = 0


class Sprite:
    def __init__(self, sprite_sheet_path: str, width: int, height: int, total_frames: int, type: str, velocity: int):
        self.bitmap, self.bitmap_palette = adafruit_imageload.load(
            sprite_sheet_path, bitmap=displayio.Bitmap, palette=displayio.Palette)

        # 00ff00: used as transparent.
        self.bitmap_palette.make_transparent(ZERO)

        self.sprite = displayio.TileGrid(
            self.bitmap, pixel_shader=self.bitmap_palette, width=1, height=1, tile_width=width, tile_height=height)

        # Since our display is mounted upside down,
        # we have to flip it here on the code.
        self.sprite.flip_y = True
        self.type = type
        self.width = width
        self.height = height
        self.velocity = velocity
        self.total_frames = total_frames
