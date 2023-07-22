import adafruit_imageload
import displayio
import json


class SpriteManager:
    def __init__(self, character):
        self.sprites = {}
        self.source_index = 0

        self.sprite_width = 48
        self.sprite_height = 48

        self.sprite_total_frames = 0
        self.sprite_index = 1
        self.sprite_width = 2
        self.sprite_height = 3

        # To control the animation.
        self.last_blink_time = -1
        self.blink_off_duration = 0.1
        self.total_cycle_per_sprite = 4
        self.current_sprite_of_cycle = 0
        self.total_cycle = 0

        with open(f"/sprites/{character}/{character}.json", "r") as read_file:
            data = json.load(read_file)
            index = 0
            for item in data:
                print(item['animation'])

                sprite_sheet, palette = adafruit_imageload.load(
                    item["path"], bitmap=displayio.Bitmap, palette=displayio.Palette)
                palette.make_transparent(0)

                # Since our display is mounted upside down :(
                # we have to flip it here on the code.
                sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette, width=1,
                                            height=1, tile_width=item["width"], tile_height=item["height"])
                sprite.flip_y = True

                self.sprites[index] = (
                    item["total_frames"], sprite, item["width"], item["height"])
                index += 1

    def get_sprite_width(self):
        current = self.sprites[self.current_sprite_of_cycle]
        return current[self.sprite_width]

    def get_sprite_height(self):
        current = self.sprites[self.current_sprite_of_cycle]
        return current[self.sprite_height]

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
