import numpy as np
from typing import Optional


class ModelBase:
    """
    Base class (interface) for various word vector models. Its purpose is to encapsulate models from different API and
    give them a unified interace.
    """

    def __init__(self):
        pass

    def get_vector(self, word: str) -> Optional[np.ndarray]:
        """
        Gets the word vector for given word. Returns None if such word is not present in the model's dictionary.

        :param word: Word for which vector should be obtained.
        :return: Either a single word vector or None.
        """
        raise NotImplementedError()