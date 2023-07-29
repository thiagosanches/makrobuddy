import board
import busio
import gc9a01
import displayio


class Display:
    def __init__(self):
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
        self.GC9A01 = gc9a01.GC9A01(
            display_bus, width=self.width, height=self.height, backlight_pin=tft_bl)