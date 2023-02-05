import cv2
import math
from time import sleep
from utils.utilities import assignAngles, preprocessing
from utils.constants import *
from utils.helpers import * 

def KneePushups(reps, sets):
    for _ in range(sets):
        COUNTER = 0
        STAGE=None
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(min_detection_confidence=DETECTION, min_tracking_confidence=TRACKING) as pose:
            while cap.isOpened():
                image,detections = preprocessing(cap,pose)
                
                try:
                    landmarks = detections.pose_landmarks.landmark
                    leftShoulder,leftElbow,leftWrist,rightShoulder,rightElbow,rightWrist = get_coordinates(landmarks, PUSHUPS)
                    leftAngle = math.trunc(compute(leftShoulder, leftElbow, leftWrist))
                    rightAngle = math.trunc(compute(rightShoulder,rightElbow,rightWrist))
                    
                    assignAngles(image,leftAngle,leftElbow,rightAngle,rightElbow)

                    if leftAngle > 160 and rightAngle > 160:
                            STAGE = UP
                    if leftAngle < 130 and rightAngle < 130 and STAGE == UP:
                            STAGE = DOWN
                            COUNTER += 1
                    if COUNTER == reps and STAGE == UP:
                            print("Congrats for making it this far, Take a break, you have finished your set")
                            break

                except:
                    pass

                renderText(image,COUNTER,STAGE)
                renderLandmarks(image,detections)           
                
                _,buffer=cv2.imencode('.jpg',image)
                x=buffer.tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')

            cap.release()
            cv2.destroyAllWindows()
        
        sleep(10)
