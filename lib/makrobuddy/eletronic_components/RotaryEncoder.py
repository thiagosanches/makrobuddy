import time
import board
import os
import usb_hid
import rotaryio
import digitalio
import supervisor

from lib.makrobuddy.helpers.TextManager import TextManager
from lib.makrobuddy.helpers.SpriteManager import SpriteManager
from lib.makrobuddy.helpers.Display import Display
from lib.makrobuddy.helpers.EventManager import EventManager
from lib.makrobuddy.eletronic_components.RotaryEncoder import RotaryEncoder


from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

class RotaryEncoder:
    def __init__(self) -> None:
        self.encoder_button = digitalio.DigitalInOut(board.GP22)
        self.encoder_button.direction = digitalio.Direction.INPUT
        self.encoder_button.pull = digitalio.Pull.UP
        self.encoder_button_state = None

        self.encoder = rotaryio.IncrementalEncoder(board.GP20, board.GP21)
        self.last_position = self.encoder.position

        
        self.cc = ConsumerControl(usb_hid.devices)

    def on_tick(self):    
        current_position = self.encoder.position
        position_change = current_position - last_position
        if position_change > 0:
            for _ in range(position_change):
                self.cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            print(current_position)
        elif position_change < 0:
            for _ in range(-position_change):
                self.cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            print(current_position)
        last_position = current_position

        if not self.encoder_button.value and self.encoder_button_state is None:
            self.encoder_button_state = "pressed"
        if self.encoder_button.value and self.encoder_button_state == "pressed":
            self.cc.send(ConsumerControlCode.PLAY_PAUSE)
            self.encoder_button_state = None