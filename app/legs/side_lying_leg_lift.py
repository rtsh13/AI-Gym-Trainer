# Importing Libraries
from time import sleep
import numpy as np
import cv2
import math 
# import pyttsx3
import mediapipe as mp
drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles

# Importing packages
from helpers import *

import os
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
print("PATH:", os.environ.get('PATH'))

# Get User Input
sets = input("Please enter the desired number of sets:")
repsForSets = {}

for i in range(1,int(sets)+1):
    reps = int(input(f"Enter the number of reps for set {i}: ")) 
    repsForSets[i] = reps

# Initialize video capture 
print("Establising connection\n")
print(".........")
sleep(1)
port = int(input(f"Are you using an external or internal camera? Enter 1 for external,0 for internal : "))

if port < 0 or port > 1:
    print("Eh, Technical Glitch")
    exit(0)

for sets in repsForSets:
    COUNTER = 0
    flag =0
    cap = cv2.VideoCapture(port)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.6) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            detections = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = detections.pose_landmarks.landmark
                
                # Get coordinates
                leftWrist,leftElbow,leftShoulder,rightWrist,rightElbow,rightShoulder,leftHip,leftKnee,leftAnkle,rightHip,rightKnee,rightAnkle=get_coordinates(landmarks,"squats")

                # Calculate the angles
                leftAngle = math.trunc(compute(leftShoulder, leftHip, leftKnee))
                rightAngle = math.trunc(compute(rightShoulder,rightHip,rightKnee))

                # leftBottomAngle = math.trunc(compute(leftHip, leftKnee, leftAnkle))
                # rightBottomAngle = math.trunc(compute(rightHip,rightKnee,rightAnkle))


                # Visualize angle
                cv2.putText(image, str(leftAngle), 
                            tuple(np.multiply(leftElbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA
                            )
                
                cv2.putText(image, str(rightAngle), 
                            tuple(np.multiply(rightElbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA
                            )

                # Curl counter logic
                if flag==0:
                    if leftAngle > 160:
                        STAGE = "DOWN"
                    if leftAngle < 130 and STAGE =="DOWN":
                        STAGE="UP"
                        COUNTER +=1
                    if COUNTER == repsForSets[sets] and STAGE == "DOWN":
                        print("Congrats for making it this far, Take a break, you have finished your set")
                        flag=1
                        COUNTER=0
                elif flag == 1:
                    if rightAngle > 160:
                        STAGE = "DOWN"
                    if rightAngle < 130 and STAGE =="DOWN":
                        STAGE="UP"
                        COUNTER +=1
                    if COUNTER == repsForSets[sets] and STAGE == "DOWN":
                        print("Congrats for making it this far, Take a break, you have finished your set")
                        break
                # if leftTopAngle > 160 and rightTopAngle > 160 and leftBottomAngle<90 and rightBottomAngle<90:
                #     STAGE = "DOWN"
                # if leftTopAngle < 120 and rightTopAngle < 120 and STAGE =="DOWN" and leftBottomAngle>160 and rightBottomAngle>160:
                #     STAGE="UP"
                #     COUNTER +=1
                # if COUNTER == repsForSets[sets] and STAGE == "DOWN":
                #     print("Congrats for making it this far, Take a break, you have finished your set")
                #     break

            except:
                pass

            renderText(image=image, COUNTER=COUNTER,STAGE=STAGE)

            # Render detections
            drawing.draw_landmarks(image, detections.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2), 
                                    drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2))               
            
            cv2.imshow('Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    
    sleep(10)

# Voice guided output for finishing the exercise -> enhancement to integrate with frontend
# engine = pyttsx3.init()
# engine.setProperty("rate",150)
# engine.say(f"Congratulations! you finished the {bicepCurls}  with {COUNTER} reps")
# engine.runAndWait()        
