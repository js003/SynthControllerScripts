import mido
import subprocess
import time

keyOne = False
keyTwo = False

with mido.open_input('Q49 MIDI 1') as port:
  for msg in port:
    if msg.channel != 0:
      break
    if msg.type == 'note_on':
      if msg.note == 36:
        keyOne = True
      elif msg.note == 84:
        keyTwo = True
    elif msg.type == 'note_off':
      if msg.note == 36:
        keyOne = False
      elif msg.note == 84:
        keyTwo = False

    if keyOne and keyTwo:
      subprocess.Popen(['xdotool', 'key', 'super+f'])
      time.sleep(0.05)
      subprocess.Popen(['xdotool', 'key', 'super+Right'])
      time.sleep(0.05)
      subprocess.Popen(['xdotool', 'key', 'super+f'])
      time.sleep(0.05)



