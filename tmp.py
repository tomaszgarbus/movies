import csv
from typing import Iterable

from constants import MOVIES_TO_FETCH_PATH
from omdb_download import get_and_cache_movie_json, preprocess_movie_json
from utils import number_heuristic
from visualize_json import VisualizeJson
from wiki_articles_download import tokens_list_to_context_json, download_article_or_load_from_cache, \
    preprocess_wiki_article, tokenize_article_text
from word_vectors_model.bert_pretrained import BertPretrained


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
        omdb_query = row[2]
        pedia_resource = row[3]

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


def compare_omdb_with_wiki_multi_window_sizes(json_viz: VisualizeJson,
                                              wiki_window_sizes: Iterable[int] = tuple(range(1, 11))) -> None:
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
        omdb_query = row[2]
        pedia_resource = row[3]

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
        pedia_resource = row[3]

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


def locate_omdb_values(json_viz: VisualizeJson,
                       wiki_window_sizes: Iterable[int] = tuple(range(1, 11))) -> None:
    """
    For each movie listed in the csv file at MOVIES_TO_FETCH_PATH (see constants.py), iterates through all fields in
    the OMDb json an tries to locate the same value in a Wikipedia context. Displays results on standard output.

    :param json_viz: An instance of VisualizeJson object.
    :param wiki_window_sizes: Radiuses of context windows for Wikipedia.
    """
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    for row in csv_rows:
        print("Processing movie: " + row[1])
        omdb_query = row[2]
        pedia_resource = row[3]

        omdb_json = preprocess_movie_json(get_and_cache_movie_json(omdb_query))
        wikipedia_text = download_article_or_load_from_cache(pedia_resource)
        wikipedia_text = preprocess_wiki_article(wikipedia_text)
        wikipedia_tokenized = tokenize_article_text(wikipedia_text)
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
            print("Wikipedia context candidates:")
            closest_wiki = list(filter(lambda a: a[0][0] == num, closest_wiki))
            if closest_wiki:
                print('\n'.join(list(map(lambda a: str((a[1], a[0][0], a[0][2])), closest_wiki))))
            else:
                print("None found")
            print()


if __name__ == '__main__':
    # model = gensim.models.KeyedVectors.load_word2vec_format(PRETRAINED_W2V_PATH, binary=True)
    # print("w2v model loaded successfully")

    model = BertPretrained()
    json_vis = VisualizeJson(model)
    # compare_omdb_with_wiki()


