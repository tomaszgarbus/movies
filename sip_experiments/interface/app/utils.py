import os
from html.parser import HTMLParser
from typing import List, Tuple

from app.constants import SAMPLE_1000_DIR, KEYWORDS_STR, AUTHOR_STR
from app.sip_parsers import KeywordsHTMLParser


def open_raw_html(fname: str) -> str:
    """
    Loads and returns raw HTML from static files for the given filename.

    :param fname: Filename, must match pattern 'c\d\d\d\d\d\d' (\d is digit).
    :return: A single string - file contents.
    """
    assert len(fname) == 7
    assert fname[0] == 'c'
    assert fname[1:].isnumeric()
    fpath = os.path.join(SAMPLE_1000_DIR, fname + '.html')
    with open(fpath, 'r') as file:
        contents = file.read()
    return contents


def load_top_5_similar(fname: str) -> List[Tuple[float, str]]:
    """
    For a given filename, loads the list of pairs (similarity, filename) - top 5 most similar files.
    :param fname: Filename of the queried document.
    :return: A list of pairs (cosine similarity, filename).
    """
    fpath = os.path.join(SAMPLE_1000_DIR, fname + '.html.sims')
    ret = []
    with open(fpath, 'r') as file:
        contents = file.read()
        for line in contents.split('\n'):
            if line == '':
                continue
            sim, name = line.split(' ')
            sim = float(sim)
            name = name[:-5]
            ret.append((sim, name))
    return ret


def get_keywords_heur(raw_html: str) -> List[str]:
    """
    From a raw HTML document, fetches the list of keywords and returns them as a list.
    This is a heuristic tested on few HTMLs with no guarantee to work well.

    :param raw_html: A raw HTML.
    :return: List of keywords (potentially empty because this is a terrible heuristic).
    """
    parser = KeywordsHTMLParser()
    parser.feed(raw_html)
    keywords = parser.get_keywords()
    return keywords
