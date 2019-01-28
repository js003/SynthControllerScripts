import socket
import mido
from marker_selection import MarkerSelection

COLORS = [b'3366cc', b'dc3912', b'ff9900', b'109618', b'990099', b'0099c6', b'dd4477', b'66aa00', b'b82e2e', b'316395', b'994499', b'22aa99', b'aaaa11', b'6633cc', b'e67300', b'8b0707', b'651067', b'329262', b'5574a6', b'3b3eac']

class SynthMarkerSelection(MarkerSelection):

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def select_action(self, marker_id)
        print('Looking at marker ' + str(marker_id))
        color = COLORS[marker_id] if marker_id >= 0 else b'000000'
        self.socket.sendto(color, ('127.0.0.1', 8899))

    def blink_action(self, marker_id):
        print('Blink at marker ' + str(marker_id))
        self.socket.sendto(str(marker_id).encode(), ('127.0.0.1', 8898))

if __name__ == '__main__':
    SynthMarkerSelection().run()
