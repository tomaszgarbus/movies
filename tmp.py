import gensim
import csv

from config import PRETRAINED_W2V_PATH, MOVIES_TO_FETCH_PATH
from omdb_download import get_and_cache_movie_json
from visualize_json import VisualizeJson
from wiki_articles_download import tokens_list_to_context_json, download_article_or_load_from_cache, cut_by_citations,\
    tokenize_and_filter_no_alphanumeric
from utils import number_heuristic


def compare_omdb_with_wiki(json_viz: VisualizeJson):
    """ Some experiments with OMDB Api and Wikipedia articles. No interesting results so far. """
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    for row in csv_rows:
        print("Row id: " + str(row[0]))
        omdb_query = row[1]
        pedia_resource = row[2]

        omdb_json = get_and_cache_movie_json(omdb_query)
        wikipedia_text = download_article_or_load_from_cache(pedia_resource)
        wikipedia_text = cut_by_citations(wikipedia_text)
        wikipedia_tokenized = tokenize_and_filter_no_alphanumeric(wikipedia_text)
        # tokens_lim = 1500
        wikipedia_json = tokens_list_to_context_json(wikipedia_tokenized,
                                                     window_size=10,
                                                     include_if=number_heuristic)

        omdb_pairs = json_viz.get_number_context_pairs(omdb_json)
        wiki_pairs = json_viz.get_number_context_pairs(wikipedia_json)
        for (num, convec, conraw) in omdb_pairs:
            closest_wiki = json_viz.k_closest_contexts(convec, wiki_pairs, k=5)
            print(conraw, num)
            print(list(map(lambda a: (a[0], a[2]), closest_wiki)))
            print()

        json_viz.visualize_many([omdb_json, wikipedia_json],
                                show_context=False,
                                limit_per_json=150)


def compare_wiki_articles(json_viz: VisualizeJson):
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    wiki_jsons = []
    all_wiki_pairs = []

    for row in csv_rows:
        print("Row id: " + str(row[0]))
        pedia_resource = row[2]

        wikipedia_text = download_article_or_load_from_cache(pedia_resource)
        wikipedia_text = cut_by_citations(wikipedia_text)
        wikipedia_tokenized = tokenize_and_filter_no_alphanumeric(wikipedia_text)
        wikipedia_json = tokens_list_to_context_json(wikipedia_tokenized,
                                                     window_size=10,
                                                     include_if=number_heuristic)
        wiki_jsons.append(wikipedia_json)
        wiki_pairs = json_viz.get_number_context_pairs(wikipedia_json)
        all_wiki_pairs.append(wiki_pairs)

    json_viz.visualize_many(wiki_jsons, show_context=False)
    for pair in all_wiki_pairs[0]:
        for j in range(1, 6):
            closest_pair = json_viz.k_closest_contexts(pair[1],
                                                       candidates=all_wiki_pairs[j],
                                                       k=1)[0]
            print(pair[0], "::", pair[2])
            print(closest_pair[0], "::", closest_pair[2])
            print()


if __name__ == '__main__':
    model = gensim.models.KeyedVectors.load_word2vec_format(PRETRAINED_W2V_PATH, binary=True)
    print("w2v model loaded successfully")

    json_viz = VisualizeJson(model)
    # compare_omdb_with_wiki()


