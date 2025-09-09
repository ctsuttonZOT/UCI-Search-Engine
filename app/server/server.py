from flask import Flask
from flask import request
from flask_cors import CORS

import sys
sys.path.append("../../")
import querySearch

app = Flask(__name__)

# curl --header "Content-Type: application/json" --request POST --data '{"username":["xyz"]}' http://127.0.0.1:5000
# python -m flask --app server run
CORS(app)
@app.route("/search", methods=['POST'])
def main():
    query = request.get_json()
    return querySearch.server_main(query["username"].split())