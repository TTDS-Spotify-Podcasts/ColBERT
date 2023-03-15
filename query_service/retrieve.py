from flask import Flask, jsonify, request

import sys
sys.path.insert(0, '../')

from searching import Searching

app = Flask(__name__)

cache = {}

@app.route('/', methods=['GET'])
def home():
    
    # initialise doc-level searcher
    if 'searcher_trans_pub' not in cache:
        cache['searcher_trans_pub'] = Searching(index='Doc', variation='transcript_and_pub')
    
    # initialise ep-level searcher
    if 'ep_searcher' not in cache:
        cache['ep_searcher'] = Searching(index='Ep')

    return jsonify({'message': 'ColBERT currently running'})


########## DOC-LEVEL: SYSTEM 2 ##########
# @app.route('/doc_query/transcript_only', methods=['GET'])
# def doc_query_trans_only():
    
#     if 'searcher_trans_only' not in cache:
#         cache['searcher_trans_only'] = Searching(index='Doc', variation='transcript_only')

#     query = request.args.get('searchquery')
#     k = request.args.get('k')
#     if k is None:
#         k = 100
#     return jsonify(cache['searcher_trans_only']._searching(query, k=int(k)))

########## DOC-LEVEL: SYSTEM CONCAT ##########
# @app.route('/doc_query/concat', methods=['GET'])
# def doc_query():
#     if 'searcher' not in cache:
#         cache['searcher'] = Searching(index='Doc', variation='concat')

#     query = request.args.get('searchquery')
#     k = request.args.get('k')
#     if k is None:
#         k = 100
#     return jsonify(cache['searcher']._searching(query, k=int(k)))

########## DOC-LEVEL: SYSTEM 3 ##########
@app.route('/doc_query/transcript_and_pub', methods=['GET'])
def doc_query_trans_pub():

    if 'searcher_trans_pub' not in cache:
        cache['searcher_trans_pub'] = Searching(index='Doc', variation='transcript_and_pub')

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 100
    return jsonify(cache['searcher_trans_pub']._searching(query, k=int(k)))

######### EP-LEVEL #########

@app.route('/ep_query', methods=['GET'])
def ep_query():

    if 'ep_searcher' not in cache:
        cache['ep_searcher'] = Searching(index='Ep')

    query = request.args.get('searchquery')
    k = request.args.get('k')
    if k is None:
        k = 100
    return jsonify(cache['ep_searcher']._searching(query, k=int(k)))


if __name__ == '__main__':
    app.run(debug=True)
