from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries, Collection
from colbert import Indexer, Searcher
import os


if __name__=='__main__':
    # collection = os.path.join(dataroot, 'docs_combined.tsv')

    nbits = 2   # encode each dimension with 2 bits
    doc_maxlen = 300   # truncate passages at 300 tokens
    checkpoint = 'downloads/colbertv2.0'


    ###### DOCUMENT-LEVEL INDEX ######

    done = False
    i = 1

    while done == False:

        try:
            collection = Collection(path=f'/home/ttds/TTDS/ColBERT/TSVs/multi_att/partition_{i}.tsv')
            index_name = f'multi_att/partition_{i}_index.{nbits}bits'

            with Run().context(RunConfig(nranks=1, experiment='notebook')):  # nranks specifies the number of GPUs to use.
                config = ColBERTConfig(doc_maxlen=doc_maxlen, nbits=nbits)

                indexer = Indexer(checkpoint=checkpoint, config=config)
                indexer.index(name=index_name, collection=collection, overwrite=True)

            i += 1

        except:
            done = True


    ###### EPISODE-LEVEL INDEX ######

    collection = Collection(path=f'/home/ttds/TTDS/ColBERT/TSVs/multi_att/episodes.tsv')
    index_name = f'multi_att/episodes_index.{nbits}bits'

    with Run().context(RunConfig(nranks=1, experiment='notebook')):  # nranks specifies the number of GPUs to use.
        config = ColBERTConfig(doc_maxlen=doc_maxlen, nbits=nbits)

        indexer = Indexer(checkpoint=checkpoint, config=config)
        indexer.index(name=index_name, collection=collection, overwrite=True)
