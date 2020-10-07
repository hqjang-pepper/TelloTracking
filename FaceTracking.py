from TelloUtils import *
import cv2

w,h = 640,480

myDrone = initTello()
while True:
    #1단계. cv2 라이브러리를 활용해 텔로의 카메라화면 보여주기
    img = getTelloFrame(myDrone,w,h)
    cv2.imshow('Image',img)
    #멈추기. 안전상으로 필요한 코드
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break
