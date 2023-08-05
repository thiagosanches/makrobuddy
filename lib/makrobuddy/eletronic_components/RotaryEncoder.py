import board
import usb_hid
import rotaryio
import digitalio

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

class RotaryEncoder:
    def __init__(self) -> None:
        self.encoder = rotaryio.IncrementalEncoder(board.GP20, board.GP21)
        self.encoder_last_position = self.encoder.position       
        self.cc = ConsumerControl(usb_hid.devices)
        
        self.button = digitalio.DigitalInOut(board.GP22)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        self.button_state = None       

    def run(self):    
        current_position = self.encoder.position
        position_change = current_position - self.encoder_last_position
        if position_change > 0:
            for _ in range(position_change):
                self.cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            print(current_position)
        elif position_change < 0:
            for _ in range(-position_change):
                self.cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            print(current_position)
        self.encoder_last_position = current_position

        if not self.button.value and self.button_state is None:
            self.encoder_button_state = "pressed"
        if self.button.value and self.button_state == "pressed":
            self.cc.send(ConsumerControlCode.PLAY_PAUSE)
            self.button_state = None