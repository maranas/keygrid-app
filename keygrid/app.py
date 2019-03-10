
import toga
from toga.style import Pack
from toga.style.pack import (
    BOLD,
    BOTTOM,
    CENTER,
    COLUMN,
    MONOSPACE,
    ROW
)
from travertino.colors import (
    # colors
    BLACK,
    DARKBLUE,
    DARKSALMON,
    GREEN,
    INDIGO,
    ORANGE,
    RED,
    CRIMSON
)
import hashlib


class Keygrid(toga.App):
    row_length = 16
    row_count = 16
    labels = []
    key_input = None
    key_input_confirm = None
    char_lookup = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?!,.:;*=#(){}[]<>%'
    row_colors = [BLACK,
                  DARKBLUE,
                  DARKSALMON,
                  GREEN,
                  INDIGO,
                  ORANGE,
                  RED,
                  CRIMSON,
                  BLACK,
                  DARKBLUE,
                  DARKSALMON,
                  GREEN,
                  INDIGO,
                  ORANGE,
                  RED,
                  CRIMSON ]

    def get_hashed_user_key(self, key_string, key_string_confirm):
        if (len(key_string) < 1 or key_string != key_string_confirm):
            return None
        hash_string =  hashlib.sha512(key_string.encode()).hexdigest()
        quarter = int(len(hash_string)/4)
        left_hash = (hashlib.sha512(hash_string[:quarter].encode()).digest() +
                     hashlib.sha512(hash_string[quarter:quarter*2].encode()).digest())
        right_hash = (hashlib.sha512(hash_string[quarter*2:quarter*3].encode()).digest() +
                      hashlib.sha512(hash_string[quarter*3:].encode()).digest())
        return left_hash + right_hash
    
    def on_change(self, widget):
        # key_input change handler
        list_length = len(self.char_lookup)
        hash_bytes = self.get_hashed_user_key(self.key_input.value, self.key_input_confirm.value)
        row_string = ''
        row_num = 0
        if hash_bytes != None:
            for i in range(len(hash_bytes)):
                index_to_use = int(hash_bytes[i]) % list_length
                row_string = row_string + self.char_lookup[index_to_use]
                if ((i + 1) % self.row_length) == 0:
                    if row_num < self.row_count:
                        self.labels[row_num].text = row_string
                    row_string = ''
                    row_num = row_num + 1
                else:
                    row_string = row_string + ' '
        else:
            for i in range(self.row_count):
                self.labels[i].text = "  K e y   m i s m a t c h ! !  "

    def startup(self):
        # Create a main window with a name matching the app
        self.main_window = toga.MainWindow(title=self.name)

        # Create a main content box
        main_box = toga.Box(style = Pack(direction = COLUMN,
                                         padding   = 12,
                                         flex      = 1 ))

        # add the key area
        main_box.add(toga.Label('Keygrid',
                                style=Pack(padding_bottom = 8,
                                           text_align = CENTER,
                                           font_size  = 16)))
        self.key_input = toga.PasswordInput(placeholder = 'Enter your key here',
                                            style       = Pack(padding_bottom = 16))
        self.key_input.on_change = self.on_change
        main_box.add( self.key_input )
        
        # add the rows
        for i in range(self.row_count):
            label = toga.Label('1 2 3 4 5 6 7 8 9 0 A B C D E F',
                               style=Pack(text_align  = CENTER,
                                          font_family = MONOSPACE,
                                          color       = self.row_colors[i]))
            self.labels.append(label)
            main_box.add(label)
        
        # copyright
        main_box.add( toga.Label('© Copyright 2019. ganglionsoftware.com',
                                style=Pack(padding = 24,
                                           text_align = CENTER )))

        # Add the content on the main window
        self.main_window.content = main_box

        # Show the main window
        self.main_window.show()


def main():
    return Keygrid('Keygrid', 'com.ganglionsoftware.keygrid')

