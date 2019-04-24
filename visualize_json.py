"""
A temporary class for visualizing Jsons with matplotlib.
First we create a list of (number, context) pairs, where context is vectorized, then use t-SNE to visualize it on a 2D
plane.
"""
import matplotlib.pyplot as plt
import numpy as np
import re
from nltk import tokenize
from sklearn.manifold import TSNE
from typing import List, Tuple, Dict

from utils import embeddings_sim
from utils import number_heuristic
from word_vectors_model.model_base import ModelBase

# Type alias for (number, vectorized context, raw context).
# TODO: consider splitting raw context into left and right side.
NumberContext = Tuple[str, np.ndarray, str]


def _random_color() -> List[float]:
    """
    Generates a random color.

    :return: A random color in RGB ([0,1]^3) representation.
    """
    return [np.random.uniform(), np.random.uniform(), np.random.uniform()]


def _camel_case_split(identifier: str) -> List[str]:
    """
    Splits the strings in camelCase.

    :param identifier: The string to split.
    :return: A list of strings - words resulting from the split.
    """
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


class VisualizeJson:
    def __init__(self, model: ModelBase):
        self.model = model

    def get_number_context_pairs(self, json_in: Dict, parent_keys: List[str] = None) -> List[NumberContext]:
        """
        Transforms a json into a list of pairs (number, vectorized context, raw context).
        TODO: handle KeyError (no such word in vocabulary)

        :param json_in: A dictionary created from an input json.
        :param parent_keys: Keys passed down from higher levels of json.
        :return: List of pairs (number, vectorized context, raw context).
        """
        if not parent_keys:
            parent_keys = []
        ret = []
        for key in json_in:
            # Splits the key into multiple words if it is provided as a camelCase.
            key_camel_split = _camel_case_split(key)
            # Further splits the key string at each space.
            key_split = ' '.join(key_camel_split).split(' ')
            # Joins the |parent_keys| with the strings obtained by splitting the current key.
            parent_keys_ext = parent_keys + key_split
            # Joins all strings in |parent_keys_ext| into a string.
            parent_keys_str = ' '.join(parent_keys_ext)
            # Vectorizes |parent_keys_ext|.
            context_vec = self.model.vectorize_context(parent_keys_ext)
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
                if number_heuristic(json_in[key]) and context_vec is not None:
                    # The string value is accepted as a number.
                    ret.append((json_in[key], context_vec, parent_keys_str))
                else:
                    # The string value is not accepted as a number, but perhaps after tokenization some tokens will be
                    # valid numbers.
                    tokens = tokenize.word_tokenize(json_in[key])
                    for i, t in enumerate(tokens):
                        if number_heuristic(t):
                            local_context_str = parent_keys_ext + tokens[:i] + tokens[i+1:]
                            local_context_vec = self.model.vectorize_context(local_context_str)
                            if local_context_vec is not None:
                                ret.append((t, local_context_vec, ' '.join(local_context_str)))
            if ((isinstance(json_in[key], int) or isinstance(json_in[key], float) or isinstance(json_in[key], bool))
                    and context_vec is not None):
                # If the value is a number, we can directly append it to ret.
                ret.append((str(json_in[key]), context_vec, parent_keys_str))
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

    def visualize_many(self, jsons_in: List[Dict], limit_per_json: int = 150, show_context: bool = False) -> None:
        """
        For each json, constructs the list of pairs (number, vectorized context), reduces them all with t-SNE and
        displays with matplotlib.

        :param jsons_in: Input jsons.
        :param limit_per_json: Limit of values to be displayed per json.
        :param show_context: Whether to display the context string together with each embedded number value.
        """
        # Each json gets its own random color for points visualization.
        colors = [_random_color() for _ in jsons_in]

        triples = []
        c = []
        for i, json_in in enumerate(jsons_in):
            cur_triples = self.get_number_context_pairs(json_in)[:limit_per_json]
            cur_triples = list(filter(lambda a: not (np.isnan(a[1])).any(), cur_triples))
            c += [colors[i]] * len(cur_triples)
            triples += cur_triples
        only_embeddings = np.array(list(map(lambda a: a[1], triples)))
        reduced = TSNE(perplexity=5.0,
                       learning_rate=2.0,
                       n_iter=10000).fit_transform(only_embeddings)
        fig, ax = plt.subplots()
        ax.scatter(reduced[:, 0], reduced[:, 1], c=np.array(c))
        for i, txt in enumerate(reduced):
            annotation = triples[i][2] + ": " + triples[i][0] if show_context else triples[i][0]
            ax.annotate(annotation, reduced[i])
        plt.show()

    def k_closest_contexts(self, context_vec: np.ndarray, candidates: List[NumberContext], k: int = 5)\
            -> List[Tuple[NumberContext, float]]:
        """
        For a given vectorized context, finds k closest (number, context) pairs.

        :param context_vec: Vectorized context.
        :param candidates: List of candidate pairs.
        :param k: k
        :return: A subset of |candidates| of length min(k, len(candidates)), zipped with embeddings similarity.
        """
        sim_candidates = list(map(lambda cand: (embeddings_sim(context_vec, cand[1], self.model.dim()), cand),
                                  candidates))
        results = sorted(sim_candidates, key=lambda p: p[0], reverse=True)[:k]
        return list(map(lambda a: (a[1], a[0]), results))
