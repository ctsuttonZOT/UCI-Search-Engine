from flask import Flask
from flask import request

app = Flask(__name__)

# curl --header "Content-Type: application/json" --request POST --data '{"username":["xyz"]}' http://127.0.0.1:5000

@app.route("/search", methods=['POST'])
def hell_world():

    print(request.get_json(request.get_data())['username'])

    return "<p>Hello, World!</p>"