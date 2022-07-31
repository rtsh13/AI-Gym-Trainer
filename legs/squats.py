import cv2
import math
from time import sleep
from utils.utilities import assignAngles, preprocessing
from utils.constants import *
from utils.helpers import * 

def Squats(reps, sets):
    for _ in range(sets):
        COUNTER = 0
        STAGE = None
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(min_detection_confidence = DETECTION, min_tracking_confidence = TRACKING) as pose:
            while cap.isOpened():
                image, detections = preprocessing(cap, pose)
                try:
                    landmarks = detections.pose_landmarks.landmark

                    leftHip,leftKnee,leftAnkle,rightHip,rightKnee,rightAnkle=get_coordinates(landmarks,SQUATS)
                    leftBottomAngle = math.trunc(compute(leftHip, leftKnee, leftAnkle))
                    rightBottomAngle = math.trunc(compute(rightHip,rightKnee,rightAnkle))

                    assignAngles(image, leftBottomAngle,leftKnee,rightBottomAngle, rightKnee)

                    if leftBottomAngle < 90 and rightBottomAngle < 90:
                        STAGE = DOWN
                    if STAGE == DOWN and leftBottomAngle > 160 and rightBottomAngle > 160:
                        STAGE=UP
                        COUNTER +=1
                    if COUNTER == reps and STAGE == DOWN:
                        print("Congrats for making it this far, Take a break, you have finished your set")
                        break

                except:
                    pass

                renderText(image, COUNTER, STAGE)
                renderLandmarks(image, detections)           

                _,buffer=cv2.imencode('.jpg', image)
                x=buffer.tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')

        cap.release()
        cv2.destroyAllWindows()
        
        sleep(10)
