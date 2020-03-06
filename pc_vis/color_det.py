cap = cv2.VideoCapture(0)
#с зеленым все проще - он в центре диапазона
lower_green = np.array([40, 85, 110], dtype = "uint8")
upper_green = np.array([91, 255, 255], dtype = "uint8")
    
#применяем маску
green_mask = cv2.inRange(converted, lower_green, upper_green)
last_green_frame = None #красные и зеленые, для дальнейшей работы
while(cap.isOpened()):
    ret, frame = cap.read()
    if frame is None:
        break
 
    #рассчитываем зеленые и красные маски для текущего кадра
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    green_mask_frame = green_mask(frame_hsv)
    
    #проверяем прошлые кадры, если они пустые - заполняем их текущими 
    #масками
    if last_green_frame is None:
        last_green_frame = green_mask_frame
    
    #здесь находиться логика по получению разницы в кадрах
    #заметьте, что порядок в действиях для зеленого и красного кадра различный, это надо из логики - красный гаснет, зеленый загорается
    green_dif_frame = (green_mask_frame-last_green_frame)
    
    #здесь мы делаем отсечку для изображений, так как в процессе вычитания мы получаем следующие цифры
    #255-0=0    0-0=0    0-255=1 мы боремся с последним случаем
    ret, green_dif_frame = cv2.threshold(green_dif_frame,127,255,cv2.THRESH_BINARY)
    
    last_green_frame = green_mask_frame
    
    #отрисовываем оба кадра
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
