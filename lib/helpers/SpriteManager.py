import adafruit_imageload
import displayio


class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.source_index = 0

        self.sprite_width = 48
        self.sprite_height = 48

        self.sprite_index = 1
        self.sprite_total_frames = 0

        # To control the animation.
        self.last_blink_time = -1
        self.blink_off_duration = 0.1
        self.total_cycle_per_sprite = 4
        self.current_sprite_of_cycle = 0
        self.total_cycle = 0

        # Load the sprite sheet 1 (bitmap)
        sprite_sheet_happy, palette_happy = adafruit_imageload.load(
            "/sprites/sun-sprite-happy.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_happy.make_transparent(0)

        # Load the sprite sheet 2 (bitmap)
        sprite_sheet_angry1, palette_angry1 = adafruit_imageload.load(
            "/sprites/sun-sprite-angry.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_angry1.make_transparent(0)

        # Load the sprite sheet 3 (bitmap)
        sprite_sheet_angry2, palette_angry2 = adafruit_imageload.load(
            "/sprites/sun-sprite-angry2.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_angry2.make_transparent(0)

        # Load the sprite sheet 4 (bitmap)
        sprite_sheet_angry3, palette_angry3 = adafruit_imageload.load(
            "/sprites/sun-sprite-angry3.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_angry3.make_transparent(0)

        # Load the sprite sheet 5 (bitmap)
        sprite_sheet_joy, palette_joy = adafruit_imageload.load(
            "/sprites/sun-sprite-joy.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_joy.make_transparent(0)

        # Since our display is mounted upside down :(
        # we have to flip it here on the code.

        sprite_happy = displayio.TileGrid(sprite_sheet_happy, pixel_shader=palette_happy,
                                          width=1, height=1, tile_width=self.sprite_width, tile_height=self.sprite_height)
        sprite_happy.flip_y = True

        sprite_angry = displayio.TileGrid(sprite_sheet_angry1, pixel_shader=palette_angry1,
                                          width=1, height=1, tile_width=self.sprite_width, tile_height=self.sprite_height)
        sprite_angry.flip_y = True

        sprite_angry2 = displayio.TileGrid(sprite_sheet_angry2, pixel_shader=palette_angry2,
                                           width=1, height=1, tile_width=self.sprite_width, tile_height=self.sprite_height)
        sprite_angry2.flip_y = True

        sprite_angry3 = displayio.TileGrid(sprite_sheet_angry3, pixel_shader=palette_angry3,
                                           width=1, height=1, tile_width=self.sprite_width, tile_height=self.sprite_height)
        sprite_angry3.flip_y = True

        sprite_joy = displayio.TileGrid(sprite_sheet_joy, pixel_shader=palette_joy,
                                        width=1, height=1, tile_width=self.sprite_width, tile_height=self.sprite_height)
        sprite_joy.flip_y = True

        self.sprites = {
            (0): (5, sprite_happy),
            (1): (7, sprite_angry),
            (2): (6, sprite_angry2),
            (3): (6, sprite_angry3),
            (4): (8, sprite_joy)
        }

    def get_sprite_width(self):
        return self.sprite_width

    def get_sprite_height(self):
        return self.sprite_height
    
    def get_last_blink_time(self):
        return self.last_blink_time
    
    def set_last_blink_time(self, value):
        self.last_blink_time = value
    
    def get_blink_off_duration(self):
        return self.blink_off_duration

    def get_current_sprite(self):
        current = self.sprites[self.current_sprite_of_cycle]
        return current[self.sprite_index]
    
    def get_total_frames_of_current_sprite(self):
        current = self.sprites[self.current_sprite_of_cycle]
        return int(current[self.sprite_total_frames])
    
    def set_current_sprite_of_cycle(self, value):
        self.current_sprite_of_cycle = value

    def get_current_sprite_of_cycle(self):
        return self.current_sprite_of_cycle

    def get_source_index(self):
        return self.source_index
    
    def set_source_index(self, value):
        self.source_index = value

    def change_frame_current_sprite(self):
        current = self.get_current_sprite()
        current[0] = self.source_index % self.get_total_frames_of_current_sprite()
        self.set_source_index(self.get_source_index() + 1)

    def get_all_sprites(self):
        return self.sprites
    
    def get_total_cycle(self):
        return self.total_cycle

    def set_total_cycle(self, value):
        self.total_cycle = value

    def get_total_cycle_per_sprite(self):
        return self.total_cycle_per_sprite
    
    def get_sprite_index(self):
        return self.sprite_index
