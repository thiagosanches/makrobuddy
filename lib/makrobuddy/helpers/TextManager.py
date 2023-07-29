import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label as label


class TextManager:
    def __init__(self, display_width, display_height):
        self.group = displayio.Group()
        self.font = bitmap_font.load_font("/fonts/LeagueSpartan-Bold-16.bdf")
        self.label = label.Label(
            font=self.font,
            line_spacing=0.7,
            color=0x00ff00,
            scale=1,
            label_direction="UPD",
            save_text=False
        )
        self.label.anchor_point = (0.5, 0.5)
        self.label.anchored_position = (
            display_width // 2, display_height // 2)
        self.group.append(self.label)

    def wrap_nicely(self, string, max_chars):
        """A helper that will return the string with word-break wrapping.
        :param str string: The text to be wrapped.
        :param int max_chars: The maximum number of characters on a line before wrapping.
        """
        string = string.replace('\n', '').replace(
            '\r', '')  # strip confusing newlines
        words = string.split(' ')
        the_lines = []
        the_line = ""
        for w in words:
            if len(the_line+' '+w) <= max_chars:
                the_line += ' '+w
            else:
                the_lines.append(the_line)
                the_line = w
        if the_line:
            the_lines.append(the_line)
        the_lines[0] = the_lines[0][1:]
        the_newline = ""
        for w in the_lines:
            the_newline += '\n'+w
        return the_newline

    def set_text(self, string):
        self.label.text = self.wrap_nicely(string, 20)
