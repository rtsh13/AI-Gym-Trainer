import cv2
import math
from time import sleep
from utils.utilities import assignAngles, preprocessing
from utils.constants import *
from utils.helpers import * 

def Lunges(reps,sets):
    for _ in range(0,sets+1):
        COUNTER = 0
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(min_detection_confidence=DETECTION, min_tracking_confidence=TRACKING) as pose:
            while cap.isOpened():
                image, detections = preprocessing(cap, pose)

                try:
                    landmarks = detections.pose_landmarks.landmark
                    rightHeel,rightKnee,rightHip,leftHeel,leftKnee,leftHip = get_coordinates(landmarks,LUNGES)
                    leftAngle = math.trunc(compute(leftHip, leftKnee,leftHeel))
                    rightAngle = math.trunc(compute(rightHip,rightKnee,rightHeel))
                    
                    assignAngles(image, leftAngle, leftKnee, rightAngle, rightKnee)

                    if leftAngle < 120 and rightAngle < 120 and STAGE == UP:
                        STAGE = DOWN
                    if leftAngle > 160 and rightAngle > 160:
                        STAGE = UP
                        COUNTER += 1 
                    if COUNTER == reps and STAGE == UP:
                        print("Congrats for making it this far, Take a break, you have finished your set")
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
