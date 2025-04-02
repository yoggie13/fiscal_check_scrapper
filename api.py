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
def receive_search():
    search = request.args.get("query")
    if checkController.returnCheck(1, search):
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success': False}), 500, {'ContentType':'application/json'}
if __name__ == "__main__":
    # app.run(host="192.168.1.4", port="5000", debug=False, threaded = True)
    app.run()