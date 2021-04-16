import cv2 as cv
import numpy as np

framewidth=640
frameheight=280
cap=cv.VideoCapture(0)

cap.set(3,framewidth)
cap.set(4,frameheight)

while True:
    timer=cv.getTickCount()
    suceess,frame=cap.read()

    fps=cv.getTickFrequency()/(cv.getTickCount()-timer)
    cv.putText(frame, "FPS:"+str(int(fps)), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv.LINE_AA)
    cv.imshow("Obeject Tracking",frame)
    if cv.waitKey(0) & 0xff == ord("f"):
        break