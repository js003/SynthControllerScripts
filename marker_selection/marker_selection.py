import traceback
import time
import uvc
import numpy as np
import cv2
import tkinter as tk
from cv2 import aruco

class MarkerSelection:
    def __init__(self):
        pass

    def run(self):
        self.running = True
        while(self.running):
            try:
                # Setup camera captures
                dev_list = uvc.device_list()
                world_capture = uvc.Capture(dev_list[1]["uid"])
                eye_capture = uvc.Capture(dev_list[0]["uid"])

                # Setup resolutions
                width = 1280
                height = 720
                self.cam_center = (int(width/2), int(height/2))
                world_capture.frame_mode = (width, height, 60)
                eye_capture.frame_mode = (640, 480, 60)

                # Aruco
                self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
                self.aruco_params = aruco.DetectorParameters_create()

                # Initialize variables
                last_pupil_count = 1
                eye_closed_start = None
                selected_marker_id = -1
           
                while(self.running):
                    # Blink detection
                    eye_frame = eye_capture.get_frame(1)
                    eye_bgr = eye_frame.bgr
                    eye_gray = eye_frame.gray
                    pupil_count = self.process_eye_frame(eye_bgr, eye_gray)
                    cv2.imshow('eye_frame', eye_bgr)

                    if last_pupil_count == 1 and pupil_count == 0:
                        last_pupil_count = 0
                        eye_closed_start = time.time()
                    elif last_pupil_count == 0 and pupil_count == 1:
                        last_pupil_count = 1
                        t = time.time() - eye_closed_start
                        if t > 0.3:
                            self.blink_action(selected_marker_id)

                    # Marker detection
                    world_frame = world_capture.get_frame(1)
                    world_bgr = world_frame.bgr
                    world_gray = world_frame.gray
                    selected_marker = self.process_world_frame(world_bgr, world_gray)
                    cv2.imshow('world_frame', world_bgr)

                    if pupil_count == 1:
                        curr_id = selected_marker[0] if selected_marker is not None else -1
                        if curr_id != selected_marker_id:
                            selected_marker_id = curr_id
                            self.select_action(selected_marker_id)

                    # Exit if the user presses 'q'
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.running = False
            except KeyboardInterrupt:
                self.running = False
            except Exception:
                cv2.destroyAllWindows()
                self.retry_dialog(traceback.format_exc())
            try:
                world_capture.close()
                eye_capture.close()
            except:
                pass
            cv2.destroyAllWindows()

    def process_eye_frame(self, frame_bgr, frame_gray):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        retval, thresholded = cv2.threshold(frame_gray, 40, 255, 0)
        closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
        thresholded, contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame_bgr, contours, -1, (255, 0, 0), 2)
        pupil_count = 0
        # Calculate and draw contours
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:
                continue
            bounding_box = cv2.boundingRect(contour)
            extend = area / (bounding_box[2] * bounding_box[3])
            # Reject the contours with big extend
            if extend > 0.8:
                continue
            pupil_count += 1
            # Calculate countour center and draw a dot there
            m = cv2.moments(contour)
            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                cv2.circle(frame_bgr, center, 3, (0, 255, 0), -1)
            # Fit an ellipse around the contour and draw it into the image
            try:
                ellipse = cv2.fitEllipse(contour)
                cv2.ellipse(frame_bgr, box=ellipse, color=(0, 255, 0))
            except:
                pass
        return pupil_count

    def process_world_frame(self, frame_bgr, frame_gray):
        corners, ids, rejected_img_points = aruco.detectMarkers(frame_gray, self.aruco_dict, parameters=self.aruco_params)

        selected_marker = None # tuple (id, points, center, distance)
        for i, c in enumerate(corners):
            marker_id = ids[i][0]
            center = c[0].mean(0)
            marker_corners = np.array(c, np.int32)
            
            cv2.polylines(frame_bgr, marker_corners, True, (255, 0, 0), 2)
            self.overlay_marker(marker_id, marker_corners, frame_bgr)
            text_pos = (int(center[0] - len(str(marker_id)) * 10), int(center[1] + 10))
            cv2.putText(frame_bgr, str(marker_id), text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 10, cv2.LINE_AA)
            cv2.putText(frame_bgr, str(marker_id), text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            distance = np.linalg.norm(self.cam_center - center)
            if selected_marker is None or selected_marker[3] > distance:
                selected_marker = (marker_id, c, center, distance)

        if selected_marker is not None:
            if selected_marker[3] > 200:
                selected_marker = None
            else:
                cv2.circle(frame_bgr, tuple(selected_marker[2]), 30, (0, 255, 0), 4)

        cv2.circle(frame_bgr, self.cam_center, 5, (0, 0, 0), 2)
        cv2.circle(frame_bgr, self.cam_center, 8, (255, 255, 255), 2)
        cv2.circle(frame_bgr, self.cam_center, 10, (0, 0, 0), 2)
        return selected_marker

    def retry_dialog(self, text):
        self.running = False
        root = tk.Tk()
        root.title("Marker tracking crashed")
        label = tk.Label(root, text=text)
        label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        def confirm_restart():
            self.running = True
            root.destroy()
        button = tk.Button(root, text="Restart", command=confirm_restart)
        button.pack(side="bottom", fill="none", expand=True, padx=20, pady=20)
        root.mainloop()

    def overlay_marker(self, marker_id, marker_corners, frame):
        pass

    def select_action(self, marker_id):
        pass

    def blink_action(self, marker_id):
        pass

if __name__ == '__main__':
    MarkerSelection().run()
