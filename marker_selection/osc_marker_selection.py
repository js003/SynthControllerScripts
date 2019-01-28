import sys
import cv2
from pythonosc import udp_client
from marker_selection import MarkerSelection


class OscMarkerSelection(MarkerSelection):

    def __init__(self, ip, port):
        self.client = udp_client.SimpleUDPClient(ip, int(port))
        self.marker_state = {}
    
    def blink_action(self, marker_id):
        if marker_id == -1: return
        toggle = self.marker_state.get(marker_id, False)
        print("Blink: Marker " + str(marker_id) + " " + str(not toggle))
        self.marker_state[marker_id] = not toggle
        self.client.send_message("/marker" + str(marker_id), 127 if toggle else 0)

    def overlay_marker(self, marker_id, marker_corners, frame):
        if self.marker_state.get(marker_id, False):
            cv2.polylines(frame, marker_corners, True, (0, 0, 255), 2)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: osc_marker_selection.py <osc_server_ip> <osc_server_port>')
    else:
        OscMarkerSelection(sys.argv[1], sys.argv[2]).run()
