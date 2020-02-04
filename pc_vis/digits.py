import cv2 
import time
import numpy as np
from PIL import Image
import pytesseract as pytes

cap_1 = cv2.VideoCapture(0)

def write_numbers():
    frame_rate = 5
    prev = 0
    hsv_min = np.array((0, 0, 110), np.uint8)
    hsv_max = np.array((169, 255, 255), np.uint8)
    cap = cap_1
    cap.set(cv2.CAP_PROP_FPS, 5)
    # PAL
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    while True:
        time_elapsed = time.time() - prev
        ret, frame = cap.read()
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            img_erode = cv2.inRange(frame, hsv_min, hsv_max)
            img_erode = cv2.erode(img_erode, np.ones((3, 3), np.uint8), iterations=1)
            contours, hierarchy = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            if contours:
                for idx, contour in enumerate(contours):
                    (x, y, w, h) = cv2.boundingRect(contour)
                    if hierarchy[0][idx][3] == 0:
                        cv2.rectangle(img_erode, (x, y), (x+w, y+h), (70, 0, 0), 1)
                        message = pytes.image_to_string(Image.fromarray(img_erode[y : y+h, x : x+w]), lang="eng", config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
                        if message:
                            print("[System] app found ", message)    
                        # print("[System] app found ", pytes.image_to_string(Image.fromarray(img_erode[y : y+h, x : x+w]), lang="eng", config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
                # print(pytes.image_to_string(Image.fromarray(img_erode), lang="eng", config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
            cv2.imshow("Output", img_erode) 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 

write_numbers()