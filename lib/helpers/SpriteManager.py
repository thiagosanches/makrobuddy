import adafruit_imageload
import displayio
import json
import random
from makrobuddy.Sprite import Sprite

FIRST = 0
CYCLE_PER_SPRITE = 4
SCREEN_LIMIT = 24


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

        with open(f"/sprites/{character}/{character}.json", "r") as read_file:
            data = json.load(read_file)
            self.explore_screen = data["exploreScreen"]

            for index, item in enumerate(data["animations"]):
                self.sprites[index] = Sprite(
                    item["path"], item["width"], item["height"], item["total_frames"], item["type"], item["velocity"])

        # Create a Group that holds the sprite.
        self.sprite_group = displayio.Group(scale=2)

        # Add the first sprite into the Group.
        self.sprite_group.append(self.sprites[FIRST].sprite)

        # Set group sprite location (in the middle of screen).
        self.center_x = (display_width / 2 - 1)
        self.center_y = (display_height / 2 - 1)

        self.sprite_group.x = int((self.center_x - self.sprites[FIRST].sprite.width / 2) - (self.sprites[FIRST].sprite.width / 2))
        self.sprite_group.y = int((self.center_x - self.sprites[FIRST].sprite.height / 2) - (self.sprites[FIRST].sprite.height / 2))

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
                print("TROCOU")
                self.total_cycle = 0
                self.current_frame_running_sprite = 0

                self.sprite_group.pop()

                # Randomize the next sprite index that will be appended into the sprite group.
                self.index_current_running_sprite = random.randint(
                    0, len(self.sprites) - 1)
                current.sprite = self.sprites[self.index_current_running_sprite].sprite
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

        print(current.type)
        print(self.current_frame_running_sprite % current.total_frames)
        print(self.current_frame_running_sprite)
        
        current.sprite.x = self.position_x_animated
        current.sprite.flip_x = self.current_sprite_going_backwards
        current.sprite[0] = self.current_frame_running_sprite % current.total_frames
        self.current_frame_running_sprite = self.current_frame_running_sprite + 1
        
        
