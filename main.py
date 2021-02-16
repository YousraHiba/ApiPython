from datetime import date, datetime

from bson.json_util import dumps
from json import JSONEncoder
import json

from bson import json_util, ObjectId
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import pymongo


client = pymongo.MongoClient()
mydb = client["homeWorkout"]
userTable = mydb["user"]
workoutsTable = mydb["workouts"]
activityTable = mydb["activity"]
app = Flask(__name__)
app.secret_key = "my_precious"

@app.route('/welcome')
def welcome():
    return({'message':'welcome'})

@app.route('/')
def index():
    return({'message':'welcome'})
    # #for x in mycol.find({"name": {"$eq": "hiba"}}):
    # if request.method == 'GET':
    #     username = request.args.get('username')
    #     print(username)
    #     password = request.args.get('password')
    #     print(password)
    #     res = dumps(userTable.find_one({'name':username ,'password':password }))
    #     return res

@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        username = request.args.get('username')
        print(username)
        password = request.args.get('password')
        print(password)
        res = dumps(userTable.find_one({'userName': username, 'password': password}))
        return res

@app.route('/logout')
def logout():
    #session.pop('logged_in', None)
    #flash("you are logged out")
    return redirect(url_for('welcome'))


####### workouts
@app.route('/register', methods=['POST'])
def registerUser():
    if request.method == 'POST':
        print("registerUser")
        print(request.json)
        user = request.json
        if(user["name"] and user["password"] and user["email"]):
            print(user)
            res = userTable.insert_one(user)
            print(user)
            return ({
                'status': 201,
                'message': user["name"]+' ßuser was registered '
            })
##### activites

## startActivity
@app.route('/startActivity', methods=['POST'])
def startActivity():
    if request.method == 'POST':
        activity = request.json
        if(activity["idWorkout"] and activity["idUser"]):
            print(activity)

            startDate = datetime.now()
            print(startDate)
            activityTosave = {
                "idWorkout" : activity["idWorkout"],
                "idUser": activity["idUser"],
                "startDate": startDate,
                "endDate": ""
            }

            print(activityTosave)
            res = activityTable.insert_one(activityTosave)
            return ({
                'status': 201,
                'message': ' activity was registered '
            })


## endActivity
@app.route('/endActivity', methods=['POST'])
def endActivity():
    if request.method == 'POST':
        activity = request.json
        if(activity["idActivity"]):
            print(activity)
            idActivity = activity["idActivity"]
            print('idActivity'+idActivity)
            endDate = datetime.now()
            print(endDate)
            res = activityTable.find_one({'_id': ObjectId(idActivity)})
            result = activityTable.update_one({"_id": res["_id"]}, {"$set": {"endtDate": endDate}})
            print("raw_result:", result.raw_result)
            activityUpdated = dumps(activityTable.find_one({'_id': ObjectId(idActivity)}))

            # return jsonify(result.raw_result)

            # return activityUpdated

            return ({
                'status': 201,
                'message': ' activity was ended  ',
                'activity':activityUpdated
            })








@app.route('/workouts', methods=['GET'])
def getWorkouts():
    if request.method == 'GET':
        workouts = dumps(workoutsTable.find())
        print(workouts)
        return workouts

if __name__ == '__main__':
    app.run(debug=True)



