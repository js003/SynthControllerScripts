import uvc
import cv2
import numpy as np
import math
import time
from PIL import Image
from pyzbar.pyzbar import decode
import socket

def main():
    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    
    # print device list
    dev_list = uvc.device_list()
    print(dev_list)

    worldCapture = uvc.Capture(dev_list[1]["uid"])
    eyeCapture = uvc.Capture(dev_list[0]["uid"])

    # Resolution
    width = 1280
    height = 720
    midX = int(width / 2)
    midY = int(height / 2)
    worldCapture.frame_mode = (width, height, 60)
    eyeCapture.frame_mode = (640, 480, 60)

    # Blink detection variables
    eyeState = 1
    eyeTime = None
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        frame = worldCapture.get_frame_robust()

        # Eye tracking stuff per eyeFrame
        eyeFrame = eyeCapture.get_frame_robust()
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        retval, thresholded = cv2.threshold(eyeFrame.gray, 40, 255, 0)
        cv2.imshow("threshold", thresholded)
        closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
        cv2.imshow("closed", closed)
        thresholded, contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        drawing = np.copy(eyeFrame.bgr)
        cv2.drawContours(drawing, contours, -1, (255, 0, 0), 2)
        i = 0
        # Calc and draw contours
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:
                continue
            bounding_box = cv2.boundingRect(contour)
            extend = area / (bounding_box[2] * bounding_box[3])
            # reject the contours with big extend
            if extend > 0.8:
                continue
            i += 1
            # calculate countour center and draw a dot there
            m = cv2.moments(contour)
            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                cv2.circle(drawing, center, 3, (0, 255, 0), -1)
            # fit an ellipse around the contour and draw it into the image
            try:
                ellipse = cv2.fitEllipse(contour)
                cv2.ellipse(drawing, box=ellipse, color=(0, 255, 0))
            except:
                pass
        if eyeState == 1 and i == 0:
            eyeState = 0
            eyeTime = time.time()
        elif eyeState == 0 and i == 1:
            eyeState = 1
            t = time.time() - eyeTime
            if t > 0.3:
                print("BLINK DETECTION!")
                sock.sendto('SELECT'.encode(), ('127.0.0.1', 8898))


        # show the frame
        cv2.imshow("Drawing", drawing)

        image_gray = np.array(frame.gray)
        image = np.array(frame.bgr)
        qr_codes = decode(image)
        
        # Draw the center
        cv2.rectangle(image,(midX - 1, midY - 1),(midX + 1, midY +1),(255, 255, 255),3)

        # Pupil tracking

        # QR Code processing
        if len(qr_codes) > 0:
            qrs = []
            for qr in qr_codes:
                tmp = qr.rect
                cv2.rectangle(image, (tmp.left, tmp.top), (tmp.left + tmp.width, tmp.top + tmp.height), (255, 0, 0), 3)
                
                # Draw the middle of the qr code
                qrX = tmp.left + int(tmp.width / 2)
                qrY = tmp.top + int(tmp.height / 2)
                cv2.rectangle(image, (qrX - 1, qrY - 1), (qrX + 1, qrY + 1), (255, 255, 255), 3)
                distance = round(math.hypot(qrX - midX, qrY - midY))
                print(qr)
                qrs.append((distance, qr))
            selected = sorted(qrs, key=lambda x: x[0])[0][1]
            print(selected.data)
            # Send color data of the selected qr code to helm.
            qr_values = str(selected.data).split(',')
            sock.sendto(qr_values[1].encode(), ('127.0.0.1', 8899))
            sock.sendto(qr_values[0].encode(), ('127.0.0.1', 8898))

            print(selected)
            cv2.rectangle(image, (selected.rect.left, selected.rect.top),
                          (selected.rect.left + selected.rect.width, selected.rect.top + selected.rect.height),
                          (0,255,0), 3)
        # Displays the current frame
        cv2.imshow('Current', image)

if __name__ == "__main__":
    main()
