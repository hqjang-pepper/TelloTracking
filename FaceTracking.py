from djitellopy.tello import Tello
import cv2

startCounter = 0  # 한번 띄운 후 1로 조정

TOLERANCE_X = 5
TOLERANCE_Y = 5
SLOWDOWN_THRESHOLD_X = 20
SLOWDOWN_THRESHOLD_Y = 20
DRONE_SPEED_X = 20
DRONE_SPEED_Y = 20
SET_POINT_X = 960/2
SET_POINT_Y = 720/2

myDrone = Tello()
myDrone.connect()
myDrone.for_back_velocity = 0
myDrone.left_right_velocity = 0
myDrone.up_down_velocity = 0
myDrone.yaw_velocity = 0
myDrone.speed = 0
print(myDrone.get_battery())
myDrone.streamoff()  # 이전 연결이 있을시 오류가 발생하므로 한번 stream을 끊어줘야 소켓통신이 잘 됩니다.
myDrone.streamon()

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
while True:
    ## Flight
    if startCounter == 0:
        myDrone.takeoff()
        print('takeoff')
        startCounter = 1


    frame = myDrone.get_frame_read().frame  # 드론
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 회색 스케일로 변환

    faces = faceCascade.detectMultiScale(  # 얼굴 탐지
        gray,
        scaleFactor=1.1,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    i = 0
    #
    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  # 인식된 얼굴 직사각형으로 표시
        cv2.circle(frame, (int(x+w/2), int(y+h/2)), 12, (255, 0, 0), 1)  # 얼굴 중심(원) 화면에 표시


        cv2.circle(frame, (int(SET_POINT_X), int(SET_POINT_Y)), 12, (255, 255, 0), 3)  # 화면 중간에 원 표시(영점)
        i+=1
        distanceX = x+w/2 - SET_POINT_X
        distanceY = y+h/2 - SET_POINT_Y

        up_down_velocity = 0
        right_left_velocity = 0

        if distanceX < -TOLERANCE_X:
            print("드론을 왼쪽으로 이동")
            right_left_velocity = - DRONE_SPEED_X

        elif distanceX > TOLERANCE_X:
            print("드론을 오른쪽으로 이동")
            right_left_velocity = DRONE_SPEED_X
        else:
            print("OK")

        if distanceY < -TOLERANCE_Y:
            print("드론을 위로 이동")
            up_down_velocity = DRONE_SPEED_Y
        elif distanceY > TOLERANCE_Y:
            print("드론을 아래로 이동")
            up_down_velocity = - DRONE_SPEED_Y
        else:
            print("OK")

        if abs(distanceX) < SLOWDOWN_THRESHOLD_X:
            right_left_velocity = int(right_left_velocity / 2)
        if abs(distanceY) < SLOWDOWN_THRESHOLD_Y:
            up_down_velocity = int(up_down_velocity / 2)

        myDrone.send_rc_control(right_left_velocity, 0, up_down_velocity, 0)

    cv2.imshow('Video', frame)  # mostra il frame sul display del pc

    if cv2.waitKey(1) & 0xFF == ord('q'):  # quit from script
        break
