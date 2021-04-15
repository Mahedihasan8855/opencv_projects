import cv2 as cv
import numpy as np


framewidth=640
frameheight=280
cap=cv.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)

def empty(a):
    pass

cv.namedWindow("parameters")
cv.resizeWindow("parameters",640,80)
cv.createTrackbar("Threashold1","parameters",23,255,empty)
cv.createTrackbar("Threashold2","parameters",20,255,empty)


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getcontours(img,imgcontour):
    countours,hierarchy=cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)

    for i in countours:
        area=cv.contourArea(i)
        if area>1000:
            cv.drawContours(imgcontour,i,-1,(255,255,0),3)
            peri=cv.arcLength(i,True)
            approx=cv.approxPolyDP(i,0.02*peri,True)
            x,y,w,h=cv.boundingRect(approx)
            cv.rectangle(imgcontour,(x,y),(x+w,y+h),(255,0,255),4)
            cv.putText(imgcontour,"Points: "+str(len(approx)),(x+w+20,y+20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
            cv.putText(imgcontour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv.FONT_HERSHEY_COMPLEX, 0.7,(0, 255, 0), 2)





while True:
    success, img=cap.read()
    imgcountour=img.copy()
    imgblur=cv.GaussianBlur(img,(7,7),1)
    imggray=cv.cvtColor(imgblur,cv.COLOR_BGR2GRAY)
    threshold1=cv.getTrackbarPos("Threashold1","parameters")
    threshold2=cv.getTrackbarPos("Threashold2", "parameters")
    imgcanny=cv.Canny(imggray,threshold1,threshold2)
    kernel=np.ones((5,5),np.uint8)
    imgdil=cv.dilate(imgcanny,kernel,iterations=1)
    getcontours(imgdil,imgcountour)


    imgstack=stackImages(0.8,([img,imggray,imgcanny],[imgblur,imgcountour,imgcountour]))
    cv.imshow("Result",imgstack)
    if cv.waitKey(1) & 0xff==ord("f"):
        break
