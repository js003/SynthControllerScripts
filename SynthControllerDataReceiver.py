import socket
import sys
import mido

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
sock.bind(('0.0.0.0', 8899))
midi_port = mido.open_output()
knob = 1

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)
    print('received {} bytes from {}\n'.format(len(data), address))

    if address[0] == '127.0.0.1':
        knob = int(data)
    else:
        midi_port.send(mido.Message('control_change', channel=0, control=knob, value=int(float(data)*127)))  

    print(data)
    print(knob)
