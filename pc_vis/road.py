import cv2
import numpy as np

name_of_file = str(input("Write name of file: "))
image = cv2.imread(name_of_file)
img_size = [360, 200]
src = np.float32([[20, 200], [350, 200], [275, 120], [85, 120]])
src_draw = np.array(src, dtype = np.int32)
dst = np.float32([[0, img_size[1]], [img_size[0], img_size[1]], [img_size[1], 0], [0, 0]])

while(cv2.waitKey(1) != 27):
    cv2.imshow("orig", image)
    resized = cv2.resize(image, (img_size[0], img_size[1]))
    cv2.imshow("resized", resized)

    #необходимо подобрать на конечном видео
    r_channel = resized[:,:,2]
    binary_r = np.zeros_like(r_channel)
    binary_r[(r_channel>200)] = 1
    # cv2.imshow("r_channel", binary)
    hls = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
    l_channel = resized[:,:,2]
    binary_l = np.zeros_like(l_channel)
    binary_l[(r_channel>160)] = 1
    #
    lr_binary = np.zeros_like(binary_l)
    lr_binary[((binary_l == 1)|(binary_r == 1))] = 255
    cv2.imshow("binary", lr_binary)

    lr_binary_visual = lr_binary.copy()
    cv2.polylines(lr_binary_visual, [src_draw], True, 255)
    cv2.imshow("polygon", lr_binary_visual)

    tmp = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.WarpPerspective(lr_binary, tmp, (img_size[0], img_size[1]), flags=cv2.INTER_LINEAR)
    cv2.imshow("warped", warped)

    histogram = np.sum(warped[warped.shape[0]//2:,:], axis=0)
    midpoint = histogram.shape[0]//2
    IndWhitestColumnL = np.argmax(histogram[:midpoint])
    IndWhitestColumnR = np.argmax(histogram[midpoint:])
    warped_visual = warped.copy()
    cv2.line(warped_visual, (IndWhitestColumnL, 0), (IndWhitestColumnL, warped_visual.shape[0], 110, 2))
    cv2.line(warped_visual, (IndWhitestColumnR, 0), (IndWhitestColumnR, warped_visual.shape[0], 110, 2))
    cv2.imshow("white_columns", warped_visual)