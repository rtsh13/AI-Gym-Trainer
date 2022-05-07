# Importing Libraries
from time import sleep
import numpy as np
import cv2
import math 
import mediapipe as mp
from helpers import *
from constants import *

def PushupsExercise():
    sets,reps,equipment,exercise_name,port = form()
    for val in sets:
        COUNTER = 0
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
                    leftShoulder,leftElbow,leftWrist,rightShoulder,rightElbow,rightWrist = get_coordinates(landmarks,exercise_name)

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
                            STAGE = "UP"
                    if leftAngle < 130 and rightAngle < 130 and STAGE == "UP":
                            STAGE="DOWN"
                            COUNTER +=1
                    if COUNTER == reps and STAGE == "UP":
                            print("Congrats for making it this far, Take a break, you have finished your set" + val)
                            break

                except:
                    pass

                renderText(image=image, COUNTER=COUNTER,STAGE=STAGE)

                # Render detections
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

        
# Voice guided output for finishing the exercise -> enhancement to integrate with frontend
# engine = pyttsx3.init()
# engine.setProperty("rate",150)
# engine.say(f"Congratulations! you finished the {diamondPushups} with {COUNTER} reps")
# engine.runAndWait()