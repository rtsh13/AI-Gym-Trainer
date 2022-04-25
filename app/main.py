# # common point for every application to run
from flask import Flask, Response, render_template,redirect
import cv2
import mediapipe as mp
drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles

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

@app.route('/')
def index():
    return render_template('videoTemplate.html')

# TODO: Random url generation // avoiding data leakage
@app.route('/pvt')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True) 