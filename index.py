from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries, Collection
from colbert import Indexer, Searcher
import os


if __name__=='__main__':

    nbits = 2   # encode each dimension with 2 bits
    doc_maxlen = 300   # truncate passages at 300 tokens
    checkpoint = 'downloads/colbertv2.0'


    ###### DOCUMENT-LEVEL INDEX ######

    for variation in ['concat', 'transcript_and_pub']: # 'transcript_only'

        done = False
        i = 13

        while done == False:

            try:
                collection = Collection(path=f'/home/ttds/TTDS/ColBERT/TSVs/{variation}/partition_{i}.tsv')
                index_name = f'{variation}/partition_{i}_index.{nbits}bits'

                with Run().context(RunConfig(nranks=1, experiment='notebook')):  # nranks specifies the number of GPUs to use.
                    config = ColBERTConfig(doc_maxlen=doc_maxlen, nbits=nbits)

                    indexer = Indexer(checkpoint=checkpoint, config=config)
                    indexer.index(name=index_name, collection=collection, overwrite=True)

                i += 1

            except:
                done = True


    ###### EPISODE-LEVEL INDEX ######

    collection = Collection(path=f'/home/ttds/TTDS/ColBERT/TSVs/episodes.tsv')
    index_name = f'episodes_index.{nbits}bits'

    with Run().context(RunConfig(nranks=1, experiment='notebook')):  # nranks specifies the number of GPUs to use.
        config = ColBERTConfig(doc_maxlen=doc_maxlen, nbits=nbits)

        indexer = Indexer(checkpoint=checkpoint, config=config)
        indexer.index(name=index_name, collection=collection, overwrite=True)
