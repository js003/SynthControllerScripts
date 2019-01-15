from plugin import Plugin
from pyglui import ui
import socket
import sys
import time
import subprocess
import os

def start_helm():
    my_env = os.environ
    my_env.pop('LD_LIBRARY_PATH', None)
    print(subprocess.Popen(['helm']))

class SynthController(Plugin):
    # Calling add_menu() will create an icon in the icon bar that represents
    # your plugin. You can customize this icon with a symbol of your choice.
    icon_chr = '@'  # custom menu icon symbol

    # The default icon font is Roboto: https://fonts.google.com/specimen/Roboto
    # Alternatively, you can use icons from the Pupil Icon font:
    # https://github.com/pupil-labs/pupil-icon-font
    icon_font = 'roboto'  # or `pupil_icons` when using the Pupil Icon font

    def __init__(self, g_pool):
        super().__init__(g_pool)
        # persistent attribute
        self.last_square = 0
        self.container = None
        self.socket = None
        self.time_eyes_closed = None

    def init_ui(self):
        # Create a floating menu
        self.add_menu()
        self.menu.label = 'SynthController'
        # Create a simple info text
        # help_str = "Example info text."
        # self.menu.append(ui.Info_Text(help_str))
        # Add a slider that represents the persistent value
        self.menu.append(ui.Slider('last_square', self, min=0, step=1, max=5, label='Pupil Labs Glasses'))
        
        self.menu.append(ui.Button('Start Helm', start_helm))

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect(('127.0.0.1', 8899))

    def deinit_ui(self):
        self.remove_menu()

    def get_init_dict(self):
        # all keys need to exists as keyword arguments in __init__ as well
        return {}

    def recent_events(self, events):
        if 'pupil' in events and events['pupil']:
            curr_time = time.time()
            if events['pupil'][0]['confidence'] < 0.5 and not self.time_eyes_closed:
                self.time_eyes_closed = curr_time
            elif events['pupil'][0]['confidence'] >= 0.5 and self.time_eyes_closed:
                if curr_time - self.time_eyes_closed > 0.25:
                    self.socket.send('SELECT'.encode())
                self.time_eyes_closed = None
        if 'surfaces' in events and events['surfaces']:
            surface = events['surfaces'][0]
            if 'gaze_on_srf' in surface and surface['gaze_on_srf'] and surface['gaze_on_srf'][0]['confidence'] > 0.95:
                pos = surface['gaze_on_srf'][0].get('norm_pos')
                if 0 <= pos[0] < 1 and 0 <= pos[1] < 1:
                    square = int(pos[0] * 3) + int(pos[1] * 2) * 3
                    if self.last_square != square and square >= 0 and square <= 127:
                        self.last_square = square
                        self.socket.send(str(self.last_square).encode())

                


