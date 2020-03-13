import numpy as np
import cv2 


while (True):
    ret, frame = cap.read()
    cv2.imshow("Frame", frame)

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    lower_red = np.array([0, 85, 110], dtype = "uint8")
    upper_red = np.array([15, 255, 255], dtype = "uint8")
 
    lower_violet = np.array([165, 85, 110], dtype = "uint8")
    upper_violet = np.array([180, 255, 255], dtype = "uint8")
 
    red_mask_orange = cv2.inRange(frame_hsv, lower_red, upper_red)        #применяем маску по цвету
    red_mask_violet = cv2.inRange(frame_hsv, lower_violet, upper_violet)  #для красного таких 2
 
    red_mask_full = red_mask_orange + red_mask_violet
    lower_green = np.array([40, 85, 110], dtype = "uint8")
    upper_green = np.array([91, 255, 255], dtype = "uint8")

    green_mask = cv2.inRange(converted, lower_green, upper_green)

    last_red_frame = None   #задаем пустые прошлые кадры
    last_green_frame = None #красные и зеленые, для дальнейшей работы

    #рассчитываем зеленые и красные маски для текущего кадра
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask_frame = red_mask(frame_hsv)
    green_mask_frame = green_mask(frame_hsv)
    
    #проверяем прошлые кадры, если они пустые - заполняем их текущими 
    #масками
    if last_red_frame is None:
        last_red_frame = red_mask_frame
    if last_green_frame is None:
        last_green_frame = green_mask_frame
    
    #здесь находиться логика по получению разницы в кадрах
    #заметьте, что порядок в действиях для зеленого и красного кадра различный, это надо из логики - красный гаснет, зеленый загорается
    red_dif_frame = (last_red_frame-red_mask_frame)
    green_dif_frame = (green_mask_frame-last_green_frame)
    
    #здесь мы делаем отсечку для изображений, так как в процессе вычитания мы получаем следующие цифры
    #255-0=0    0-0=0    0-255=1 мы боремся с последним случаем
    ret, red_dif_frame = cv2.threshold(red_dif_frame,127,255,cv2.THRESH_BINARY)
    ret, green_dif_frame = cv2.threshold(green_dif_frame,127,255,cv2.THRESH_BINARY)
    
    last_green_frame = green_mask_frame
    last_red_frame = red_mask_frame
    
    #отрисовываем оба кадра
    cv2.imshow("red_dif_frame", red_dif_frame)
    cv2.imshow("green_dif_frame", green_dif_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1);
