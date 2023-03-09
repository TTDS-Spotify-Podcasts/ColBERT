from flask import Flask, jsonify, request

import sys
sys.path.insert(0, '../')

from searching import Searching

app = Flask(__name__)

cache = {}

# NOTE: uncomment when eval done
# @app.route('/', methods=['GET'])
# def home():
#     if 'searcher' not in cache:
#         cache['searcher'] = Searching()
#     return jsonify({'message': 'ColBERT currently running'})

######### DOC-LEVEL #########

@app.route('/doc_query/transcript_only', methods=['GET'])
def doc_query():
    if 'searcher' not in cache:
        cache['searcher'] = Searching(index='Doc', variation='transcript_only')

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 100
    return jsonify(cache['searcher']._searching(query, k=int(k)))


@app.route('/doc_query/concat', methods=['GET'])
def doc_query():
    if 'searcher' not in cache:
        cache['searcher'] = Searching(index='Doc', variation='concat')

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 100
    return jsonify(cache['searcher']._searching(query, k=int(k)))


@app.route('/doc_query/transcript_and_pub', methods=['GET'])
def doc_query():
    if 'searcher' not in cache:
        cache['searcher'] = Searching(index='Doc', variation='transcript_and_pub')

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 100
    return jsonify(cache['searcher']._searching(query, k=int(k)))

######### EP-LEVEL #########

@app.route('/ep_query', methods=['GET'])
def ep_query():
    if 'searcher' not in cache:
        cache['searcher'] = Searching(index='Ep')

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 100
    return jsonify(cache['searcher']._searching(query, k=int(k)))


if __name__ == '__main__':
    app.run(debug=True)
