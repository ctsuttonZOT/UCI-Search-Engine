from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)

# curl --header "Content-Type: application/json" --request POST --data '{"username":["xyz"]}' http://127.0.0.1:5000
# python -m flask --app server run
CORS(app)
@app.route("/search", methods=['POST'])
def hell_world():
    # parse the query
    # call the query search function
    # return results

    print(request.get_json(request.get_data())['username'])

    return "<p>Hello, World!</p>"