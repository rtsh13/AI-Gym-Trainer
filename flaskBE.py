from flask import Flask,jsonify,request 
from flask_cors import CORS 
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

userData=[]

@app.route('/sendData',methods=['POST'])
def sendData():
    data=request.json
    print(data)
    userData.append(data)
    return jsonify("Data recieved")




if __name__ == '__main__':
    app.run(debug=True)