# Importing Libraries
from time import sleep
import numpy as np
import cv2
import math 
import mediapipe as mp
drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles

# Importing packages
from helpers import *
from constants import *

# Get User Input
sets,equipment = input("Please enter the desired number of sets and equipment to be used:").split()
repsForSets = {}

for i in range(1,int(sets)+1):
    reps = int(input(f"Enter the number of reps for set {i}: ")) 
    repsForSets[i] = reps

for sets in repsForSets:
    # Initialize video capture 
    vc = cv2.VideoCapture(1)
    if not vc.read()[0]:
        vc = cv2.VideoCapture(0)

    COUNTER = 0
    cap = cv2.VideoCapture(0)
    if equipment == defaultEquipment or equipment == bicepEquiment:
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
                    leftShoulder,leftElbow,leftWrist,leftHip,leftKnee,rightShoulder,rightElbow,rightWrist,rightHip,rightKnee=get_coordinates(landmarks)

                    # Calculate the angles
                    leftAngle = math.trunc(compute(leftShoulder, leftElbow, leftWrist))
                    rightAngle = math.trunc(compute(rightShoulder,rightElbow,rightWrist))

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
                    if leftAngle > 160 and rightAngle > 160:
                        STAGE = "DOWN"
                    if leftAngle < 30 and rightAngle < 30 and STAGE =="DOWN":
                        STAGE="UP"
                        COUNTER +=1
                    if COUNTER == repsForSets[sets] and STAGE == "DOWN":
                        print("Congrats for making it this far, Take a break, you have finished your set")
                        break

                except:
                    pass

                renderText()

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

        
