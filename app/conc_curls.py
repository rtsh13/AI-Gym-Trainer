# Importing Libraries
from time import sleep
import numpy as np
import cv2
import math 
import mediapipe as mp
from helpers import *
from constants import *

def ConCurlsExercise():
    sets,reps,equipment,exercise_name,port = form()
    for val in sets:
        COUNTER = 0
        flag=0
        cap = cv2.VideoCapture(port)
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.6) as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                detections = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = detections.pose_landmarks.landmark
                    leftShoulder,leftElbow,leftWrist,rightShoulder,rightElbow,rightWrist=get_coordinates(landmarks,exercise_name)
                    leftAngle = math.trunc(compute(leftShoulder, leftElbow, leftWrist))
                    rightAngle = math.trunc(compute(rightShoulder,rightElbow,rightWrist))

                    cv2.putText(image, str(leftAngle), 
                                tuple(np.multiply(leftElbow, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA
                                )
                    
                    cv2.putText(image, str(rightAngle), 
                                tuple(np.multiply(rightElbow, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA
                                )

                    if flag ==0:
                        if leftAngle > 160:
                            STAGE = "DOWN"
                        if leftAngle < 30 and STAGE =="DOWN":
                            STAGE="UP"
                            COUNTER +=1
                        if COUNTER == reps and STAGE == "DOWN":
                            print("Congrats for making it this far, Take a break, you have finished your set" + val)
                            flag=1
                            COUNTER=0
                            
                    elif flag==1:
                        if rightAngle > 160:
                            STAGE = "DOWN"
                        if rightAngle < 30 and STAGE =="DOWN":
                            STAGE="UP"
                            COUNTER +=1
                        if COUNTER == reps and STAGE == "DOWN":
                            print("Congrats for making it this far, Take a break, you have finished your set", + val)
                            break
                    

                except:
                    pass

                renderText(image=image, COUNTER=COUNTER,STAGE=STAGE)
                drawing.draw_landmarks(image, detections.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2), 
                                        drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2))               
                
                _,buffer=cv2.imencode('.jpg',image)
                x=buffer.tobytes()
                yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')

        cap.release()
        cv2.destroyAllWindows()
        
        sleep(10)

    # cv2.rectangle(image, (500, 0),(800,80),(0,0,0), -1)    
    # cv2.putText(image, str(STAGE), (500,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,255,0), 2, cv2.LINE_AA)