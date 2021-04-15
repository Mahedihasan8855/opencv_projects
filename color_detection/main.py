import cv2 as cv
import numpy as  np


framewidth=300
framheight=200
cap= cv.VideoCapture(0)
cap.set(1,framewidth)
cap.set(2,framheight)

def empty(a):
    pass


cv.namedWindow("HSV")
cv.resizeWindow("HSV",640,240)
cv.createTrackbar("HUE MIN","HSV",0,179,empty)
cv.createTrackbar("HUE MAX","HSV",179,179,empty)
cv.createTrackbar("SAT MIN","HSV",0,255,empty)
cv.createTrackbar("SAT MAX","HSV",255,255,empty)
cv.createTrackbar("VALUE MIN","HSV",0,255,empty)
cv.createTrackbar("VALUE MAX","HSV",255,255,empty)



while True:
    isTrue, frame=cap.read()
    framehsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    h_min = cv.getTrackbarPos("HUE MIN","HSV")
    h_max = cv.getTrackbarPos("HUE MAX", "HSV")
    s_min = cv.getTrackbarPos("SAT MIN", "HSV")
    s_max = cv.getTrackbarPos("SAT MAX", "HSV")
    v_min = cv.getTrackbarPos("VALUE MIN", "HSV")
    v_max = cv.getTrackbarPos("VALUE MAX", "HSV")

    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv.inRange(framehsv,lower,upper)
    result=cv.bitwise_and(framehsv,framehsv,mask=mask)


    output = np.hstack((frame, framehsv, result))
    cv.imshow("Output",output)
    if cv.waitKey(1) & 0xff==ord("f"):
        break


cap.release()
cv.destroyAllWindows()