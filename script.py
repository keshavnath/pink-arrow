import cv2
import numpy as np

pinky=np.uint8([[[255,115,160]]])
hsv_pinky=cv2.cvtColor(pinky,cv2.COLOR_BGR2HSV)
#print(hsv_pinky)

lower=np.array([170, 50, 50],np.uint8)
higher=np.array([180, 255, 255],np.uint8)

kernel = np.ones((5, 5), np.uint8)

vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while (True):
    ret, frame= vid.read()

    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(hsv, lower, higher)

    #NOISE REMOVAL
    mask=cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask=cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    res = cv2.bitwise_and(frame, frame, mask = mask)

    frame=cv2.flip(frame,1)
    mask=cv2.flip(mask,1)
    res=cv2.flip(res,1)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 3000): 
            '''
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame,[box],0,(0,0,255),2)
            '''

            (x,y),radius = cv2.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(frame,center,radius,(0,255,0),2)

            cords,axes,angle = cv2.fitEllipse(contour)
            x,y=cords[:2]
            x,y=int(x),int(y)
            #print(f"X={cords[0]}\nY={cords[1]}\nAngle={angle}\n")
            cv2.putText(frame, f"A={int(angle)}",(x,y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
            '''
            x, y, w, h = cv2.boundingRect(contour) 
            frame = cv2.rectangle(frame, (x, y),  
                                       (x + w, y + h),  
                                       (255, 0, ), 2) 
            
            cv2.putText(frame, "Arrow", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (255, 255, 0))
            '''
    try:
        cv2.imshow('Video',frame)
        cv2.imshow('Mask',mask)
        cv2.imshow('Colour',res)
    except:
        print("ERROR")

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        vid.release()
        cv2.destroyAllWindows()
        break
