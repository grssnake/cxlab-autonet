import cv2
from cv2 import warpPerspective
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

    #необходимо подобрать на конечном видео
    #конвертирование картинки в черно-белое
    r_channel = resized[:,:,2]
    binary_r = np.zeros_like(r_channel)
    binary_r[(r_channel>200)] = 1
    hls = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
    l_channel = resized[:,:,2]
    binary_l = np.zeros_like(l_channel)
    binary_l[(r_channel>160)] = 1

    # объединение двух масок
    lr_binary = np.zeros_like(binary_l)
    lr_binary[((binary_l == 1)|(binary_r == 1))] = 255
    cv2.imshow("binary", lr_binary)

    #отрисовка трапеции, для дальнейшей обработки
    lr_binary_visual = lr_binary.copy()
    cv2.polylines(lr_binary_visual, [src_draw], True, 255)
    cv2.imshow("polygon", lr_binary_visual)

    # создане вида сверху
    tmp = cv2.getPerspectiveTransform(src, dst)
    warped = warpPerspective(lr_binary, tmp, (img_size[0], img_size[1]), flags=cv2.INTER_LINEAR)
    cv2.imshow("warped", warped)

    # выделение линии разметки
    histogram = np.sum(warped[warped.shape[0]//2:,:], axis=0)
    midpoint = histogram.shape[0]//2
    IndWhitestColumnL = np.argmax(histogram[:midpoint])
    IndWhitestColumnR = np.argmax(histogram[midpoint:])+midpoint
    warped_visual = warped.copy()
    cv2.line(warped_visual, (IndWhitestColumnL, 0), (IndWhitestColumnL, warped_visual.shape[0]), (0, 255, 0), 2)
    cv2.line(warped_visual, (IndWhitestColumnR, 0), (IndWhitestColumnR, warped_visual.shape[0]), (0, 255, 0), 2)
    cv2.imshow("white_columns", warped_visual)

    # создание выделения блоками дороги 
    nwindows = 9
    windows_height = np.int(warped.shape[0]/nwindows)
    window_half_width = 25

    XCenterLeftWindow = IndWhitestColumnL
    XcenterRightWindow = IndWhitestColumnR

    left_lane_inds = np.array([], dtype=np.int16)
    right_lane_inds = np.array([], dtype=np.int16)

    out_img = np.dstack((warped, warped, warped))

    nonzero = warped.nonzero()
    WhitePixelIndY = np.array(nonzero[0])
    WhitePixelIndX = np.array(nonzero[1])

    for window in range(nwindows):
        win_y1 = warped.shape[0] - (window+1) * windows_height
        win_y2 = warped.shape[0] - (window) * windows_height

        left_win_x1 = XCenterLeftWindow - window_half_width
        left_win_x2 = XCenterLeftWindow + window_half_width
        right_win_x1 = XcenterRightWindow - window_half_width
        right_win_x2 = XcenterRightWindow + window_half_width

        cv2.rectangle(out_img, (left_win_x1, win_y1), (left_win_x2, win_y2), (50 + window * 21, 0, 0), 2)
        cv2.rectangle(out_img, (right_win_x1, win_y1), (right_win_x2, win_y2), (0, 0, 50 + window * 21), 2)
        cv2.imshow("windows", out_img)

        good_left_inds = ((WhitePixelIndY >= win_y1) & (WhitePixelIndY <= win_y2) & (WhitePixelIndX >= left_win_x1) & (WhitePixelIndX <= left_win_x2)).nonzero()[0]
        good_right_inds = ((WhitePixelIndY >= win_y1) & (WhitePixelIndY <= win_y2) & (WhitePixelIndX >= right_win_x1) & (WhitePixelIndX <= right_win_x2)).nonzero()[0]

        left_lane_inds = np.concatenate((left_lane_inds, good_left_inds))
        right_lane_inds = np.concatenate((right_lane_inds, good_right_inds))

        if len(good_left_inds) > 50:
            XCenterLeftWindow = np.int(np.mean(WhitePixelIndX[good_left_inds]))
        if len(good_right_inds) > 50:
            XcenterRightWindow = np.int(np.mean(WhitePixelIndX[good_right_inds]))
    
    out_img[WhitePixelIndY[left_lane_inds], WhitePixelIndX[left_lane_inds]] = [255, 0, 0]
    out_img[WhitePixelIndY[right_lane_inds], WhitePixelIndX[right_lane_inds]] = [0, 0, 255]
    cv2.imshow("Lane", out_img)

    # вывод средней линии движения
    leftx = WhitePixelIndX[left_lane_inds]
    lefty = WhitePixelIndY[left_lane_inds]
    rightx = WhitePixelIndX[right_lane_inds]
    righty = WhitePixelIndY[right_lane_inds]
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)
    center_fit = ((left_fit+right_fit)/2)
    for ver_ind in range(out_img.shape[0]):
        gor_ind = ((center_fit[0])*(ver_ind**2) + center_fit[1] * ver_ind + center_fit[2])
        cv2.circle(out_img, (int(gor_ind), int(ver_ind)), 2, (255, 0, 255), 1)
    cv2.imshow("centerline", out_img)