import pytesseract as pytes
from PIL import Image 
import cv2

def print_digits_from_img():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.inRange(hsv, (0, 0, 159), (75, 33, 255))
        contours = cv2.findContours(hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = contours[0]
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            (x, y, w, h) = cv2.boundingRect(contours[0])
        roimg = hsv[y : y+h, x : x+w]
        cv2.imshow("hsv", hsv)
        cv2.imshow("frame", roimg)
        print(pytes.image_to_string(Image.fromarray(hsv), lang="eng"))
        if cv2.waitKey(1) == 27:
            break

print_digits_from_img()