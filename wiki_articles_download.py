import nltk
import os
import requests
from lxml import html
from typing import Optional, Dict, Callable, List
import string

from config import WIKIPEDIA_CACHE_DIR


def _contains_letter_or_digit(s: str) -> bool:
    """
    Decides whether |s| contains some alphanumeric character. Meant for use when filtering created tokens during
    tokenizing.

    :param s: A single string token.
    :return: True iff there is at least one alphanumeric character in |s|.
    """
    letters_and_digits = string.ascii_letters + string.digits
    return any(map(lambda c: c in s, letters_and_digits))


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
    if cache_result is None:
        article = download_article(resource_name)
        store_article_to_cache(resource_name, article)
        return article
    else:
        return cache_result


def tokens_list_to_context_json(tokens: List[str],
                                window_size = 2,
                                include_if: Callable[[str], bool] = lambda s: True) -> Dict:
    """
    Transforms the tokenized article to a flat json. The keys are possible contexts of width |window_size| * 2.
    The resulting json consists of key-value pairs context: word, where context is a list of words split by a single
    space.

    :param tokens: The tokenized article.
    :param window_size: The width (i.e. number of words) of the context from the left and right side.
    :param limit_
    :param include_if: A function determining for a given word whether it should get a dedicated
    :return: A Python dictionary, i.e. a representation of a json.
    """
    ret = {}
    for i, w in enumerate(tokens):
        if not include_if(w):
            continue
        context_words = tokens[i - window_size:i] + tokens[i + 1:i + window_size + 1]
        ret[' '.join(context_words)] = w
    return ret


def tokenize_article_text(article_text: str, filter_fun: Callable[[str], bool] = lambda s: True) -> List[str]:
    """
    Tokenizes the article and filters the tokens basing on |filter_fun| function.

    :param article_text: Text of a Wikipedia article. This must be plain text, not HTML nor markdown.
    :param filter_fun: A function determining for a given word whether it should be included in the list of tokens.
    :return: A List of strings - (filtered) tokens.
    """
    words = nltk.word_tokenize(article_text)
    return list(filter(filter_fun, words))


def article_text_to_context_json(article_text: str,
                                 window_size = 2,
                                 include_if: Callable[[str], bool] = lambda s: True) -> Dict:
    """
    Transforms the article text to a flat json. The keys are possible contexts of width |window_size| * 2.
    The resulting json consists of key-value pairs context: word, where context is a list of words split by a single
    space.

    :param article_text: Text of a Wikipedia article. This must be a plain text, not HTML nor markdown.
    :param window_size: The width (i.e. number of words) of the context from the left and right side.
    :param include_if: A function determining for a given word whether it should get a dedicated key:value pair in
                       the resulting json.
    :return: A Python dictionary, i.e. a representation of a json.
    """
    words = nltk.word_tokenize(article_text)
    return tokens_list_to_context_json(words, window_size, include_if)


def filter_no_letter_or_digit(tokenized_article: List[str]) -> List[str]:
    """
    Filters the tokenized article by removing those tokens that do not contain any letter nor digit.
    :param tokenized_article: List of tokens.
    :return: List of tokens after filtering.
    """
    return list(filter(_contains_letter_or_digit, tokenized_article))


def tokenize_and_filter_no_alphanumeric(article_text: str) -> List[str]:
    """
    Tokenizes the article and filters out the tokens that do not contain any letter nor digit.
    :param article_text:
    :return:
    """
    return tokenize_article_text(article_text, filter_fun=_contains_letter_or_digit)


def cut_by_citations(article_text: str) -> str:
    """
    Heuristically cuts the article before the "Citations" section. "Heuristically" because it just searches for the
    first occurrence of the word "Citations" (case matters).

    :param article_text: Text of Wikipedia article. This must be a plain text, not HTML nor markdown.
    :return: A string - some prefix of provided article text.
    """
    citations_pos = article_text.find('Citations')
    return article_text[:citations_pos] if citations_pos != -1 else article_text


if __name__ == '__main__':
    article_text = download_article('Star_Wars_(film)')
    # print(nltk.word_tokenize(article_text))
    # print(download_article("Star_Wars_(film)"))
    print(article_text_to_context_json(article_text))

