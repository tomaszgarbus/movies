from typing import Optional

import numpy as np
from word_vectors_model.model_base import ModelBase
import gensim
from utils import number_heuristic


class GoogleNewsW2V(ModelBase):
    """
    A class encapsulating pretrained GoogleNews word2vec vectors.
    """

    def __init__(self, w2v_model: gensim.models.KeyedVectors):
        """
        Initializes the instance with a loaded Google News model.

        :param w2v_model: Initialized gensim class with vectors loaded from file.
        """
        super(GoogleNewsW2V, self).__init__()
        self.w2v_model = w2v_model

    def _safe_get_vector(self, word: str) -> Optional[np.ndarray]:
        """
        Returns the word vector for |word| or None if the word is not in vocabulary of the w2v model.

        :param word: word.
        :return: Embedding or None.
        """
        try:
            return self.w2v_model.get_vector(word)
        except KeyError:
            if number_heuristic(word):
                # The GoogleNews-trained vectors do not contain embeddings for numbers (well, most of them), but they
                # do contain embeddings for '#', '##', ... '#' * 14, which for now I will assume are placeholders for
                # numbers of different representation lengths.
                # TODO: consider generating new random vectors for unknown numbers (ideally, in a deterministic way
                #       so that they don't need to be stored), e.g. seed for random generator can be the provided
                #       number.
                return self._safe_get_vector('#' * len(word))
            return None

    def get_word_vector(self, word: str) -> Optional[np.ndarray]:
        """
        Returns the word vector for |word| or None if the word is not in vocabulary of the w2v model.

        :param word: word.
        :return: Embedding or None.
        """
        return self._safe_get_vector(word)

