import numpy as np
from typing import Optional, List

from flair.embeddings import FlairEmbeddings, WordEmbeddings, StackedEmbeddings, Sentence
from word_vectors_model.model_base import ModelBase


class FlairPretrained(ModelBase):
    """
    Encapsulates pretrained Flair Embeddings (Zalando Flair) by conforming to the ModelBase interface.
    """

    def __init__(self, model = None):
        super(FlairPretrained, self).__init__()

        if model is not None:
            self.model = model
        else:
            self.model = StackedEmbeddings([
                FlairEmbeddings('news-forward-fast'),
                FlairEmbeddings('news-backward-fast'),
            ])

    def dim(self) -> int:
        """
        The dimensionality of created embeddings.

        :return: 2048 (for now, #TODO)
        """
        return 2048

    def get_word_vector(self, word: str) -> Optional[np.ndarray]:
        """
        Returns the word vector for word |word| or None. It is discouraged to use this method as it invalidates the
        purpose of Flair embeddings. Instead, utilize the context as well for more accurate vectorization.

        In reality, Flair embeddings never return None, even for bogus words.

        :param word: The word to vectorize.
        :return: Either the word vector or None.
        """
        dummy_sentence = Sentence(word)
        self.model.embed(dummy_sentence)
        return np.array(list(dummy_sentence)[0].embedding)

    def get_word_vectors(self, words: List[str]) -> List[np.ndarray]:
        """
        Vectorizes the list of words, using pretrained Flair embeddings. These embeddings are context dependent, so this
        method is preferred over fetching word vectors for single words.

        :param words: The list of words to vectorize.
        :return: A list of word vectors.
        """
        sentence = Sentence(' '.join(words))
        self.model.embed(sentence)
        return list(
            map(lambda token: np.array(token.embedding),
                list(sentence))
        )

    def vectorize_context(self, words: List[str]) -> Optional[np.ndarray]:
        """
        Transforms the context into a single vector. May return None in extreme cases, e.g. if |words| is an empty list.

        :param words: List of tokens describing the context.
        :return: A single word vector or None.
        """
        return self.mean_of_words(self.get_word_vectors(words))
