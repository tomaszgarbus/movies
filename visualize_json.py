"""
A temporary class for visualizing Jsons with matplotlib.
First we create a list of (number, context) pairs, where context is vectorized, then use t-SNE to visualize it on a 2D
plane.
"""
from typing import List, Tuple, Dict
import numpy as np
import gensim
from sklearn.manifold import TSNE
import matplotlib as plt


class VisualizeJson:
    def __init__(self, w2v_model: gensim.models.KeyedVectors):
        self.w2v_model = w2v_model

    def get_number_context_pairs(self, json_in: Dict) -> List[Tuple[float, np.ndarray]]:
        """
        Transforms a json into a list of pairs (number, vectorized context).
        TODO: handle KeyError (no such word in vocabulary)

        :param json_in: A dictionary created from an input json.
        :return: List of pairs (number, vectorized context).
        """
        ret = []
        # TODO: Handle nested objects.
        for key in json_in:
            try:
                number = float(json_in[key])
                # TODO: split key if multiple words.
                key_vector = self.w2v_model.get_vector(key)
                ret.append((number, key_vector))
            except (ValueError, TypeError, KeyError):
                pass
        return ret

    def visualize(self, json_in: Dict) -> None:
        pairs = self.get_number_context_pairs(json_in)
        reduced = TSNE().fit_transform(list(map(lambda a: a[1], pairs)))
        fig, ax = plt.subplots()
        ax.scatter(reduced[:, 0], reduced[:, 1])
        for i, txt in enumerate(reduced):
            ax.annotate(pairs[i][0], reduced[i])
        plt.show()
