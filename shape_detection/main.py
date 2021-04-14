import cv2 as cv
import numpy as np


framewidth=640
frameheight=280
cap=cv.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)



while True:
    success, img=cap.read()


    cv.imshow("Result",img)
    if cv.waitKey(1) & 0xff==ord("f"):
        break
