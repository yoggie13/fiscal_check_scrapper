from ast import parse
from flask import Flask
from flask_restful import reqparse
from flask_cors import CORS
import pandas as pd
import scrapper

app = Flask(__name__)
CORS(app)
# api = Api(app)


@app.route("/scan", methods=['POST'])
def receive_code():
    parser = reqparse.RequestParser()
    parser.add_argument('link', required=True, location='args')
    scrapper.scrape_web_page(args['link'])
