from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import numpy as np
import math

def main():
    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    capture = cv2.VideoCapture(0)
    # eyeCapture = cv2.VideoCapture(1)

    # Resolution
    width = 1280
    height = 720
    midX = int(width / 2)
    midY = int(height / 2)

    # capture.set(2, ())
    capture.set(3, width)
    capture.set(4, height)
    # eyeCapture.set(3, 120)
    # eyeCapture.set(4, 40)

    
    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()
        # ret, frame2 = eyeCapture.read()

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        
        # print(decode(image))
        
        # TESTING STUFF
        qr_codes = decode(image)
        
        # Draw the center
        cv2.rectangle(frame,(midX - 1, midY - 1),(midX + 1, midY +1),(0,255,0),3)

        if len(qr_codes) > 0:
            qrs = []
            for qr in qr_codes:
                tmp = qr.rect
                cv2.rectangle(frame,(tmp.left,tmp.top),(tmp.left + tmp.width ,tmp.top + tmp.height),(0,255,0),3)
                
                # Draw the middle of the qr code
                qrX = tmp.left + int(tmp.width / 2)
                qrY = tmp.top + int(tmp.height / 2)
                cv2.rectangle(frame, (qrX - 1, qrY - 1), (qrX + 1, qrY + 1), (0, 255, 0), 3)
                distance = round(math.hypot(qrX - midX, qrY - midY))
                print(qr)
                wasd = { 'left': tmp.left, 'top': tmp.top, 'width': tmp.width, 'height': tmp.height, 'distance': distance }
                qrs.append(wasd)
            selected = sorted(qrs, key=lambda x: x['distance'])[0]
            print(selected)
            cv2.rectangle(frame,(selected['left'], selected['top']),(selected['left'] + selected['width'], selected['top'] + selected['height']),(0,0,255),3)
        # Displays the current frame
        cv2.imshow('Current', frame)



if __name__ == "__main__":
    main()
