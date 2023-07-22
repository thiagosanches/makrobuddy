import time
import board
import displayio
import gc9a01
import os
import usb_hid
import terminalio
import busio
import rotaryio
import vectorio
import digitalio
import adafruit_imageload
import json
import random

from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_display_text import label, wrap_text_to_lines, wrap_text_to_pixels
from adafruit_bitmap_font import bitmap_font

board_type = os.uname().machine

# Release any resources currently in use for the displays
displayio.release_displays()

time.sleep(1)

print("---Pico Pad Keyboard---")
print(board_type)

# Display something on the LCD
tft_clk = board.GP10
tft_mosi = board.GP11
tft_rst = board.GP12
tft_dc = board.GP8
tft_cs = board.GP9
tft_bl = board.GP25
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=240,
                        height=240, backlight_pin=tft_bl)

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


# Create the sprites (tilegrid)
spriteWidth = 48
spriteHeight = 48

# Since our display is mounted upside down :(
# we have to flip it here on the code.

sprite_happy = displayio.TileGrid(sprite_sheet_happy, pixel_shader=palette_happy,
                                  width=1, height=1, tile_width=spriteWidth, tile_height=spriteHeight)
sprite_happy.flip_y = True

sprite_angry = displayio.TileGrid(sprite_sheet_angry1, pixel_shader=palette_angry1,
                                  width=1, height=1, tile_width=spriteWidth, tile_height=spriteHeight)
sprite_angry.flip_y = True

sprite_angry2 = displayio.TileGrid(sprite_sheet_angry2, pixel_shader=palette_angry2,
                                   width=1, height=1, tile_width=spriteWidth, tile_height=spriteHeight)
sprite_angry2.flip_y = True

sprite_angry3 = displayio.TileGrid(sprite_sheet_angry3, pixel_shader=palette_angry3,
                                   width=1, height=1, tile_width=spriteWidth, tile_height=spriteHeight)
sprite_angry3.flip_y = True

sprite_joy = displayio.TileGrid(sprite_sheet_joy, pixel_shader=palette_joy,
                                width=1, height=1, tile_width=spriteWidth, tile_height=spriteHeight)
sprite_joy.flip_y = True

# The numbers are the total of frames per sprite.
SPRITE_INDEX = 1
SPRITE_TOTAL_FRAMES = 0
sprite_map = {
    (0): (5, sprite_happy),
    (1): (7, sprite_angry),
    (2): (6, sprite_angry2),
    (3): (6, sprite_angry3),
    (4): (8, sprite_joy)
}

# Create a Group to hold the sprite
group = displayio.Group(scale=2)

# Add the sprite to the Group
group.append(sprite_map[0][SPRITE_INDEX])

# Add the Group to the Display
display.show(group)

# Set sprite location
centerX = (240/2-1)
centerY = (240/2-1)

group.x = int((centerX - spriteWidth / 2) - (spriteWidth / 2))
group.y = int((centerX - spriteHeight / 2) - (spriteHeight / 2))
source_index = 0

# END

button = digitalio.DigitalInOut(board.GP22)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
button_state = None

encoder = rotaryio.IncrementalEncoder(board.GP20, board.GP21)
last_position = encoder.position

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# list of pins to use (skipping GP15 on Pico because it's funky)
pins = (
    board.GP0,
    board.GP1,
    board.GP3,
    board.GP4,
    board.GP5,
)

MEDIA = 1
KEY = 2
keymap = {
    (0): (KEY, [Keycode.HOME]),
    (1): (KEY, [Keycode.UP_ARROW]),
    (2): (KEY, [Keycode.LEFT_ARROW]),
    (3): (KEY, [Keycode.DOWN_ARROW]),
    (4): (KEY, [Keycode.RIGHT_ARROW]),
}

switches = []
for i in range(len(pins)):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)

switch_state = [0, 0, 0, 0, 0]

LAST_BLINK_TIME = -1
BLINK_OFF_DURATION = 0.1
TOTAL_CYCLE_PER_SPRITE = 4
CURRENT_SPRITE_OF_CYCLE = 0
total_cycle = 0

while True:
    now = time.monotonic()

    # display some art!!!
    if now >= LAST_BLINK_TIME + BLINK_OFF_DURATION:
        current = sprite_map[CURRENT_SPRITE_OF_CYCLE]
        total_frames = int(current[SPRITE_TOTAL_FRAMES])
        current_sprite = current[SPRITE_INDEX]
        current_sprite[0] = source_index % (total_frames)

        source_index += 1

        if source_index == total_frames:
            source_index = 0
            total_cycle += 1
            if total_cycle == TOTAL_CYCLE_PER_SPRITE:
                total_cycle = 0
                source_index = 0
                group.pop()

                CURRENT_SPRITE_OF_CYCLE = random.randint(0, 4)
                group.append(sprite_map[CURRENT_SPRITE_OF_CYCLE][SPRITE_INDEX])

        LAST_BLINK_TIME = now

        # try:
        #    with open("data.json", "r") as read_file:
        #        data = json.load(read_file)
        #        print(data)
        # except Exception:
        #    pass

    position = encoder.position
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    last_position = current_position

    # Why button is not working?
    # if not button.value and button_state is None:
    #    button_state = "pressed"
    # if button.value and button_state == "pressed":
    #    print("Button pressed.")
    #    cc.send(ConsumerControlCode.PLAY_PAUSE)
    #    button_state = None

    for button in range(len(pins)):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                    else:
                        cc.send(keymap[button][1])
                except ValueError:  # deals w six key limit
                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])

                except ValueError:
                    pass
                switch_state[button] = 0

    # debounce
    time.sleep(0.01)
