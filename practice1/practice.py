import cv2
import numpy as np

coin = cv2.imread("mariocoin.jpg")

h,w = coin.shape[:2]
center = (w/2, h/2)
#scale = 1.0
#angle = 0

for angle in range(0, 360, 30):
    for scale in range(10, 20, 1):
        m = cv2.getRotationMatrix2D(center, angle, 1)
        img=cv2.warpAffine(coin, m, (h, w))
        img=cv2.resize(img, (0, 0), fx=scale/10, fy=scale/10)
        cv2.imshow("Woop", img)
        cv2.waitKey(100)
    cv2.destroyAllWindows()
        
