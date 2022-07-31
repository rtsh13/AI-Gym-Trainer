import imp
import cv2
import math
from time import sleep
from utils.utilities import assignAngles, preprocessing
from utils.constants import *
from utils.helpers import * 

def JumpingJacks(reps, sets):
    for _ in range(sets):
        COUNTER = 0
        STAGE = None
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(min_detection_confidence=DETECTION, min_tracking_confidence=TRACKING) as pose:
            while cap.isOpened():
                image,detections = preprocessing(cap,pose)

                try:
                    landmarks = detections.pose_landmarks.landmark
                    leftShoulder,leftElbow,leftWrist,leftHip,leftKnee,leftAnkle,rightShoulder,rightElbow,rightWrist,rightHip,rightKnee,rightAnkle = get_coordinates(landmarks,JUMPING_JACKS)
                    leftAngleTop = math.trunc(compute(leftShoulder, leftElbow, leftWrist))
                    rightAngleTop = math.trunc(compute(rightShoulder,rightElbow,rightWrist))
                    leftAngleBottom = math.trunc(compute(leftAnkle,leftHip,rightHip))
                    rightAngleBottom = math.trunc(compute(rightAnkle,rightHip,leftHip))
                    
                    assignAngles(image,leftAngleTop,leftElbow,rightAngleTop,rightElbow)
                    assignAngles(image,leftAngleBottom,leftHip,rightAngleBottom,rightHip)

                    if leftAngleTop > 165 and rightAngleTop > 165:
                        STAGE = DOWN
                    if leftAngleTop < 150 and rightAngleTop < 150 and STAGE == DOWN:
                        STAGE = UP
                        COUNTER +=1
                    if COUNTER == reps and STAGE == DOWN:
                        print("Congrats for making it this far, Take a break, you have finished your set")
                        break

                except:
                    pass

                renderText(image, COUNTER, STAGE)
                renderLandmarks(image,detections)           
                
                _,buffer=cv2.imencode('.jpg',image)
                x=buffer.tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')

        cap.release()
        cv2.destroyAllWindows()
    
        sleep(10)
