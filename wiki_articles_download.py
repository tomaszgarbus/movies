import requests
from lxml import html
from typing import Optional, Dict, Callable
import nltk


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

