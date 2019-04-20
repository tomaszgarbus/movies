import gensim

from dbpedia_helper import DBPediaHelper
from omdb_download import get_and_cache_movie_json
from visualize_json import VisualizeJson
from wiki_articles_download import tokens_list_to_context_json, tokenize_article_text, filter_no_letter_or_digit,\
    download_article_or_load_from_cache, cut_by_citations, number_heuristic
from config import PRETRAINED_W2V_PATH

if __name__ == '__main__':
    model = gensim.models.KeyedVectors.load_word2vec_format(PRETRAINED_W2V_PATH, binary=True)
    json_viz = VisualizeJson(model)

    helper = DBPediaHelper()
    dbpedia_json = helper.load_resourse_as_flat_json("Star_Wars_(film)")
    print(dbpedia_json)
    omdb_json = get_and_cache_movie_json("Star Wars Episode IV")
    print(omdb_json)
    wikipedia_text = download_article_or_load_from_cache("Star_Wars_(film)")
    wikipedia_text = cut_by_citations(wikipedia_text)
    print(len(wikipedia_text))

    wikipedia_tokenized = filter_no_letter_or_digit(tokenize_article_text(wikipedia_text))
    print(len(wikipedia_tokenized))
    wikipedia_json = tokens_list_to_context_json(wikipedia_tokenized, include_if=number_heuristic)
    print(wikipedia_json)


    # json_viz.visualize_many([omdb_json, dbpedia_json, wikipedia_json])
    json_viz.visualize_many([omdb_json, wikipedia_json], show_context=False)
