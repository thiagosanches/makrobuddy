import time
import board
import os
import usb_hid
import rotaryio
import digitalio
import supervisor

from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

KEY = 2

class MechanicalSwitches:
    def __init__(self):

        self.kbd = Keyboard(usb_hid.devices)
        # list of pins to use (skipping GP15 on Pico because it's funky)
        self.pins = (
            board.GP0,
            board.GP1,
            board.GP3,
            board.GP4,
            board.GP5,
        )

        self.keymap = {
            (0): (KEY, [Keycode.HOME]),
            (1): (KEY, [Keycode.UP_ARROW]),
            (2): (KEY, [Keycode.LEFT_ARROW]),
            (3): (KEY, [Keycode.DOWN_ARROW]),
            (4): (KEY, [Keycode.RIGHT_ARROW]),
        }

        self.switches = []
        self.switch_state = [0, 0, 0, 0, 0]
        for i in range(len(self.pins)):
            switch = DigitalInOut(self.pins[i])
            switch.direction = Direction.INPUT
            switch.pull = Pull.UP
            self.switches.append(switch)

    def run(self):
        for button in range(len(self.pins)):
            if self.switch_state[button] == 0:
                if not self.switches[button].value:
                    try:
                        if self.keymap[button][0] == KEY:
                            self.kbd.press(*self.keymap[button][1])
                    except ValueError:  # deals w six key limit
                        pass
                    self.switch_state[button] = 1

            if self.switch_state[button] == 1:
                if self.switches[button].value:
                    try:
                        if self.keymap[button][0] == KEY:
                            self.kbd.release(*self.keymap[button][1])

                    except ValueError:
                        pass
                    self.switch_state[button] = 0
