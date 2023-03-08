from flask import Flask, jsonify, request

import sys
sys.path.insert(0, '../')

from searching import Searching

app = Flask(__name__)

cache = {}
@app.route('/', methods=['GET'])
def home():
    if 'searcher' not in cache:
        cache['searcher'] = Searching()

    return jsonify({'message': 'ColBERT currently running'})


@app.route('/doc_query', methods=['GET'])
def query():
    if 'searcher' not in cache:
        cache['searcher'] = Searching()

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 100
    return jsonify(cache['searcher']._searching(query, index='doc', k=int(k)))


@app.route('/ep_query', methods=['GET'])
def query():
    if 'searcher' not in cache:
        cache['searcher'] = Searching()

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 100
    return jsonify(cache['searcher']._searching(query, index='ep', k=int(k)))


if __name__ == '__main__':
    app.run(debug=True)