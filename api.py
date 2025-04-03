from ast import parse
from flask import Flask
from flask import request
from flask_restful import reqparse
from flask_cors import CORS
import scrapper
import json
import checkController

app = Flask(__name__)
CORS(app)
# api = Api(app)


@app.route("/scan", methods=['POST'])
def receive_code():

    data = request.get_json()

    if checkController.insertCheck(1, data['link']):
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success': False}), 500, {'ContentType':'application/json'}

@app.route("/checks/search", methods=['GET'])
def search():

    search = request.args.get("query")
    checks = checkController.searchChecks(1, search)

    if len(checks)>0:
        return json.dumps(checks), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 404, {'ContentType':'application/json'}

@app.route("/checks/userPaid", methods=['PUT'])
def updateUserPaid():

    amount = request.args.get("amount")
    checkID = request.args.get("checkID")

    if checkController.updateUserPaid(1, checkID, amount):
        return json.dumps({}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 500, {'ContentType':'application/json'}

@app.route("/checks/category", methods=['PUT'])
def updateCategory():

    categoryID = request.args.get("categoryID")
    checkID = request.args.get("checkID")

    if checkController.updateCategory(1, checkID, categoryID):
        return json.dumps({}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 500, {'ContentType':'application/json'}

@app.route("/checks/category", methods=['GET'])
def getCheckByCategory():

    categoryID = request.args.get("categoryID")
    checks  = checkController.getChecksByCategory(1, categoryID)

    if len(checks) > 0:
        return json.dumps(checks), 200, {'ContentType':'application/json'}
    else:
        return json.dumps([]), 404, {'ContentType':'application/json'}        

@app.route("/analytics", methods=['GET'])
def get_analytics():

    rangeBegin = request.args.get("begin")
    rangeEnd = request.args.get('end')
    data = checkController.getAnalytics(1, rangeBegin, rangeEnd)

    if len(data)>0:
        return json.dumps(data), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 404, {'ContentType':'application/json'}
    
if __name__ == "__main__":
    app.run(host="192.168.1.4", port="5000", debug=False, threaded = True)
    # app.run()