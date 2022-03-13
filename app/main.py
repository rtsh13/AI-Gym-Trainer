# Importing Libraries
from matplotlib.pyplot import draw
import numpy as np
import ctypes
import cv2
import math 
import mediapipe as mp
import pyttsx3
from time import sleep
from  helpers.helper import *
drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize video capture for external webcam 
vc = cv2.VideoCapture(1)

# Using internal webcam, if external not present
if not vc.read()[0]:
    vc = cv2.VideoCapture(0)

cap = cv2.VideoCapture(0)

# Curl counter variables
COUNTER = 0 
STAGE = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
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
            shoulder,elbow, wrist,left_hip,left_knee,right_shoulder,right_elbow,right_wrist=get_coordinates(landmarks)


            # Calculate the angles
            angle = math.trunc(compute(shoulder, elbow, wrist))
            rangle = math.trunc(compute(right_shoulder,right_elbow,right_wrist))

            # Visualize angle
            cv2.putText(image, str(angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            cv2.putText(image, str(rangle), 
                           tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

            # Curl counter logic
            if angle > 160 and rangle > 160:
                STAGE = "down"
            if angle < 30 and rangle < 30 and STAGE =='down':
                STAGE="up"
                COUNTER +=1
            if COUNTER == 4 and STAGE == "down":
                break
                        
        except:
            print("Unable to fetch the landmarks, please face the camera upright!")
 
        cv2.putText(image, str(COUNTER), (12,60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,0), 2, cv2.LINE_AA)
        cv2.putText(image, str(STAGE), (500,60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,0), 2, cv2.LINE_AA)

        # Render detections
        drawing.draw_landmarks(image, detections.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                )               
        
        cv2.imshow('Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

# Delay the execution by 1 second
sleep(1)

# Voice guided output for finishing the exercise -> enhancement to integrate with frontend
engine = pyttsx3.init()
engine.setProperty("rate",150)
engine.say(f"Congratulations! you finished the exercise with {COUNTER} reps")
engine.runAndWait()
