import gensim
from omdb_download import get_and_cache_movie_json
from visualize_json import VisualizeJson
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from dbpedia_helper import DBPediaHelper
from wiki_articles_download import download_article, article_text_to_context_json

if __name__ == '__main__':
    helper = DBPediaHelper()
    dbpedia_json = helper.load_resourse_as_flat_json("Star_Wars_(film)")
    print(dbpedia_json)
    omdb_json = get_and_cache_movie_json("Star Wars Episode IV")
    print(omdb_json)
    wikipedia_text = download_article("Star_Wars_(film)")
    print(len(wikipedia_text))

    def number_heur(s: str) -> bool:
        """ True iff |s| should be treated as a number. """
        allowed_chars = '0123456789,.%/$E'
        any_digit = False
        for c in s:
            if c.isdigit():
                any_digit = True
            if c not in allowed_chars:
                return False
        return any_digit
    wikipedia_json = article_text_to_context_json(wikipedia_text[:1000], include_if=number_heur)
    print(wikipedia_json)

    model = gensim.models.KeyedVectors.load_word2vec_format('./data/GoogleNews-vectors-negative300.bin', binary=True)
    json_viz = VisualizeJson(model)
    # json_viz.visualize_many([omdb_json, dbpedia_json, wikipedia_json])
    json_viz.visualize_many([omdb_json, wikipedia_json])
