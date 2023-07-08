# yet-another-rp2040-macropad

This Git repository provides step-by-step instructions and code samples for building a simple macropad using the Raspberry Pi Pico microcontroller board. A macropad is a programmable keypad with customizable buttons that can be used to automate tasks, streamline workflows, or enhance productivity.

The Raspberry Pi Pico is a powerful yet affordable microcontroller board that offers a wide range of possibilities for DIY projects. By following the instructions in this repository, you'll be able to create your own macropad using the Pico and a few additional components.

| Photo A                            |  Photo B                            |
| ----------------------------------- | ----------------------------------- |
| ![image](https://github.com/thiagosanches/yet-another-rp2040-macropad/assets/5191469/f7b57aa0-b103-4cf7-b7d5-47833562f37e) | ![image](https://github.com/thiagosanches/yet-another-rp2040-macropad/assets/5191469/4682dc8b-548b-4197-a9b8-ca7d19ab609b) |

For this project I'm using a board from [Waveshare](https://www.waveshare.com/rp2040-lcd-1.28.htm) (RP2040 MCU Board, With 1.28inch Round LCD) that was laying around here. It uses a raspberry pi pico (rp2040) as its microcontroler, so it's possible to build a HID (Human Interface Device). In this repository, you'll discover a convenient housing specifically designed for this project. It includes designated spots for the Waveshare board, rotary encoder, and mechanical switches, ensuring a clean and organized assembly.

**Important:** Please take note that the LCD in my previous assembly was accidentally damaged during this project. Therefore, it is crucial to exercise caution when mounting the LCD into the housing or avoid any potential mishaps, such as dropping it on the floor.

## Bill of materials
- [Raspberry Pi-RP2040 Development Board](https://pt.aliexpress.com/item/1005004616586355.html?spm=a2g0o.order_list.order_list_main.21.21efcaa4GvI4NZ&gatewayAdapt=glo2bra).
- [Rotary Encoder](https://pt.aliexpress.com/item/4001112405456.html?spm=a2g0o.order_list.order_list_main.337.56c2caa4j3XZvl&gatewayAdapt=glo2bra).
- Any mechanical [switch](https://pt.aliexpress.com/item/1005004285463567.html?spm=a2g0o.productlist.main.15.7c3823b2lCL06c&algo_pvid=f50a2a66-7073-4be2-a435-df6fec2686b5&algo_exp_id=f50a2a66-7073-4be2-a435-df6fec2686b5-7&pdp_npi=3%40dis%21BRL%2165.37%2132.69%21%21%2112.66%21%21%40212244c416888441242025140d0779%2112000028629113466%21sea%21BR%21172919556&curPageLogUid=xjMCfauOfAiu) compatible with MX Cherry should work.
- Some wires.
- Hot glue (to keep the wires on the waveshare board, since I don't have some male 1.27 pins).
- Soldering iron.
- 3d printed housing  (you can use the one that I've built [here](https://www.tinkercad.com/things/47IuxGAQAh5)).

## Hardware assembly guide

### Rotary Encoder
To ensure proper connectivity and functionality, it is recommended to refer to the following schematics. While you have the flexibility to choose which GPIO ports to utilize, please note that updating the code accordingly is essential for seamless operation.
![image](https://github.com/thiagosanches/yet-another-rp2040-macropad/assets/5191469/e939b195-b1f8-49cc-a5c2-993f597680d0)

### Mechanical Switches
![image](https://github.com/thiagosanches/yet-another-rp2040-macropad/assets/5191469/6970535f-c027-4c64-8933-e0e63ebadb38)


### Real footage

![image](https://github.com/thiagosanches/yet-another-rp2040-macropad/assets/5191469/04d06d68-d482-4c2d-9083-9100d1852387)

- The black wire is connected to the GND pin on the left header of the Waveshare board. This single black wire serves as the common ground connection for all the other switches.
- The colored wires originating from the left header of the Waveshare board are individually connected to the GPX ports and then connected to the corresponding switch pins.
- The wires from the rotary encoder are connected to the right header of the waveshare board.
- As you can noticed there are some hot glues to keep the wires steady on both left and right headers. I had to cut the wire a little bit, solder it a little and force to enter on each pin that I wanted. Remember, those pins are only 1.27mm.

Waveshare board offers a lot of pins as we can see here:
![image](https://github.com/thiagosanches/yet-another-rp2040-macropad/assets/5191469/34edd9b2-64b1-420e-881d-fecc4bb6de79)

## Firmware setup guide
- I've used CircuitPython from Adafruit as the firmware, you **must** follow [this](https://learn.adafruit.com/welcome-to-circuitpython?view=all#download-the-latest-version-2977908) guide before push our code into it. Basically, we have to 'prepare' our board with a proper firmware before push the code into it and make it executable.

## Install our code
- Clone this git repository.
- Connect your board on a USB port.
- Copy the `lib/`, `code.py` and `boot_out.txt` file into the `CIRCUITPY` volume (mount point).

That's it! Feel free to modify the python code, by default, I'm using the home key and the arrow keys and the rotary encoder as a volume controller (media controls).

You also may notice, that the code makes some references to graphics modules/libraries, however I'm still not using since I broke my LCD 😢.

## References
- https://learn.adafruit.com/diy-pico-mechanical-keyboard-with-fritzing-circuitpython/code-the-pico-keyboard
- https://learn.adafruit.com/rotary-encoder/hardware
- https://www.waveshare.com/rp2040-lcd-1.28.htm

Feel free to modify and personalize according to your specific project and goals. Good luck with your macropad build!
