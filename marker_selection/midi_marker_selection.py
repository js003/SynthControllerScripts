import cv2
import mido
from marker_selection import MarkerSelection


class MidiMarkerSelection(MarkerSelection):

    def __init__(self):
        self.midi_port = mido.open_output()
        self.marker_state = {}
    
    def blink_action(self, marker_id):
        if marker_id == -1: return
        toggle = self.marker_state.get(marker_id, False)
        print("Blink: Marker " + str(marker_id) + " " + str(not toggle))
        self.marker_state[marker_id] = not toggle
        if marker_id == 0:
            self.midi_port.send(mido.Message('control_change', channel=0 if toggle else 1, control=marker_id, value=127) 
        else:
            self.midi_port.send(mido.Message('control_change', channel=0, control=marker_id, value=127 if toggle else 0))  

    def overlay_marker(self, marker_id, marker_corners, frame):
        if self.marker_state.get(marker_id, False):
            cv2.polylines(frame, marker_corners, True, (0, 0, 255), 2)


if __name__ == '__main__':
    MidiMarkerSelection().run()
