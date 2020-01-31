from PIL import Image
import pytesseract as pytes
import cv2
import numpy as np

def main():
    image = input("Write name of img file: ")
    img = cv2.imread(image)
    print("[System] Image had read")

    img = cv2.bitwise_not(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = np.array((0, 0, 110), np.uint8)
    hsv_max = np.array((169, 255, 255), np.uint8)
    img_erode = cv2.inRange(img, hsv_min, hsv_max)
    img_erode = cv2.erode(img_erode, np.ones((3, 3), np.uint8), iterations=1)

    contours, hierarchy = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    output = img.copy()

    for idx, contour in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        if hierarchy[0][idx][3] == 0:
            cv2.rectangle(output, (x, y), (x+w, y+h), (70, 0, 0), 1)
            print("[System] app found ", pytes.image_to_string(Image.fromarray(img[y : y+h, x : x+w]), lang="eng", config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytes.image_to_string(Image.fromarray(img_erode), lang="eng", config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    cv2.imshow("Input", img)
    cv2.imshow("Enlarged", img_erode)
    cv2.imshow("Output", output)
    cv2.waitKey(0)

main()