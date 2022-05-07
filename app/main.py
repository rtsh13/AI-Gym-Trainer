# # common point for every application to run
from flask import Flask, Response, render_template,redirect
import cv2
import mediapipe as mp
from helpers import *
from constants import *

app = Flask(__name__)

cap = cv2.VideoCapture(0)
res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
pvt = str(res)    

@app.route("/form", methods = ["POST"])
def form():
    sets = request.form("sets")
    reps = request.form("sets")
    equipment = request.form("sets")
    exercise_name = request.form("sets")
    port = request.form("sets")

    return sets,reps,equipment,exercise_name,port

@app.route('/')
def index():
    return render_template('videoTemplate.html')

@app.route('/'+pvt)
def video():
    if exercise_name == BICEP_CURLS:
        return Response(BicepsExercise(),mimetype='multipart/x-mixed-replace; boundary=frame')
    if exercise_name == CONCENTRATION_CURLS:
        return Response(ConCurlsExercise(),mimetype='multipart/x-mixed-replace; boundary=frame')
    if exercise_name == DIAMOND_PUSHUPS || exercise_name == PUSHUPS:
            return Response(PushupsExercise(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__== "__main__":
    app.run(debug=True) 