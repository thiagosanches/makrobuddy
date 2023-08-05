import time
import os
import supervisor

from lib.makrobuddy.helpers.TextManager import TextManager
from lib.makrobuddy.helpers.SpriteManager import SpriteManager
from lib.makrobuddy.helpers.Display import Display
from lib.makrobuddy.helpers.EventManager import EventManager
from lib.makrobuddy.eletronic_components.RotaryEncoder import RotaryEncoder
from lib.makrobuddy.eletronic_components.MechanicalSwitches import MechanicalSwitches

print(os.uname().machine)
time.sleep(0.5)

# Disable auto_reload
supervisor.disable_autoreload()

rotary_encoder = RotaryEncoder()
mechanical_switches = MechanicalSwitches()
event_manager = EventManager()
display = Display()
text_manager = TextManager(display.width, display.height)
text_manager.set_text("MakroBuddy 1.0")

display.GC9A01.show(text_manager.group)
display.GC9A01.refresh()

character = "dog"
available_character = os.listdir("/sprites")
while rotary_encoder.button.value == True:
    character = available_character[rotary_encoder.encoder.position %
                                    len(available_character)]
    text_manager.set_text(character)
    display.GC9A01.refresh()
    time.sleep(0.01)

sprite_manager = SpriteManager(character, display.width, display.height)
display.GC9A01.show(sprite_manager.main_group)
display.GC9A01.refresh()

while True:
    now = time.monotonic()

    # display some art if there is no important message!
    if not event_manager.showing_message and now >= sprite_manager.last_blink_time + sprite_manager.blink_off_duration:
        sprite_manager.run(now)
        display.GC9A01.refresh()

    message = event_manager.run(now)
    if message != None:
        text_manager.set_text(message)
        display.GC9A01.show(text_manager.group)
        display.GC9A01.refresh()

    # important messages should stay like 30 seconds on the screen!
    if (event_manager.last_time_read + event_manager.ttl) <= now:
        event_manager.showing_message = False
        display.GC9A01.show(sprite_manager.main_group)
        display.GC9A01.refresh()

    rotary_encoder.run()
    mechanical_switches.run()

    # debounce
    time.sleep(0.01)
