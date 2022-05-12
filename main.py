import time
import cv2
from flask import Flask, Response, redirect, render_template
from arms.bicepCurls import Biceps
from arms.concentrationCurls import ConcentrationCurls
from arms.pushups import DiamondPushUps
from legs.jumpingJacks import JumpingJacks
from legs.lunges import Lunges
from legs.squats import Squats
from utils.constants import BARBELL

app = Flask(__name__)

"""
NOTE : This needs to be allocated via input form result
"""

cap = cv2.VideoCapture(0)

"""
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
"""

@app.route('/')
def index():
    return redirect("landing page", code = 302)

@app.route('/result', methods=['POST'])
def result():
    time.sleep(5) 
    return render_template('registrationForm.html')

@app.route('/biceps')
def bicepTemplate():
    return render_template('biceps.html')

@app.route('/pvt')
def bicepsVidBox():
    return Response(Biceps(reps = 5, sets = 1, equipment = BARBELL), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/concentrationCurls')
def concTemplate():
    return render_template('conc-curl.html')

@app.route('/pvt')
def concCurlsVidBox():
    return Response(ConcentrationCurls(reps = 5, sets = 1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/diamondPushups')
def dpushUpTemplate():
    return render_template('dp.html')

@app.route('/pvt')
def dpushupsVidBox():
    return Response(DiamondPushUps(reps = 5, sets = 1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/jumpingJacks')
def jJacksTemplate():
    return render_template('jumping-jacks.html')

@app.route('/pvt')
def jJacksVidBox():
    return Response(JumpingJacks(reps = 5, sets = 1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/lunges')
def lungesTemplate():
    return render_template('lunges.html')

@app.route('/pvt')
def lungesVidBox():
    return Response(Lunges(reps = 5, sets = 1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/squats')
def squatsTemplate():
    return render_template('squats.html')

@app.route('/pvt')
def squatsVidBox():
    return Response(Squats(reps = 5, sets = 1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sideLegLifts')
def sideLegLifts():
    return render_template('side-leg-lifts.html')

@app.route('/pvt')
def sideLegLiftsTemplate():
    return Response(JumpingJacks(reps = 5, sets = 1), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug=True) 