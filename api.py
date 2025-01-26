from ast import parse
from flask import Flask
from flask import request
from flask_restful import reqparse
from flask_cors import CORS
import scrapper
import json

app = Flask(__name__)
CORS(app)
# api = Api(app)


@app.route("/scan", methods=['POST'])
def receive_code():
    data = request.get_json()
    print(data)
    scrapper.scrape_web_page(data["link"])

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == "__main__":
    app.run(host="192.168.1.4", port="5000", debug=False, threaded = True)