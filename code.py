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

from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_display_text import label
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
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=tft_bl)

# Draw a text label

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("/cp_sprite_sheet2.bmp",bitmap=displayio.Bitmap,palette=displayio.Palette)
palette.make_transparent(0)


# Create a sprite (tilegrid)
spriteWidth = 16
spriteHeight = 16

sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = spriteWidth,
                            tile_height = spriteHeight)


# Create a Group to hold the sprite
group = displayio.Group(scale=2)

# Add the sprite to the Group
group.append(sprite)

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
BLINK_OFF_DURATION = 0.5

while True:    
    # display some art!!!
    now = time.monotonic()
    # Is it time to switch the sprite?
    if now >= LAST_BLINK_TIME + BLINK_OFF_DURATION:
        sprite[0] = source_index % 6
        source_index += 1
        LAST_BLINK_TIME = now

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
    #if not button.value and button_state is None:
    #    button_state = "pressed"
    #if button.value and button_state == "pressed":
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

    time.sleep(0.01)  # debounce



