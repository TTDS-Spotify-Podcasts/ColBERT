import os
import sys
sys.path.insert(0, '../')

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries, Collection
from colbert import Indexer, Searcher

# dataroot = '.docs/downloads/lotte/'

# queries = os.path.join(dataroot, dataset, datasplit, 'questions.search.tsv')

# queries = Queries(path=queries)

# checkpoint = 'downloads/colbertv2.0'
# index_name = f'{dataset}.2bits'

# f'Loaded {len(queries)} queries and {len(collection):,} passages'


class Searching:
    def __init__(self):
        self.searchers = self.get_searchers()

    def get_searchers(self):
        searchers = []
        done = False
        i = 1
        while done == False:
            try:
                with Run().context(RunConfig(experiment='notebook')):
                    searcher = Searcher(index=f'partition_{i}_index.2bits')
                    searchers.append(searcher)
                i += 1
            except:
                done = True
                
        return searchers



    def _searching(self, query, K):
        
        # get results for each partition's index
        partition_results = []
        for searcher in self.searchers:    
            results = searcher.search(query, k=100)
            ans = []
            # Print out the top-k retrieved passages
            for passage_id, passage_rank, passage_score in zip(*results):
                ans.append({'Passage ID': passage_id, 'Passage rank': passage_rank, 'Score': passage_score, 'Contexts': self.searcher.collection[passage_id]})
            partition_results.append(ans)

            # TODO need to return embeddings

        for 

        return final_results


searcher = Searching()
results = searcher._searching("trump white house", K=3)
for i in results: print(i) 