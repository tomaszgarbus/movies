import numpy as np
from typing import Optional, List


class ModelBase:
    """
    Base class (interface) for various word vector models. Its purpose is to encapsulate models from different API and
    give them a unified interace.
    """

    def __init__(self):
        pass

    def get_word_vector(self, word: str) -> Optional[np.ndarray]:
        """
        Gets the word vector for given word. Returns None if such word is not present in the model's dictionary.

        :param word: Word for which vector should be obtained.
        :return: Either a single word vector or None.
        """
        raise NotImplementedError()

    def get_word_vectors(self, words: List[str]) -> List[np.ndarray]:
        """
        Gets the word vectors for given list of words. If some word is not present in the dictionary, it is ignored,
        so do not depend on the length of returned list to be the same. In particular, the returned list may be empty.

        :param words: A list of words to vectorize.
        :return: A list of word vectors.
        """
        raise NotImplementedError()

    def mean_of_words(self, words: List[np.ndarray]) -> Optional[np.ndarray]:
        """
        Provided a list of word embeddings, returns a single vector of the same dimensionality, by calculating
        elementwise mean, or None if the provided list is empty. TODO: support weighted mean.

        :param words: A list of word vectors.
        :return: A single vector or None.
        """
        if not words:
            return None
        # TODO: weighted mean
        return np.mean(words, axis=0)

    def vectorize_context(self, words: List[str]) -> Optional[np.ndarray]:
        """
        Transforms the entire context, provided as a list of tokens, to a single vector of the same dimensionality as
        any other word vector.

        :param words: A list of words, representing the context.
        :return: Either a single vector or, in extreme cases, None (if the context is really invalid, e.g. empty list).
        """
        raise NotImplementedError()