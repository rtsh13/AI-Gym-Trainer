import cv2
import math
from time import sleep
from utils.utilities import assignAngles, preprocessing
from utils.constants import *
from utils.helpers import * 

def SideLegLifting(reps,sets):
    for _ in range(sets):
        COUNTER = 0
        flag = 0
        STAGE = None
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(min_detection_confidence=DETECTION, min_tracking_confidence=TRACKING) as pose:
            while cap.isOpened():
                image, detections = preprocessing(cap,pose)
                try:
                    landmarks = detections.pose_landmarks.landmark
                    leftElbow,leftShoulder,rightElbow,rightShoulder,leftHip,leftKnee,rightHip,rightKnee = get_coordinates(landmarks, SIDE_LEG_LIFTING)
                    leftAngle = math.trunc(compute(leftShoulder, leftHip, leftKnee))
                    rightAngle = math.trunc(compute(rightShoulder,rightHip,rightKnee))

                    assignAngles(image, leftAngle, leftElbow, rightAngle, rightElbow)

                    if flag == 0:
                        if leftAngle > 160:
                            STAGE = DOWN
                        if leftAngle < 130 and STAGE == DOWN:
                            STAGE = UP
                            COUNTER +=1
                        if COUNTER == reps and STAGE == DOWN:
                            print("Congrats for making it this far, Take a break, you have finished your set")
                            flag = 1
                            COUNTER = 0

                    elif flag == 1:
                        if rightAngle > 160:
                            STAGE = DOWN
                        if rightAngle < 130 and STAGE == DOWN:
                            STAGE="UP"
                            COUNTER +=1
                        if COUNTER == reps and STAGE == DOWN:
                            print("Congrats for making it this far, Take a break, you have finished your set")
                            break

                except:
                    pass

                renderText(image, COUNTER, STAGE)
                renderLandmarks(image, landmarks) 
                
                _,buffer=cv2.imencode('.jpg', image)
                x=buffer.tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')

        cap.release()
        cv2.destroyAllWindows()
        
        sleep(10)
