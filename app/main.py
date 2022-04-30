# common point for every application to run
from flask import Flask, Response, redirect
import cv2
import mediapipe as mp
import numpy as np
import math
drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles
COUNTER = 0
STAGE = None

app = Flask(__name__)


cap = cv2.VideoCapture(0)
def generate_frames():
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.6) as pose:
        while cap.isOpened():
            _, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            detections = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            drawing.draw_landmarks(image, detections.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2), 
                                    drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2))   

            _,buffer=cv2.imencode('.jpg',image)
            x=buffer.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()


@app.route("/about")
def about():
    return redirect("https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask")

@app.route("/video")
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
