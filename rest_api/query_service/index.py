from flask import Flask, jsonify, request

import sys
sys.path.insert(0, '../')

from searching import Searching

app = Flask(__name__)

cache = {}
@app.route('/', methods=['GET'])
def home():
    cache['searcher'] = Searching()

    return jsonify({'message': 'Hello, World!'})

@app.route('/query', methods=['GET'])
def query():
    word = request.args.get('word')
    return jsonify(cache['searcher']._searching(word))

# @app.route('/user', methods=['POST'])
# def add_user():
#     data = request.get_json()
#     return jsonify({'username': data['username']})

if __name__ == '__main__':
    app.run(debug=True)
