import os
import sys
sys.path.insert(0, '../')

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries, Collection
from colbert import Indexer, Searcher

import numpy as np


class Searching:
    
    def __init__(self):
        self.searchers = self.get_searchers()

    # Gets the corresponding Searcher for each partition index
    def get_searchers(self):
        searchers = []
        done = False
        i = 1
        while done == False:
            try:
                with Run().context(RunConfig(experiment='notebook')):
                    searcher = Searcher(index=f'transcript_only/partition_{i}_index.2bits')
                    searchers.append(searcher)
                i += 1
            except:
                done = True
        # return list of Searchers
        return searchers


    def _searching(self, query, K):
        # Get top 100 results for each partition's index and save them to a list
        colbert_results = []
        for searcher in self.searchers:    
            results = searcher.search(query, k=100) # NOTE we can change from 100 if needed..
            for passage_id, passage_rank, passage_score in zip(*results):
                
                # simple fix for header row issue # TODO: better solution that doesn't reduce k to 99?
                if passage_id == 0: continue  
                
                colbert_results.append({
                    'Doc ID': searcher.collection.item_ids[passage_id] 
                    'score': passage_score,  
                    })


        # return top K by score
        return sorted(colbert_results, key=lambda x: x['score'], reverse=True)[:K]

        '''
        Perform re-ranking using cosine similarity between query and results from previous step
        '''

        # Get query embedding 
        # NOTE encode() method is found in Searcher class, so we just use first of self.searchers
        # Q_emb = self.searchers[0].encode(query) # TODO this doesn't work, it's a tensor!!
        # # print(Q_emb.shape)

        # # calculate cosine similarity between query and all results
        # reranking_results = []
        # for p in colbert_results:
        #     p_emb = passage['Embedding']
        #     cos_sim = np.dot(Q_emb, p_emb) / (np.linalg.norm(Q_emb) * np.linalg.norm(p_emb))
        #     p['Cosine'] = cos_sim
        #     reranking_results.append(p)

        # # order results by cosine similarity (descending)
        # reranking_results = sorted(reranking_results, key=lambda x: x['Cosine'], reverse=True)

        # # return top K results
        # return reranking_results[:K]


# TESTING ---------------------------------------
searcher = Searching()

import time

t0 = time.time()

results = searcher._searching("trump", K=5)
for res in results: 
    print(res)
    print()

t1 = time.time()

print("Time: ", t1 - t0)