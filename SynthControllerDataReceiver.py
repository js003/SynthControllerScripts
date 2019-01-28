import socket
import sys
import mido

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
sock.bind(('0.0.0.0', 8898))
midi_port = mido.open_output()
selected_knob = -1

# Smoothing
smoothing_k = 42
smoothing_array = {}

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)
    print('received {} bytes from {}\n'.format(len(data), address))

    if address[0] == '127.0.0.1':
        selected_knob = int(data.decode())
        if selected_knob >= 0 and selected_knob not in smoothing_array:
            smoothing_array[selected_knob] = [0] * smoothing_k

    elif selected_knob >= 0:
        smoothing_array[selected_knob] = smoothing_array[selected_knob][1:]
        smoothing_array[selected_knob].append(int(float(data) * 127))
        val = int(sum(smoothing_array[selected_knob])/len(smoothing_array[selected_knob]))
        print("Value: " + str(val))
        print(smoothing_array[selected_knob])
        midi_port.send(mido.Message('control_change', channel=0, control=selected_knob, value=val))  

    print(data)
    print("Looking at knob: " + str(knob))
    print("Selected knob: " + str(selected_knob))

