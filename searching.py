import os
import sys
sys.path.insert(0, '../')

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries, Collection
from colbert import Indexer, Searcher

import numpy as np


class Searching:
    
    def __init__(self, index, variation=None):
        self.index = index # Doc or Ep
        self.variation = variation # transcript_only, concat, or transcript_and_pub
        if index == 'Doc': self.searchers = self.get_doc_searchers()
        if index == 'Ep': self.searchers = self.get_ep_searcher()


    # Get Searchers for each partition index
    def get_doc_searchers(self):
        searchers = []

        variation_dir = f"experiments/notebook/indexes/{self.variation}"
        for part_index in os.listdir(variation_dir):
                index = os.path.join(self.variation, part_index)
                with Run().context(RunConfig(experiment='notebook')):
                    # iterate over files in variation directory
                        print(1, self.variation, part_index)
                        searcher = Searcher(index=index)
                        searchers.append(searcher)

        # return list of Searchers
        return searchers

    # Get Searcher for episodes index
    def get_ep_searcher(self):
        with Run().context(RunConfig(experiment='notebook')):
            searcher = Searcher(index=f'episodes_index.2bits')
        # return as a list for the _searching method below
        return [searcher] 


    # Perform search over index of the specified searchers
    def _searching(self, query, k):
        '''
        query   query text
        k       number of results for each Searcher 

        @return: sorted list of results
        '''

        results = []

        for searcher in self.searchers:
            colbert_results = searcher.search(query, k=k)
            for passage_id, passage_rank, passage_score in zip(*colbert_results):
                
                # simple fix for header row issue
                if passage_id == 0: continue  
                
                results.append({
                    f'{self.index} ID': searcher.collection.item_ids[passage_id], # item_ids can mean doc_ids or ep_ids (needed a name to generalise)
                    'context': searcher.collection.data[passage_id],
                    'score': passage_score, 
                    })
        
        return sorted(results, key=lambda x: x['score'], reverse=True)


# TESTING ---------------------

# import time

# q = "Donald trump china trade war"

# searcher = Searching('Doc', 'transcript_only')

# start_time = time.time()

# results = searcher._searching(q, 10)[:10]

# for res in results:
#     print(res)
#     print("")

# print(f"TOTAL RESULTS: {len(results)}")

# end_time = time.time()
# print(f"QUERY TIME: {end_time - start_time}")