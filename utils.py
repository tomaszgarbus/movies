from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config import W2V_DIM


def embeddings_sim(vec1: np.ndarray, vec2: np.ndarray, dim: int = W2V_DIM) -> float:
    """
    Calculates the similarity between two vectors. These may be single word vectors or combined (e.g. by mean).

    :param vec1: First word embedding.
    :param vec2: Second word embedding.
    :param dim: Dimensionality of the vectors.
    :return: Cosine similarity.
    """
    return cosine_similarity(vec1.reshape((-1, dim)),
                             vec2.reshape((-1, dim)))[0, 0]


def number_heuristic(s: str) -> bool:
    """
    A heuristic meant to be used as an argument for filtering json keys and values.

    :param s: A key candidate.
    :return: True iff |s| should be treated as a number.
    """
    allowed_chars = '0123456789,./$E'
    any_digit = False
    for c in s:
        if c.isdigit():
            any_digit = True
        if c not in allowed_chars:
            return False
    return any_digit