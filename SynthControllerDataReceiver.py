import socket
import sys
import mido

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
sock.bind(('0.0.0.0', 8899))
midi_port = mido.open_output()
knob = None
selected_knob = None

# Smoothing
smoothing_k = 42
smoothing_array = {}

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)
    print('received {} bytes from {}\n'.format(len(data), address))

    if address[0] == '127.0.0.1':
        if data.decode() == 'SELECT\n':
            selected_knob = knob
            if selected_knob not in smoothing_array:
                smoothing_array[selected_knob] = [0] * smoothing_k
        else:
            knob = int(data)
    elif selected_knob is not None:
        smoothing_array[selected_knob] = smoothing_array[selected_knob][1:]
        smoothing_array[selected_knob].append(int(float(data) * 127))
        val = int(sum(smoothing_array[selected_knob])/len(smoothing_array[selected_knob]))
        print("Value: " + str(val))
        print(smoothing_array[selected_knob])
        midi_port.send(mido.Message('control_change', channel=0, control=selected_knob, value=val))  

    print(data)
    print("Looking at knob: " + str(knob))
    print("Selected knob: " + str(selected_knob))

