### DOCUMENTATION GUIDE
### ---
### All Important Info is in Pound-Sign Comments (#)
### All unused code that was used in previous versions but is obsolete now is
### in Quotation Mark comments (''')
### ---
### Press the Q key on the keyboard to exit the script when its running
### ---
### Keshav Nath - 2K20/A9/47

import cv2
import numpy as np

'''
pinky=np.uint8([[[255,115,160]]])
hsv_pinky=cv2.cvtColor(pinky,cv2.COLOR_BGR2HSV)
print(hsv_pinky)
'''

#Lower and Upper limits of Hue for Red Color Detection
lower=np.array([170, 50, 50],np.uint8)
higher=np.array([180, 255, 255],np.uint8)

#A Kernel - 7x7 Pixels was found to be the ideal size for me - Used for Morphology
kernel = np.ones((7, 7), np.uint8)

#Capturing the WebCam
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Looping through each frame
while (True):
    #Reading current frame
    ret, frame= vid.read()

    #Converting frame to HSV Format
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Creating a mask to capture Red as 1 (White) and every other color as 0 (Black)
    mask=cv2.inRange(hsv, lower, higher)

    #Noise Removal using Morphology
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    #Bitwise-And to the regular frame and the mask to show only the colour that we're capturing
    res = cv2.bitwise_and(frame, frame, mask = mask)

    #Laterally inverting each video for easier viewing
    frame=cv2.flip(frame,1)
    mask=cv2.flip(mask,1)
    res=cv2.flip(res,1)

    #Finding contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Exploring the contour
    for pic, contour in enumerate(contours): 
        #Finding area of each contour
        area = cv2.contourArea(contour) 

        #Only dealing with the larger contours, so that
        #any accidental noise is not considered for the angle or the circle
        if(area > 3000): 
            '''
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame,[box],0,(0,0,255),2)
            '''

            #Drawing the circle around the detected arrow
            (x,y),radius = cv2.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(frame,center,radius,(0,255,0),2)

            #Imagining an Elipse around the contour to find its center and its angle
            cords,axes,angle = cv2.fitEllipse(contour)
            x,y=cords[:2]
            x,y=int(x),int(y)

            #Writing angle on the center of the Arrow
            cv2.putText(frame, f"A={int(angle)}",(x,y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))

            '''
            print(f"X={cords[0]}\nY={cords[1]}\nAngle={angle}\n")
            print(axes)
            '''

            '''
            rows,cols = frame.shape[:2]
            [vx,vy,x0,y0] = cv2.fitLine(contour, cv2.DIST_L2,0,0.01,0.01)
            lefty = int((-x0*vy/vx) + y0)
            righty = int(((cols-x0)*vy/vx)+y0)
            cv2.putText(frame, f"LY={lefty}",(x,y+20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
            cv2.putText(frame, f"RY={righty}",(x,y+40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
            #frame = cv2.line(frame,(cols-1,righty),(0,lefty),(0,255,0),2)
            '''

            '''
            x, y, w, h = cv2.boundingRect(contour) 
            frame = cv2.rectangle(frame, (x, y),  
                                       (x + w, y + h),  
                                       (255, 0, ), 2) 
            
            cv2.putText(frame, "Arrow", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (255, 255, 0))
            '''
    #Showing the final video, the mask, and the coloured mask       
    try:
        cv2.imshow('Video',frame)
        cv2.imshow('Mask',mask)
        cv2.imshow('Colour',res)
    #Try|Except block because an error crashed my laptop, so I'm saving you
    except:
        print("ERROR")

    #Condition for Exiting Video on pressing the 'Q' Key
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        vid.release()
        cv2.destroyAllWindows()
        break

#Final message to acknowledge smooth running of code
print("FINIT.")
