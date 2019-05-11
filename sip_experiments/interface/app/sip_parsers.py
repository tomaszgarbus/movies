from html.parser import HTMLParser
from typing import List, Optional
from app.constants import AUTHOR_STR, KEYWORDS_STR, INTERPRETATION_SUBJECT, POSITION_STR


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
        self.parsing_keywords = False
        self.keywords: List[str] = []

    def error(self, message):
        pass

    def handle_data(self, data):
        if self.parsing_keywords:
            if data == AUTHOR_STR:
                self.parsing_keywords = False
            else:
                if not str(data).startswith('$'):
                    self.keywords.append(str(data))
        else:
            if data == KEYWORDS_STR:
                self.parsing_keywords = True

    def get_keywords(self) -> List[str]:
        """
        Fetches the list of found keywords.
        :return: A list of strings (possibly empty).
        """
        return self.keywords


class InterpretationSubjectHTMLParser(HTMLParser):
    """
    A parser extracting interpretation subject from HTML document. Note that this is a terrible heuristic but the
    documents are not perfectly valid HTMLs so it has to suffice.

    Example usage:
    parser = IntepretationSubjectHTMLParser()
    parser.feed(raw_html)
    subj = parser.get_subject()
    """
    def __init__(self):
        super(InterpretationSubjectHTMLParser, self).__init__()
        self.parsing_subject = False
        self.interpretation = None

    def error(self, message):
        pass

    def handle_data(self, data):
        if self.parsing_subject:
            if data == POSITION_STR:
                self.parsing_subject = False
            else:
                if not str(data).startswith('$'):
                    self.interpretation = str(data)
        else:
            if data == INTERPRETATION_SUBJECT:
                self.parsing_subject = True

    def get_subject(self) -> Optional[str]:
        """
        Returns the found interpretation subject or None if it has failed to locate it.

        :return: A single string.
        """
        return self.interpretation
