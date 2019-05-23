import csv
from typing import Iterable, List, Tuple, Dict

from nltk import tokenize
from constants import MOVIES_TO_FETCH_PATH
from omdb_download import get_and_cache_movie_json, preprocess_movie_json
from utils import number_heuristic
from visualize_json import VisualizeJson, NumberContext
from wiki_articles_download import tokens_list_to_context_json, download_article_or_load_from_cache, \
    preprocess_wiki_article, tokenize_article_text


def compare_omdb_with_wiki(json_viz: VisualizeJson,
                           wiki_window_sizes: Iterable[int] = tuple(range(1, 11))) -> None:
    """
    Compares OMDb jsons with jsonized Wikipedia articles, using t-SNE visualizations of context embeddings as well as
    finding closest contexts to each number found in |json_viz|.
    The jsonization of Wikipedia article is performed multiple times (ones for each window size).
    Performs the procedure for every movie listed in the csv.

    :param json_viz: An instance of VisualizeJson.
    :param wiki_window_sizes: Radii of context windows for Wikipedia.
    """
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    for row in csv_rows:
        print("Row id: " + str(row[0]))
        omdb_query = row[2]
        pedia_resource = row[3]
        compare_omdb_with_wiki_single_movie(json_viz=json_viz,
                                            omdb_query=omdb_query,
                                            pedia_resource=pedia_resource,
                                            wiki_window_sizes=wiki_window_sizes)


def compare_omdb_with_wiki_single_movie(json_viz: VisualizeJson,
                                        omdb_query: str,
                                        pedia_resource: str,
                                        wiki_window_sizes: Iterable[int] = tuple(list(range(1, 11))))\
        -> List[Tuple[NumberContext, List[Tuple[NumberContext, float]]]]:
    """
    Compares OMDb jsons with jsonized Wikipedia articles, using t-SNE visualizations of context embeddings as well as
    finding the closest contexts to each number found in |json_viz|. Performs this only for one movie.

    :param json_viz: An instance of VisualizeJson.
    :param omdb_query: Phrase to query OMDb API with.
    :param pedia_resource: Exact name of the Wikipedia resource for the movie.
    :param wiki_window_sizes: Radii of context windows for Wikipedia.
    :return: List of pairs (number context, list of closest number contexts with distance).
    """
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

    result = []

    omdb_pairs = json_viz.get_number_context_pairs(omdb_json)
    wiki_pairs = json_viz.get_number_context_pairs(wikipedia_json)
    for (num, convec, conraw) in omdb_pairs:
        closest_wiki = json_viz.k_closest_contexts(convec, wiki_pairs, k=15)
        print("number:", num, "context:", conraw)
        print('\n'.join(list(map(lambda a: str((a[1], a[0][0], a[0][2])), closest_wiki))))
        print()

        result.append(((num, convec, conraw),
                       closest_wiki))

    json_viz.visualize_many([omdb_json, wikipedia_json],
                            show_context=False,
                            limit_per_json=50)
    return result


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


def locate_omdb_values_single_movie(json_viz: VisualizeJson,
                                    omdb_query: str,
                                    pedia_resource: str,
                                    wiki_window_sizes: Iterable[int] = tuple(range(1, 11)))\
        -> List[Tuple[NumberContext, List[NumberContext]]]:
    """
    Iterates through all fields in the OMDb json for the movie and tries to locate the same value in Wikipedia article.
    The algorithm is as follows:
    1) Fetch the movie json from OMDb API (or cache).
    2) Fetch the Wikipedia article and jsonize it.
    3) Transform both resources into lists of (number, context) pairs.
    4) For every field in OMDb json, find k=15 nearest contexts among Wikipedia pairs.
    5) Filter only those pairs, where the embedded number matches.

    :param json_viz: An instance of VisualizeJson object.
    :param omdb_query: A phrase to search in OMDb API to fetch the movie.
    :param pedia_resource: Exact name of Wikipedia resource for this movie.
    :param wiki_window_sizes: Radii of context windows for Wikipedia
    :return: A list of pairs (NumberContext, NumberContext[]), where the first element originates from the OMDb response
             and the second from Wikipedia (all the found matches).
    """
    result = []

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
        closest_wiki: List[NumberContext] = list(filter(lambda a: a[0][0] == num, closest_wiki))
        result.append(((num, convec, conraw),
                       closest_wiki))
    return result


def print_omdb_matched_values_count(matches: List[Tuple[NumberContext, List[NumberContext]]]) -> None:
    """
    Prints, to standard output, the ratio of matched values from OMDb.

    :param matches: Results of `locate_omdb_values_single_movie` call.
    """
    nonempty = sum([1 if l else 0 for _, l in matches])
    print("%d/%d fields matched with Wiki" % (nonempty, len(matches)))


def locate_omdb_values(json_viz: VisualizeJson,
                       wiki_window_sizes: Iterable[int] = tuple(range(1, 11)),
                       show_matches=True,
                       show_match_ratio=False)\
        -> Dict[str, List[Tuple[NumberContext, List[NumberContext]]]]:
    """
    For each movie listed in the csv file at MOVIES_TO_FETCH_PATH (see constants_sip.py), iterates through all fields in
    the OMDb json and tries to locate the same value in a Wikipedia context. Returns the list of results and optionally
    displays results on standard output.

    :param json_viz: An instance of VisualizeJson object.
    :param wiki_window_sizes: Radii of context windows for Wikipedia.
    :param show_matches: Whether to display found pairs.
    :param show_match_ratio: Whether to display ratio of matched fields (against all fields).
    :return: Returns a dictionary of pairs (movie title, list of matches for movie). For the description of the value
             element refer to `locate_omdb_values_single_movie`.
    """
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    matches = {}
    for row in csv_rows:
        print("Processing movie: " + row[1])
        omdb_query = row[2]
        pedia_resource = row[3]

        matches[row[1]] = locate_omdb_values_single_movie(json_viz=json_viz,
                                                          omdb_query=omdb_query,
                                                          pedia_resource=pedia_resource,
                                                          wiki_window_sizes=wiki_window_sizes)

    if show_matches:
        for row in csv_rows:
            print("Movie: " + row[1])
            for ((num, convec, conraw), closest_wiki) in matches[row[1]]:
                print("number:", num, "context:", conraw)
                print("Wikipedia context candidates:")
                if closest_wiki:
                    print('\n'.join(list(map(lambda a: str((a[1], a[0][0], a[0][2])), closest_wiki))))
                    print()
                else:
                    print("None found")
                    print()
    if show_match_ratio:
        for row in csv_rows:
            print("Movie: " + row[1])
            print_omdb_matched_values_count(matches[row[1]])

    return matches


def find_k_closest_question_answers(json_viz: VisualizeJson,
                                    question: str,
                                    candidates: List[NumberContext],
                                    k: int = 15
                                    ) -> List[Tuple[NumberContext, float]]:
    """
    Given a question as a string and a list of answer candidates, returns |k| closest candidates based on embeddings
    cosine similarity.

    :param json_viz: An instance of VisualizeJson.
    :param question: A question, given as a raw string.
    :param candidates: A list of candidate NumberContext pairs.
    :param k: Number of values to return.
    :return:
    """
    question_words = tokenize.word_tokenize(question)
    question_vec = json_viz.model.vectorize_context(question_words)
    return json_viz.k_closest_contexts(question_vec, candidates=candidates, k=k)


def pedia_resource_to_wiki_pairs(json_viz: VisualizeJson,
                                 pedia_resource: str,
                                 wiki_window_sizes: Iterable[int] = tuple(range(1, 11))) -> List[NumberContext]:
    """
    Given a Wikipedia resource name, produces NumberContext pairs for the article.

    :param json_viz: An instance of VisualizeJson.
    :param pedia_resource: Resource name.
    :param wiki_window_sizes: Radii of context windows for Wikipedia.
    :return: List of NumberContext pairs.
    """
    wikipedia_text = download_article_or_load_from_cache(pedia_resource)
    wikipedia_text = preprocess_wiki_article(wikipedia_text)
    wikipedia_tokenized = tokenize_article_text(wikipedia_text)
    wikipedia_json = {}
    for window_size in wiki_window_sizes:
        tmp_wiki_json = tokens_list_to_context_json(wikipedia_tokenized,
                                                    window_size=window_size,
                                                    include_if=number_heuristic)
        wikipedia_json = {**wikipedia_json, **tmp_wiki_json}

    wiki_pairs = json_viz.get_number_context_pairs(wikipedia_json)
    return wiki_pairs


def interactive_question_answering(json_viz: VisualizeJson,
                                   wiki_window_sizes: Iterable[int] = tuple(range(1, 11))) -> None:
    """
    Asks the user for the movie title, then in a loop, user asks questions. In return they get, for each question, 15
    closest answers.

    :param json_viz: An instance of VisualizeJson.
    :param wiki_window_sizes: Radii of context windows for Wikipedia.
    """
    with open(MOVIES_TO_FETCH_PATH, 'r') as movies_csv:
        reader = csv.reader(movies_csv, delimiter=',', )
        csv_rows = [row for row in reader][1:]

    def movie_exists(title: str, csv_rows: List[List[str]]) -> bool:
        for row in csv_rows:
            if row[1] == title:
                return True
        return False

    print("Provide movie title")
    title = input().strip()
    while not movie_exists(title, csv_rows):
        print("Invalid title, try again")
        title = input().strip()

    for row in csv_rows:
        if row[1] == title:
            pedia_resource = row[3]

    print("Vectorizing document...")
    wiki_pairs = pedia_resource_to_wiki_pairs(json_viz, pedia_resource, wiki_window_sizes)

    while True:
        print("Ask a question:")
        question = input().strip()
        answer_candidates = find_k_closest_question_answers(json_viz=json_viz, question=question, candidates=wiki_pairs)
        for cand in answer_candidates:
            print(cand[1], cand[0][0], cand[0][2])
