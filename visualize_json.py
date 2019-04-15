"""
A temporary class for visualizing Jsons with matplotlib.
First we create a list of (number, context) pairs, where context is vectorized, then use t-SNE to visualize it on a 2D
plane.
"""
from typing import List, Tuple, Dict, Optional
import numpy as np
import gensim
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import re


def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


class VisualizeJson:
    def __init__(self, w2v_model: gensim.models.KeyedVectors):
        self.w2v_model = w2v_model

    def safe_get_vector(self, word: str) -> Optional[np.ndarray]:
        """
        Returns the word vector for |word| or None if the word is not in vocabulary of the w2v model.

        :param word: word.
        :return: Embedding or None.
        """
        try:
            return self.w2v_model.get_vector(word)
        except KeyError:
            return None

    def mean_of_words(self, words: List[np.ndarray]):
        # TODO: weighted mean
        return np.mean(words, axis=0)

    def get_number_context_pairs(self, json_in: Dict, parent_keys: List[str] = [])\
            -> List[Tuple[str, np.ndarray, str]]:
        """
        Transforms a json into a list of pairs (number, vectorized context, raw context).
        TODO: handle KeyError (no such word in vocabulary)

        :param json_in: A dictionary created from an input json.
        :param parent_keys: Keys passed down from higher levels of json.
        :return: List of pairs (number, vectorized context, raw context).
        """
        ret = []
        for key in json_in:
            # Splits the key into multiple words if it is provided as a camelCase.
            key_camel_split = camel_case_split(key)
            # Further splits the key string at each space.
            key_split = ' '.join(key_camel_split).split(' ')
            # Joins the |parent_keys| with the strings obtained by splitting the current key.
            parent_keys_ext = parent_keys + key_split
            # Joins all strings in |parent_keys_ext| into a string.
            parent_keys_str = ' '.join(parent_keys_ext)
            # Vectorizes |parent_keys_ext|.
            parent_keys_vec = list(filter(lambda a: a is not None, map(self.safe_get_vector, parent_keys_ext)))
            if isinstance(json_in[key], dict):
                # If the value is a dictionary, we recursively extract pairs from it.
                ret += self.get_number_context_pairs(json_in[key], parent_keys_ext)
            if isinstance(json_in[key], list):
                # If the value is a list, we iterate it. Since the list can contain either primitive values or objects,
                # the unified solution is to call this method recursively on an object {key: elem}, where |key| is the
                # name (key) of the list and |elem| is any element.
                for elem in json_in[key]:
                    ret += self.get_number_context_pairs({key: elem}, parent_keys)
            if isinstance(json_in[key], str):
                # TODO: Try to handle strings like "29 million" by tokenizing them and searching for numbers.
                allowed_chars = '0123456789,.%/$E'
                if all(map(lambda c: c in allowed_chars, json_in[key])):
                    ret.append((json_in[key], self.mean_of_words(parent_keys_vec), parent_keys_str))
            if isinstance(json_in[key], int) or isinstance(json_in[key], float) or isinstance(json_in[key], bool):
                # If the value is a number, we can directly append it to ret.
                ret.append((str(json_in[key]), self.mean_of_words(parent_keys_vec), parent_keys_str))
            else:
                pass
        return ret

    def visualize_one(self, json_in: Dict, show_context: bool = False) -> None:
        """
        Constructs the list of pairs (number, vectorized context), reduces the context vectors dimensionality with t-SNE
        and displays with matplotlib.
        :param json_in: An input json.
        :param show_context: Whether to display the context string together with each embedded number value.
        """
        triples = self.get_number_context_pairs(json_in)
        triples = list(filter(lambda a: not (np.isnan(a[1])).any(), triples))
        only_embeddings = np.array(list(map(lambda a: a[1], triples)))
        reduced = TSNE(perplexity=5.0, verbose=2, learning_rate=20.0, n_iter=10000).fit_transform(only_embeddings)
        fig, ax = plt.subplots()
        ax.scatter(reduced[:, 0], reduced[:, 1])
        for i, txt in enumerate(reduced):
            annotation = triples[i][2] + ": " + triples[i][0] if show_context else triples[i][0]
            ax.annotate(annotation, reduced[i])
        plt.show()

    def visualize_many(self, jsons_in: List[Dict], show_context: bool = False) -> None:
        """
        For each json, constructs the list of pairs (number, vectorized context), reduces them all with t-SNE and
        displays with matplotlib.

        :param jsons_in: Input jsons.
        :param show_context: Whether to display the context string together with each embedded number value.
        """
        def random_color():
            return [np.random.uniform(), np.random.uniform(), np.random.uniform()]
        # Each json gets its own random color for points visualization.
        colors = [random_color() for _ in jsons_in]

        triples = []
        c = []
        for i, json_in in enumerate(jsons_in):
            cur_triples = self.get_number_context_pairs(json_in)
            cur_triples = list(filter(lambda a: not (np.isnan(a[1])).any(), cur_triples))
            c += [colors[i]] * len(cur_triples)
            triples += cur_triples
        only_embeddings = np.array(list(map(lambda a: a[1], triples)))
        reduced = TSNE(perplexity=5.0,
                       verbose=2,
                       learning_rate=2.0,
                       n_iter=10000).fit_transform(only_embeddings)
        fig, ax = plt.subplots()
        ax.scatter(reduced[:, 0], reduced[:, 1], c=np.array(c))
        for i, txt in enumerate(reduced):
            annotation = triples[i][2] + ": " + triples[i][0] if show_context else triples[i][0]
            ax.annotate(annotation, reduced[i])
        plt.show()
