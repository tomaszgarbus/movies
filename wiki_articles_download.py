import requests
from lxml import html
from typing import Optional, Dict, Callable
import nltk
import os
from config import WIKIPEDIA_CACHE_DIR


def download_article(resource_name: str) -> Optional[str]:
    """
    Downloads the full Wikipedia article for the given resource name.

    :param resource_name: Resource name (must match exactly). For example, for Star Wars Episode IV that would be
                          "Star_Wars_(film)".
    :return: A string - full Wikipedia article.
    """
    rsp = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=parse&page=' + resource_name)
    text = rsp.json()['parse']['text']['*']
    parsed_html = html.document_fromstring(text)
    return parsed_html.text_content()


def store_article_to_cache(resource_name: str, article_text: str) -> None:
    """
    Stores the |article_text| to cache dedicated to Wikipedia articles.

    :param resource_name: Exact Wikipedia resource name corresponding to the article.
    :param article_text: Text of the article to be saved.
    """
    if not os.path.exists(WIKIPEDIA_CACHE_DIR):
        os.makedirs(WIKIPEDIA_CACHE_DIR, exist_ok=True)
    fpath = os.path.join(WIKIPEDIA_CACHE_DIR, resource_name)
    with open(fpath, 'w+') as file:
        file.write(article_text)


def load_article_from_cache(resource_name: str) -> Optional[str]:
    """
    Loads article text from cache or returns None if not found.

    :param resource_name: Exact Wikipedia resource name corresponding to the article.
    :return: Either a string with cached article text or None.
    """
    if not os.path.exists(WIKIPEDIA_CACHE_DIR):
        return None
    fpath = os.path.join(WIKIPEDIA_CACHE_DIR, resource_name)
    if not os.path.exists(fpath):
        return None
    with open(fpath, 'r') as file:
        return file.read()


def download_article_or_load_from_cache(resource_name: str) -> Optional[str]:
    """
    Fetches the article text for the given Wikipedia resource name.
    :param resource_name: Exact name of the Wikipedia resource for the article.
    :return: Either a string with article in plain text (no HTML nor markdown) or None if none could have been obtained.
    """
    cache_result = load_article_from_cache(resource_name)
    return cache_result if cache_result is not None else download_article(resource_name)


def article_text_to_context_json(article_text: str,
                                 window_size = 2,
                                 include_if: Callable[[str], bool] = lambda s: True) -> Dict:
    """
    Transforms the article text to a flat json. The keys are possible contexts of width |window_size| * 2.
    The resulting json consists of key-value pairs context: word, where context is a list of words split by a single
    space.

    :param article_text: Text of a Wikipedia article. This must be a plain text, not HTML nor markdown.
    :param window_size: The width (i.e. number of words) of the context from the left and right side.
    :param include_if: A function determining for a given word whether it should get a dedicated
    :return: A Python dictionary, i.e. a representation of a json.
    """
    words = nltk.word_tokenize(article_text)
    ret = {}
    for i, w in enumerate(words):
        if not include_if(w):
            continue
        context_words = words[i - window_size:i] + words[i + 1:i + window_size + 1]
        ret[' '.join(context_words)] = w
    return ret


if __name__ == '__main__':
    article_text = download_article('Star_Wars_(film)')
    # print(nltk.word_tokenize(article_text))
    # print(download_article("Star_Wars_(film)"))
    print(article_text_to_context_json(article_text))

