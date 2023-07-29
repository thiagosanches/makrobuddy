import time
import board
import displayio
import os
import usb_hid
import rotaryio
import digitalio
import random
import supervisor

from lib.helpers.TextManager import TextManager
from lib.helpers.SpriteManager import SpriteManager
from lib.helpers.Display import Display
from lib.helpers.EventManager import EventManager
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Release any resources currently in use for the displays
displayio.release_displays()
time.sleep(0.5)

# Disable auto_reload
supervisor.disable_autoreload()

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

display = Display()
display.GC9A01.auto_refresh = False
event_manager = EventManager()

text_manager = TextManager(display.width, display.height)
text_manager.set_text("MakroBuddy 1.0")
display.GC9A01.show(text_manager.group)
display.GC9A01.refresh()
time.sleep(2)

sprite_manager = SpriteManager("sonic", display.width, display.height)
display.GC9A01.show(sprite_manager.sprite_group)
display.GC9A01.refresh()
time.sleep(5)

while True:
    now = time.monotonic()

    # display some art if there is no important message!
    if not event_manager.showing_message and now >= sprite_manager.last_blink_time  + sprite_manager.blink_off_duration:
        sprite_manager.run(now)
        display.GC9A01.refresh()

    if now >= (event_manager.last_time_read + event_manager.period_check) and not event_manager.showing_message:
        event = event_manager.get()
        if event != None:
            if event["uuid"] != event_manager.uuid:
                event_manager.uuid = event["uuid"]
                event_manager.showing_message = True
                event_manager.last_time_read = now

                text_manager.set_text(event["message"])
                display.GC9A01.show(text_manager.group)
                display.GC9A01.refresh()

    # important messages should stay like 30 seconds on the screen!
    if (event_manager.last_time_read + event_manager.ttl) <= now:
        event_manager.showing_message = False
        display.GC9A01.show(sprite_manager.sprite_group)
        display.GC9A01.refresh()

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
