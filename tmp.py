import gensim
import csv
from typing import List

from config import PRETRAINED_W2V_PATH, MOVIES_TO_FETCH_PATH
from omdb_download import get_and_cache_movie_json, preprocess_movie_json
from visualize_json import VisualizeJson
from wiki_articles_download import tokens_list_to_context_json, download_article_or_load_from_cache,\
    preprocess_wiki_article, tokenize_article_text
from utils import number_heuristic


def compare_omdb_with_wiki(json_viz: VisualizeJson, wiki_window_size=10) -> None:
    """
    Compares OMDb jsons with jsonized Wikipedia articles, using t-SNE visualizations of context embeddings as well as
    finding closest contexts to each number found in |json_viz|.

    :param json_viz: An instance of VisualizeJson.
    :param wiki_window_size: Radius of a context window for Wikipedia.  # TODO: rename variable to wiki_window_radius
    """
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    for row in csv_rows:
        print("Row id: " + str(row[0]))
        omdb_query = row[1]
        pedia_resource = row[2]

        omdb_json = preprocess_movie_json(get_and_cache_movie_json(omdb_query))
        wikipedia_text = download_article_or_load_from_cache(pedia_resource)
        wikipedia_text = preprocess_wiki_article(wikipedia_text)
        wikipedia_tokenized = tokenize_article_text(wikipedia_text)
        # tokens_lim = 1500
        wikipedia_json = tokens_list_to_context_json(wikipedia_tokenized,
                                                     window_size=wiki_window_size,
                                                     include_if=number_heuristic)

        omdb_pairs = json_viz.get_number_context_pairs(omdb_json)
        wiki_pairs = json_viz.get_number_context_pairs(wikipedia_json)
        for (num, convec, conraw) in omdb_pairs:
            closest_wiki = json_viz.k_closest_contexts(convec, wiki_pairs, k=15)
            print("number:", num, "context:", conraw)
            print('\n'.join(list(map(lambda a: str((a[1], a[0][0], a[0][2])), closest_wiki))))
            print()

        json_viz.visualize_many([omdb_json, wikipedia_json],
                                show_context=False,
                                limit_per_json=50)


def compare_omdb_with_wiki_multi_window_sizes(json_viz: VisualizeJson,  # TODO: make the default argument immutable
                                              wiki_window_sizes: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) -> None:
    """
    Compares OMDb jsons with jsonized Wikipedia articles, using t-SNE visualizations of context embeddings as well as
    finding closest contexts to each number found in |json_viz|.
    The jsonization of Wikipedia article is performed multiple times (ones for each window size).

    :param json_viz: An instance of VisualizeJson.
    :param wiki_window_sizes: Radiuses of context windows for Wikipedia.
    """
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    for row in csv_rows:
        print("Row id: " + str(row[0]))
        omdb_query = row[1]
        pedia_resource = row[2]

        omdb_json = preprocess_movie_json(get_and_cache_movie_json(omdb_query))
        wikipedia_text = download_article_or_load_from_cache(pedia_resource)
        wikipedia_text = preprocess_wiki_article(wikipedia_text)
        wikipedia_tokenized = tokenize_article_text(wikipedia_text)
        # tokens_lim = 1500
        wikipedia_json = {}
        for window_size in wiki_window_sizes:
            tmp_wiki_json = tokens_list_to_context_json(wikipedia_tokenized,
                                                        window_size=window_size,
                                                        include_if=number_heuristic)
            wikipedia_json = {**wikipedia_json, **tmp_wiki_json}

        omdb_pairs = json_viz.get_number_context_pairs(omdb_json)
        wiki_pairs = json_viz.get_number_context_pairs(wikipedia_json)
        for (num, convec, conraw) in omdb_pairs:
            closest_wiki = json_viz.k_closest_contexts(convec, wiki_pairs, k=15)
            print("number:", num, "context:", conraw)
            print('\n'.join(list(map(lambda a: str((a[1], a[0][0], a[0][2])), closest_wiki))))
            print()

        json_viz.visualize_many([omdb_json, wikipedia_json],
                                show_context=False,
                                limit_per_json=50)


def compare_wiki_articles(json_viz: VisualizeJson, wiki_window_size=10) -> None:
    """
    Visualizes together numeric values from multiple articles from Wikipedia. For each value from the first article,
    shows the closest contexts from all other articles.

    :param json_viz: An instance of VisualizeJson.
    :param wiki_window_size: Radius of the context window used when jsonizing Wikipedia articles.
    """
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    wiki_jsons = []
    all_wiki_pairs = []

    for row in csv_rows:
        print("Row id: " + str(row[0]))
        pedia_resource = row[2]

        wikipedia_text = download_article_or_load_from_cache(pedia_resource)
        wikipedia_text = preprocess_wiki_article(wikipedia_text)
        wikipedia_tokenized = tokenize_article_text(wikipedia_text)
        wikipedia_json = tokens_list_to_context_json(wikipedia_tokenized,
                                                     window_size=wiki_window_size,
                                                     include_if=number_heuristic)
        wiki_jsons.append(wikipedia_json)
        wiki_pairs = json_viz.get_number_context_pairs(wikipedia_json)
        all_wiki_pairs.append(wiki_pairs)

    json_viz.visualize_many(wiki_jsons, show_context=False)

    for pair in all_wiki_pairs[0]:
        print(pair[0], "::", pair[2])
        for j in range(1, 6):
            closest_pair = json_viz.k_closest_contexts(pair[1],
                                                       candidates=all_wiki_pairs[j],
                                                       k=1)[0]
            print(closest_pair[1], "::", closest_pair[0][0], "::", closest_pair[0][2])
        print()


if __name__ == '__main__':
    model = gensim.models.KeyedVectors.load_word2vec_format(PRETRAINED_W2V_PATH, binary=True)
    print("w2v model loaded successfully")

    json_viz = VisualizeJson(model)
    # compare_omdb_with_wiki()


