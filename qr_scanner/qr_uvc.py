import uvc
import cv2
import numpy as np
import math
from PIL import Image
from pyzbar.pyzbar import decode

def main():
    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    
    # print device list
    dev_list = uvc.device_list()
    print(dev_list)

    cap0 = uvc.Capture(dev_list[1]["uid"])
    # cap1 = uvc.Capture(dev_list[1]["uid"])

    # Resolution
    width = 1280
    height = 720
    midX = int(width / 2)
    midY = int(height / 2)

    cap0.frame_mode = (width, height, 60)
    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        frame = cap0.get_frame_robust()

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        # image = Image.fromarray(frame.gray)
        image_gray = np.array(frame.gray)
        image = np.array(frame.bgr)
        qr_codes = decode(image)
        
        # Draw the center
        cv2.rectangle(image,(midX - 1, midY - 1),(midX + 1, midY +1),(255, 255, 255),3)

        if len(qr_codes) > 0:
            qrs = []
            for qr in qr_codes:
                tmp = qr.rect
                cv2.rectangle(image, (tmp.left,tmp.top), (tmp.left + tmp.width, tmp.top + tmp.height), (255, 0, 0), 3)
                
                # Draw the middle of the qr code
                qrX = tmp.left + int(tmp.width / 2)
                qrY = tmp.top + int(tmp.height / 2)
                cv2.rectangle(image, (qrX - 1, qrY - 1), (qrX + 1, qrY + 1), (255, 255, 255), 3)
                distance = round(math.hypot(qrX - midX, qrY - midY))
                print(qr)
                wasd = { 'left': tmp.left, 'top': tmp.top, 'width': tmp.width, 'height': tmp.height, 'distance': distance }
                qrs.append(wasd)
            selected = sorted(qrs, key=lambda x: x['distance'])[0]
            print(selected)
            cv2.rectangle(image,(selected['left'], selected['top']),(selected['left'] + selected['width'], selected['top'] + selected['height']),(0,255,0),3)
        # Displays the current frame
        cv2.imshow('Current', image)



if __name__ == "__main__":
    main()
