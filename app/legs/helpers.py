import numpy as np
import mediapipe as mp
import cv2
from constants import *
drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def compute(firstAngle,secondAngle, thirdAngle):
    firstAngle = np.array(firstAngle) # First
    secondAngle = np.array(secondAngle) # Mid
    thirdAngle = np.array(thirdAngle) # End
    
    radians = np.arctan2(thirdAngle[1]-secondAngle[1], thirdAngle[0]-secondAngle[0]) - np.arctan2(firstAngle[1]-secondAngle[1], firstAngle[0] - secondAngle[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle 

def get_coordinates(landmarks,type):
    leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    leftHeel = [landmarks[mp_pose.PoseLandmark.LEFT_HELL.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HELL.value].y]
    rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    rightHeel = [landmarks[mp_pose.PoseLandmark.RIGHT_HELL.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HELL.value].y]
    if type == JUMPING_JACKS:
        return leftShoulder,leftElbow,leftWrist,leftHip,leftKnee,leftAnkle,rightShoulder,rightElbow,rightWrist,rightHip,rightKnee,rightAnkle
    elif type == SQUATS:
        return leftWrist,leftElbow,leftShoulder,rightWrist,rightElbow,rightShoulder,leftHip,leftKnee,leftAnkle,rightHip,rightKnee,rightAnkle

def renderText(image,COUNTER,STAGE):
    cv2.rectangle(image, (0, 0),(65,80),(0,0,0), -1)
    cv2.putText(image, str(COUNTER), (12,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,255,0), 2, cv2.LINE_AA)

    cv2.rectangle(image, (500, 0),(800,80),(0,0,0), -1)    
    cv2.putText(image, str(STAGE), (500,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,255,0), 2, cv2.LINE_AA)


