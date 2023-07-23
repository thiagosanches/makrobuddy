import time
import board
import displayio
import os
import usb_hid
import rotaryio
import digitalio
import random

from lib.helpers.TextManager import TextManager
from lib.helpers.SpriteManager import SpriteManager
from lib.helpers.Display import Display



from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Release any resources currently in use for the displays
displayio.release_displays()

time.sleep(1)

print("---Pico Pad Keyboard---")
print(os.uname().machine)

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

sprite_manager = SpriteManager("sonic")
display = Display(sprite_manager)
text_manager = TextManager(display)
text_manager.set_text("Meeting that contains a big big very big, Ive said a big title in the event calendar")
time.sleep(10)
original_group = display.get_group()
display.get().show(original_group)

while True:
    now = time.monotonic()

    # display some art!!!
    if now >= sprite_manager.get_last_blink_time() + sprite_manager.get_blink_off_duration():
        sprite_manager.change_frame_current_sprite()

        if sprite_manager.get_source_index() == sprite_manager.get_total_frames_of_current_sprite():
            sprite_manager.set_source_index(0)
            sprite_manager.set_total_cycle(sprite_manager.get_total_cycle()+1)
            if sprite_manager.get_total_cycle() == sprite_manager.get_total_cycle_per_sprite():
                sprite_manager.set_total_cycle(0)
                sprite_manager.set_source_index(0)
                display.get_group().pop()
                sprite_manager.set_current_sprite_of_cycle(
                    random.randint(0, len(sprite_manager.get_all_sprites())-1))
                display.get_group().append(sprite_manager.get_all_sprites()[
                    sprite_manager.get_current_sprite_of_cycle()][sprite_manager.get_sprite_index()])

        sprite_manager.set_last_blink_time(now)

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
