from ast import parse
from flask import Flask
from flask import request
from flask_restful import reqparse
from flask_cors import CORS
import scrapper
import json
import checkController
import pprint
import userController


app = Flask(__name__)
CORS(app)
# api = Api(app)

@app.route("/auth", methods=["POST"])
def login_user():
    data = request.get_json()
    userData = userController.loginUser(data)
    if userData != {}:
        return json.dumps(userData, ensure_ascii=False).encode('utf8'), 200, {'ContentType':'application/json'}
    else: 
        return json.dumps({}), 500, {'ContentType':'application/json'}

@app.route("/scan", methods=['POST'])
def receive_code():

    data = request.get_json()

    if checkController.insertCheck(1, data['link'], 2, False):
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success': False}), 500, {'ContentType':'application/json'}

@app.route("/checks/<user_id>/search", methods=['GET'])
def search(user_id):

    search = request.args.get("query")
    checks = checkController.searchChecks(user_id, search)

    if len(checks)>0:
        return json.dumps(checks), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 404, {'ContentType':'application/json'}

@app.route("/checks/<check_id>", methods=['GET'])
def getCheck(check_id):
    data = checkController.getCheck(check_id)
    if data:
        return json.dumps(data, ensure_ascii=False).encode('utf8'), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 404, {'ContentType':'application/json'}

@app.route("/checks/recent/<user_id>", methods=['GET'])
def getRecentChecks(user_id):
    data = checkController.getRecentChecks(user_id)
    if data:
        return json.dumps(data, ensure_ascii=False).encode('utf8'), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 404, {'ContentType':'application/json'}

@app.route("/checks/all/<user_id>", methods=['GET'])
def getAllChecks(user_id):
    data = checkController.getChecks(user_id)
    if data:
        return json.dumps(data, ensure_ascii=False).encode('utf8'), 200, {'ContentType':'application/json'}
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

@app.route("/checks/<check_id>/<user_id>/categories", methods=['PUT'])
def updateCategory(check_id, user_id):

    categoryID = request.args.get("category")

    if checkController.updateCategory(user_id, check_id, categoryID):
        return json.dumps({}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 500, {'ContentType':'application/json'}
    
@app.route("/checks/<check_id>/<user_id>/favorite", methods=['PUT'])
def updateFavorite(check_id, user_id):

    value = request.args.get("value")

    if checkController.updateFavorite(user_id, check_id, value):
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

@app.route("/categories", methods=['GET'])
def getCategories():

    categories = checkController.getCategories()

    if len(categories) > 0:
        return json.dumps(categories), 200, {'ContentType':'application/json'}
    else:
        return json.dumps([]), 404, {'ContentType':'application/json'}        


@app.route("/<user_id>/analytics", methods=['GET'])
def get_analytics(user_id):

    rangeBegin = request.args.get("begin")
    rangeEnd = request.args.get('end')
    data = checkController.getAnalytics(user_id, rangeBegin, rangeEnd)

    if len(data)>0:
        return json.dumps(data, ensure_ascii=False).encode('utf8'), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 404, {'ContentType':'application/json'}
    
@app.route("/checks/<check_id>/<user_id>", methods=['DELETE'])
def deleteACheck(check_id, user_id):

    if checkController.deleteACheck(user_id, check_id):
        return json.dumps({}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({}), 500, {'ContentType':'application/json'}
    
if __name__ == "__main__":
    app.run(host="192.168.1.6", port="5000", debug=False, threaded = True)
    # app.run()