from djitellopy.tello import Tello
import cv2

#step1
def initTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity=0
    myDrone.up_down_velocity=0
    myDrone.yaw_velocity=0
    myDrone.speed=0
    print(myDrone.get_battery())
    myDrone.streamoff() #이전 연결이 있을시 오류가 발생하므로 한번 stream을 끊어줘야 소켓통신이 잘 됩니다.
    myDrone.streamon()
    return myDrone

def getTelloFrame(myDrone, w=360, h=240):
    myFrame = myDrone.get_frame_read().frame
    IMG = cv2.resize(myFrame,(w,h))
    return IMG

#step2
def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img,cv2.COLOR_BAYER_BG2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,4) #1.2,4는 scalefactor, 다른값으로 바꿔도 된다.

    #프레임마다 두 리스트에 얼굴 면적, 중심점 정보를 계속 집어넣는다.
    FaceCenterList = []
    FaceAreaList = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        FaceAreaList.append(area)
        FaceCenterList.append([cx, cy])

    #리스트의 맨 마지막 부분의 idx를 가져와 면적과 중심정보를 리턴한다.
    if len(FaceAreaList):
        idx = FaceAreaList.index(max(FaceAreaList))
        return img, [FaceCenterList[idx], FaceAreaList[idx]]
    else:
        return img, [[0, 0], 0]
