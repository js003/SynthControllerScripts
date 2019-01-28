import socket
import mido
from marker_selection import MarkerSelection

COLORS = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099', '#0099c6', '#dd4477', '#66aa00', '#b82e2e', '#316395', '#994499', '#22aa99', '#aaaa11', '#6633cc', '#e67300', '#8b0707', '#651067', '#329262', '#5574a6', '#3b3eac']

class SynthMarkerSelection(MarkerSelection):

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def select_action(self, marker_id)
        self.socket.sendto(str(marker_id).encode(), ('127.0.0.1', 8898))
        self.socket.sendto(COLORS[marker_id], ('127.0.0.1', 8899))
    
    def blink_action(self, marker_id):
        self.socket.sendto('SELECT'.encode(), ('127.0.0.1', 8898))

if __name__ == '__main__':
    SynthMarkerSelection().run()
