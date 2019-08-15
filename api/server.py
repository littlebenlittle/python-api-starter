
from config import *
from flask import Flask, request

app = Flask(__name__)


@app.route('/ping', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print('received a get request')
    else:
        print(request.json())
    return b'success', 200
