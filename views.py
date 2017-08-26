from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    pass


@app.route('/notes', methods=['POST'])
def add_note():
    pass


@app.route('/notes/<str:hash>', methods=['GET'])
def get_note(hash):
    pass