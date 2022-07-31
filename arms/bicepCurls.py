import cv2
import math
from time import sleep
from utils.utilities import assignAngles, preprocessing
from utils.constants import *
from utils.helpers import * 

def Biceps(reps, sets, equipment):
    for _ in range(sets):
        COUNTER = 0
        STAGE = None
        cap = cv2.VideoCapture(0)
        if equipment == DUMBBELL or equipment == BARBELL :
            with mp_pose.Pose(min_detection_confidence=DETECTION, min_tracking_confidence=TRACKING) as pose:
                while cap.isOpened():
                    image,detections = preprocessing(cap,pose)
                    
                    try:
                        landmarks = detections.pose_landmarks.landmark 
                        leftShoulder,leftElbow,leftWrist,rightShoulder,rightElbow,rightWrist=get_coordinates(landmarks,BICEPS)
                        leftAngle = math.trunc(compute(leftShoulder, leftElbow, leftWrist))
                        rightAngle = math.trunc(compute(rightShoulder,rightElbow,rightWrist))

                        assignAngles(image,leftAngle,leftElbow,rightAngle,rightElbow)

                        if leftAngle > 160 and rightAngle > 160:
                            STAGE = DOWN
                        if leftAngle < 30 and rightAngle < 30 and STAGE == DOWN:
                            STAGE = UP
                            COUNTER +=1
                        if COUNTER == reps and STAGE == DOWN:
                            break

                    except:
                        pass

                    renderText(image, COUNTER, STAGE)
                    renderLandmarks(image, detections)           
                    
                    _,buffer=cv2.imencode('.jpg',image)
                    x=buffer.tobytes()
                    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')

        cap.release()
        cv2.destroyAllWindows()
        
        sleep(10)