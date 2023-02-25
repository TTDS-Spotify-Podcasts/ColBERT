from flask import Flask, jsonify, request

import sys
sys.path.insert(0, '../')

from searching import Searching

app = Flask(__name__)

cache = {}
@app.route('/', methods=['GET'])
def home():
    cache['searcher'] = Searching()

    return jsonify({'message': 'ColBERT currently running'})

@app.route('/query', methods=['GET'])
def query():
    if 'searcher' not in cache:
        cache['searcher'] = Searching()

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 1000
    return jsonify(cache['searcher']._searching(query, K=int(k)))

if __name__ == '__main__':
    app.run(debug=True)