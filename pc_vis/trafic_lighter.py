import cv2
import numpy as np
import time

def find_circle():
    cap = cv2.VideoCapture(0)
    frame_rate = 30
    prev = 0
    while True:
        time_elapsed = time.time() - prev
        ret, frame = cap.read()
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, minRadius=30)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(frame, (x-5, y-5), (x+5, y+5), (0, 128, 255), -1)
                    cv2.waitKey(0)
        cv2.imshow("output", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break 

find_circle()
