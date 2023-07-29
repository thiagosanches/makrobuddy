import displayio
import json
import random
import math

from makrobuddy.Sprite import Sprite
from makrobuddy.Tile import Tile

FIRST_SPRITE = 0
CYCLE_PER_SPRITE = 4
SCREEN_LIMIT = 24

EXPLORE_SCREEN_JSON_FIELD = "exploreScreen"
ANIMATIONS_JSON_FIELD = "animations"
TILE_SET_JSON_FIELD = "tileSet"
PATH_JSON_FIELD = "path"
WIDTH_JSON_FIELD = "width"
HEIGHT_JSON_FIELD = "height"
VISIBLE_JSON_FIELD = "visible"
SCENE_JSON_FIELD = "scene"
TOTAL_FRAMES_JSON_FIELD = "total_frames"
TYPE_JSON_FIELD = "type"
VELOCITY_JSON_FIELD = "velocity"


class SpriteManager:
    def __init__(self, character, display_width, display_height):
        self.sprites = {}
        self.current_frame_running_sprite = 0
        self.current_sprite_of_cycle = 0
        self.total_cycle = 0
        self.current_sprite_going_backwards = False
        self.explore_screen = False
        self.last_blink_time = 0
        self.blink_off_duration = 0.1
        self.index_current_running_sprite = 0
        self.position_x_animated = -1
        self.main_group = displayio.Group()
        self.tile_group = None

        with open(f"/sprites/{character}/{character}.json.min", "r") as read_file:
            data = json.load(read_file)
            self.explore_screen = data[EXPLORE_SCREEN_JSON_FIELD]

            is_tile_visible = data[TILE_SET_JSON_FIELD][VISIBLE_JSON_FIELD]
            if is_tile_visible:
                scene = data[TILE_SET_JSON_FIELD][SCENE_JSON_FIELD]
                tile_width = data[TILE_SET_JSON_FIELD][WIDTH_JSON_FIELD]
                tile_height = data[TILE_SET_JSON_FIELD][HEIGHT_JSON_FIELD]

                self.tile_set = Tile(data[TILE_SET_JSON_FIELD][PATH_JSON_FIELD],
                                     math.ceil(display_width / tile_width),
                                     math.ceil(display_height / tile_height),
                                     tile_width,
                                     tile_height,
                                     scene)

                # Create a Group that holds the tile set (to create the 'scenario/scenes').
                self.tile_group = displayio.Group()
                self.tile_group.append(self.tile_set.tile)
                self.main_group.append(self.tile_group)

            for index, item in enumerate(data[ANIMATIONS_JSON_FIELD]):
                self.sprites[index] = Sprite(
                    item[PATH_JSON_FIELD],
                    item[WIDTH_JSON_FIELD],
                    item[HEIGHT_JSON_FIELD],
                    item[TOTAL_FRAMES_JSON_FIELD],
                    item[TYPE_JSON_FIELD],
                    item[VELOCITY_JSON_FIELD])

        # Create a Group that holds the sprite.
        self.sprite_group = displayio.Group(scale=2)

        # Add the first sprite into the Group.
        self.sprite_group.append(self.sprites[FIRST_SPRITE].sprite)

        # Set group sprite location (in the middle of screen).
        self.center_x = (display_width / 2 - 1)
        self.center_y = (display_height / 2 - 1)

        self.sprite_group.x = int(
            (self.center_x - self.sprites[FIRST_SPRITE].width / 2) - (self.sprites[FIRST_SPRITE].width / 2))
        self.sprite_group.y = int(
            (self.center_x - self.sprites[FIRST_SPRITE].height / 2) - (self.sprites[FIRST_SPRITE].height / 2))

        self.main_group.append(self.sprite_group)

    def run(self, now):
        self.last_blink_time = now
        current = self.sprites[self.index_current_running_sprite]

        # If we achieve the total numer of frames of the current sprite, let's change a little bit the animation,
        # or resets if it's not the total cycle per running sprite yet.
        if self.current_frame_running_sprite == current.total_frames:
            self.current_frame_running_sprite = 0
            self.total_cycle = self.total_cycle + 1

            # If it's equal the CYCLE_PER_SPRITE it's time to change the animation!!!
            if self.total_cycle == CYCLE_PER_SPRITE:
                self.total_cycle = 0
                self.current_frame_running_sprite = 0

                # Pops the last sprite appended into that group.
                self.sprite_group.pop()

                # Randomize the next sprite index that will be appended into the sprite group.
                self.index_current_running_sprite = random.randint(
                    0, len(self.sprites) - 1)
                current = self.sprites[self.index_current_running_sprite]
                current.sprite.x = self.position_x_animated

                self.sprite_group.append(current.sprite)

        if self.explore_screen:
            if self.position_x_animated == -1:
                self.position_x_animated = current.sprite.x

            if current.velocity > 0:
                if self.current_sprite_going_backwards:
                    self.position_x_animated -= current.velocity
                else:
                    self.position_x_animated += current.velocity

                if self.position_x_animated >= SCREEN_LIMIT:
                    self.current_sprite_going_backwards = True
                    current.flip_x = True

                if self.position_x_animated <= SCREEN_LIMIT * -1:
                    self.current_sprite_going_backwards = False
                    current.flip_x = False

        current.sprite.x = self.position_x_animated
        current.sprite.flip_x = self.current_sprite_going_backwards
        current.sprite[0] = self.current_frame_running_sprite % current.total_frames
        self.current_frame_running_sprite = self.current_frame_running_sprite + 1
