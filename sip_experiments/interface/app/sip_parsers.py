from html.parser import HTMLParser
from typing import List
from app.constants import AUTHOR_STR, KEYWORDS_STR


class KeywordsHTMLParser(HTMLParser):
    """
    A class for extracting keywords from HTML document. Note that this is a terrible heuristic but the documents are
    not valid HTMLs so it has to suffice.

    Example usage:
    parser = KeywordsHTMLParser()
    parser.feed(raw_html)
    keywords = parser.get_keywords()
    """
    def __init__(self):
        super(KeywordsHTMLParser, self).__init__()
        self.started_parsing_keywords = False
        self.keywords: List[str] = []

    def error(self, message):
        pass

    def handle_data(self, data):
        if self.started_parsing_keywords:
            if data == AUTHOR_STR:
                self.started_parsing_keywords = False
            else:
                if not str(data).startswith('$'):
                    self.keywords.append(str(data))
        else:
            if data == KEYWORDS_STR:
                self.started_parsing_keywords = True

    def get_keywords(self) -> List[str]:
        """
        Fetches the list of found keywords.
        :return: A list of strings (possibly empty).
        """
        return self.keywords