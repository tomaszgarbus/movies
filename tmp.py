import gensim
from omdb_download import get_and_cache_movie_json
from visualize_json import VisualizeJson
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from dbpedia_helper import DBPediaHelper

if __name__ == '__main__':
    helper = DBPediaHelper()
    dbpedia_json = helper.load_resourse_as_flat_json("Star_Wars_(film)")
    print(dbpedia_json)
    omdb_json = get_and_cache_movie_json("Star Wars Episode V")
    print(omdb_json)

    model = gensim.models.KeyedVectors.load_word2vec_format('./data/GoogleNews-vectors-negative300.bin', binary=True)
    json_viz = VisualizeJson(model)
    json_viz.visualize_many([omdb_json, dbpedia_json])
