from djitellopy.tello import Tello
import cv2

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
    
