import cv2
import math
from time import sleep
from utils.utilities import assignAngles, preprocessing
from utils.constants import *
from utils.helpers import * 

def ConcentrationCurls(reps, sets, equipment):
    for _ in range(sets):
        COUNTER = 0
        STAGE = None
        flag = 0
        cap = cv2.VideoCapture(0)
        if equipment == DUMBBELL:
            with mp_pose.Pose(min_detection_confidence=DETECTION, min_tracking_confidence=TRACKING) as pose:
                    while cap.isOpened():
                        image,detections = preprocessing(cap,pose)
                        try:
                            landmarks = detections.pose_landmarks.landmark
                            leftShoulder,leftElbow,leftWrist,rightShoulder,rightElbow,rightWrist=get_coordinates(landmarks,CONCCURLS)
                            leftAngle = math.trunc(compute(leftShoulder, leftElbow, leftWrist))
                            rightAngle = math.trunc(compute(rightShoulder,rightElbow,rightWrist))
                            
                            assignAngles(image,leftAngle,leftElbow,rightAngle,rightElbow)

                            if flag == 0:
                                if leftAngle > 160:
                                    STAGE = DOWN
                                if leftAngle < 30 and STAGE == DOWN:
                                    STAGE = UP
                                    COUNTER +=1
                                if COUNTER == reps and STAGE == DOWN:
                                    print("Congrats for making it this far, Take a break, you have finished your set")
                                    flag=1
                                    COUNTER=0
                                    
                            elif flag == 1:
                                if rightAngle > 160:
                                    STAGE = DOWN
                                if rightAngle < 30 and STAGE == DOWN:
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

    # cv2.rectangle(image, (500, 0),(800,80),(0,0,0), -1)    
    # cv2.putText(image, str(STAGE), (500,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,255,0), 2, cv2.LINE_AA)