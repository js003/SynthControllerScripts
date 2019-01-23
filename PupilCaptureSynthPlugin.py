from plugin import Plugin
from pyglui import ui
import time
import socket
import sys
import time
import subprocess
import os

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
        # persistent attributes
        self.menu = None
        self.last_square = 0
        self.socket = None
        self.time_eyes_closed = None
        self.colors = [b'1511ff',b'00ff15',b'fff200',b'ff0000']
        self.helm_started = False

    def init_ui(self):
        # Create a floating menu
        self.add_menu()
        self.menu.label = 'SynthController'
        self.menu.append(ui.Slider('last_square', self, min=0, step=1, max=3, label='Pupil Labs Glasses'))
        self.menu.append(ui.Button('Start Helm', self.start_helm))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_helm(self):
        if self.helm_started:
             return
        self.helm_started = True
        my_env = os.environ
        my_env.pop('LD_LIBRARY_PATH', None)
        subprocess.Popen(['python3', '/home/snyth/Desktop/SynthControllerScripts/SynthControllerDataReceiver.py'], env=my_env)
        subprocess.Popen(['/home/synth/Desktop/helm/gui-synth/standalone/builds/linux/build/helm'], env=my_env)
        time.sleep(0.5)
        subprocess.Popen(['xdotool', 'key', 'super+f'], env=my_env)

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
                    self.socket.sendto('SELECT'.encode(), ('127.0.0.1', 8898))
                self.time_eyes_closed = None
        if 'surfaces' in events and events['surfaces']:
            surface = events['surfaces'][0]
            if 'gaze_on_srf' in surface and surface['gaze_on_srf'] and surface['gaze_on_srf'][0]['confidence'] > 0.95:
                pos = surface['gaze_on_srf'][0].get('norm_pos')
                if 0 <= pos[0] < 1 and 0 <= pos[1] < 1:
                    square = int(pos[0] * 4)
                    if self.last_square != square and square >= 0 and square <= 127:
                        self.last_square = square
                        self.socket.sendto(str(self.last_square).encode(), ('127.0.0.1', 8898))
                        self.socket.sendto(self.colors[self.last_square], ('127.0.0.1', 8899))

                


