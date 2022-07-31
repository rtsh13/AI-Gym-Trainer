from flask import Flask, Response, redirect, render_template,jsonify,request 
from flask_cors import CORS 
from arms.bicepCurls import Biceps
from arms.concentrationCurls import ConcentrationCurls
from arms.pushups import DiamondPushUps
from legs.jumpingJacks import JumpingJacks
from legs.lunges import Lunges
from legs.squats import Squats
from utils.constants import BARBELL, DUMBBELL
import cv2


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

cap = cv2.VideoCapture(0)

userData=[]
@app.route('/sendData',methods=['POST'])
def sendData():
    data=request.json
    global userData
    userData.append(data)
    print(userData)
    return jsonify("Data recieved")

@app.route('/biceps')
def bicepTemplate():
    return render_template('biceps.html')

@app.route('/pvt1')
def bicepsVidBox():
    return Response(Biceps(3, 1, DUMBBELL), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cc')
def concTemplate():
    return render_template('conc-curl.html')

@app.route('/pvt2')
def concCurlsVidBox():
    return Response(ConcentrationCurls(3,1,DUMBBELL), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/diamondPushups')
def dpushUpTemplate():
    return render_template('dp.html')

@app.route('/pvt3')
def dpushupsVidBox():
    return Response(DiamondPushUps(3,1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/jumpingJacks')
def jJacksTemplate():
    return render_template('jumping-jacks.html')

@app.route('/pvt4')
def jJacksVidBox():
    return Response(JumpingJacks(10,1), mimetype='multipart/x-mixed-replace; boundary=frame')

# TODO: #Fix it
# @app.route('/lunges')
# def lungesTemplate():
#     return render_template('lunges.html')

# @app.route('/pvt5')
# def lungesVidBox():
#     return Response(Lunges(5,1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/squats')
def squatsTemplate():
    return render_template('squats.html')

@app.route('/pvt6')
def squatsVidBox():
    return Response(Squats(3,1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sideLegLifts')
def sideLegLifts():
    return render_template('side-leg-lifts.html')

@app.route('/pvt7')
def sideLegLiftsTemplate():
    return Response(sideLegLifts(int(userData[0]['reps']),int(userData[0]['sets'])), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug=True) 