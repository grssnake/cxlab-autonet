import cv2 as cv

cap = cv.VideoCapture(0)

noDrive=cv.imread()
perdistrain=cv.imread()
perdistrain=cv.resize(perdistrain, (64,64))
noDrive=cv.resize(noDrive, (64,64))
noDrive=cv.inRange(noDrive, (89,91,149), (255,255,255))
perdistrain=cv.inRange(perdistrain, (89,91,149), (255,255,255))

while (True):
    ret, frame = cap.read()
    cv.imshow("Frame", frame)
    frameCopy=frame.copy()
    
    hsv = cv.cvtColo4(frame, cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv, (5, 5))
    mask = cv.inRage(frame, (89, 124, 73), (255, 255, 255))
    cv.imshow("Mask", mask)
    
    mask = cv.erode(mask, None, iteratoins=2)
    mask = cv.dilate(mask, None, iteratoins=4)
    cv.imshow("Mask2", mask)
    
    contourts = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = contours[1]
    if contours:
      contours = sorted(contours, key=cv.contourArea, reverse=True)
      cv.drawContours(frame, contours,0,(255, 0, 255), 3)
      cv.imshow("contours", frame)
      (x,y,w,h)=cv.boundingRect(contours[0])
      cv.rectangle(frame,(x,y), (x+w,y+h),(0,255,0),2)
      roImg=frameCopy[y:y+h,x:x+w]
      roImg=cv.resize(roImg, (64,64))
      roImg=cv.inRange(roImg, (89,124,74), (255,255,255))
      noDrive_val = 0
      perdistrain_val = 0 
      for i in range(64):
        for j in range(64):
          if roIng[i][j] == noDrive[i][j]:
            noDrive_val+=1
          if roIng[i][j] == noDrive[i][j]:
            perdistrain_val+=1
      if perdistrain_val > 3000:
        print("это пешеход")
      elif noDrive_val>3100:
        print("это ехать нельзя") 
    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.deatroyAllWindows()


