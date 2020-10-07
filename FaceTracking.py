from TelloUtils import *
import cv2

w,h = 640,480

myDrone = initTello()
while True:
    #1단계. cv2 라이브러리를 활용해 텔로의 카메라화면 보여주기
    img = getTelloFrame(myDrone,w,h)
    #2단계. 얼굴정보를 가져오기
    img,faceInfo = findFace(img) #faceInfo[0][0]은 얼굴 중심 x좌표, faceInfo[0][1]은 얼굴 중심 y좌표, faceInfo[1]은 얼굴면적
    cv2.imshow('Image',img)
    #멈추기. 안전상으로 필요한 코드
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break
