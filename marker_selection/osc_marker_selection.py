from marker_selection import MarkerSelection
from pythonosc import udp_client

class OscMarkerSelection(MarkerSelection):

    def __init__():
        self.client = udp_client.SimpleUDPClient("192.168.178.72", 5006)
        self.marker_state = {}
    
    def blink_action(self, marker_id):
        toggle = self.marker_state.get(marker_id, False)
        print("Blink: Marker " + str(marker_id) + " " + str(not toggle))
        self.marker_state[marker_id] = not toggle
        self.client.send_message("/marker" + str(marker_id), 127 if toggle else 0)


if __name__ == '__main__':
    OscMarkerSelection().run()
