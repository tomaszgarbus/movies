from typing import Optional, List

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

    def dim(self) -> int:
        """
        The dimensionality of used W2V embeddings.

        :return: 300, for now (#TODO)
        """
        return 300

    def _safe_get_vectors(self, words: List[str]) -> List[np.ndarray]:
        """
        Returns the list of word vectors for all known words in |words| (note that the list may be empty).

        :param words: List of words for which the vectors should be fetched.
        :return: List of embeddings for known words.
        """
        return list(filter(lambda a: a is not None, map(self._safe_get_vector, words)))

    def get_word_vectors(self, words: List[str]) -> List[np.ndarray]:
        """
        Vectorizes the list of words. If a word is not present in GoogleNews dictionary, it is ignored.

        :param words: List of words to vectorize.
        :return: List of word vectors.
        """
        return self._safe_get_vectors(words)

    def get_word_vector(self, word: str) -> Optional[np.ndarray]:
        """
        Returns the word vector for |word| or None if the word is not in vocabulary of the w2v model.

        :param word: The word to vectorize.
        :return: Embedding or None.
        """
        return self._safe_get_vector(word)

    def vectorize_context(self, words: List[str]) -> Optional[np.ndarray]:
        """
        Vectorizes the context, provided as a list of words, by vectorizing each word and averaging the vectors. In some
        cases may return None (e.g. if all words failed to vectorize or there weren't any).

        :param words: List of words describing the context.
        :return: A single vector or None.
        """
        return self.mean_of_words(self.get_word_vectors(words))


