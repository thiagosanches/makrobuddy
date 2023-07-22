import board
import busio
import gc9a01
import displayio


class Display:
    def __init__(self, sprite_manager):

        self.width = 240
        self.height = 240

        # Display something on the LCD.
        # Pin outs were defined from here: https://www.waveshare.com/rp2040-lcd-1.28.htm
        tft_dc = board.GP8
        tft_cs = board.GP9
        tft_clk = board.GP10
        tft_mosi = board.GP11
        tft_rst = board.GP12
        tft_bl = board.GP25

        spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

        # Make the displayio SPI bus and the GC9A01 display.
        display_bus = displayio.FourWire(
            spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
        self.display = gc9a01.GC9A01(
            display_bus, width=self.width, height=self.height, backlight_pin=tft_bl)

        # Create a Group to hold the sprite.
        self.group = displayio.Group(scale=2)

        # Add the sprite to the Group.
        self.group.append(sprite_manager.get_current_sprite())

        # Add the Group to the Display.
        self.display.show(self.group)

        # Set sprite location
        self.center_x = (self.width/2-1)
        self.center_y = (self.height/2-1)
        self.group.x = int((self.center_x - sprite_manager.get_sprite_width() /
                           2) - (sprite_manager.get_sprite_width() / 2))
        self.group.y = int((self.center_x - sprite_manager.get_sprite_height() /
                           2) - (sprite_manager.get_sprite_height() / 2))

    def get(self):
        return self.display

    def get_group(self):
        return self.group
