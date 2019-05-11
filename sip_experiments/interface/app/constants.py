from interface.settings import BASE_DIR
import os

# Path to the sample of 1000 documents.
SAMPLE_1000_DIR = os.path.join(BASE_DIR, 'app/static/sample1000')

# Pattern to find the "Document type" field in raw text.
DOCUMENT_TYPE_STR = 'Typ dokumentu:'

# Pattern to find the "Author" field in HTML.
AUTHOR_STR = 'Autor:'

# Pattern to find the "Keywords" field in HTML.
KEYWORDS_STR = 'Słowa kluczowe:'

# Pattern to find the "Interpretation subject" field in HTML.
INTERPRETATION_SUBJECT = 'Istota interpretacji:'

# Pattern to find the "Position" field in HTML.
POSITION_STR = 'Stanowisko:'

# "Not available" string.
NA_STR = "N/A"

# Possible headers for the question section, found manually on a small sample of documents.
# There is no guarantee that this set will cover the entire dataset but should do for a vast majority of cases.
QUESTION_SECTION_HEADERS = [
    'W związku z powyższym zadano następujące pytanie:',
    'W związku z powyższym zadano następujące pytania.',
    'W związku z powyższym zadano następujące pytanie.',
    'W związku z powyższym zadano następujące:',
    'W związku z opisanym stanem faktycznym zadano następujące pytanie:',
    'W związku z powyższym zadano następujące pytanie',
]

# Possible headers for the verdict section, found manually on a small sample of documents.
# There is no guarantee that this set will cover the entire dataset but should do for most cases.
VERDICT_SECTION_HEADERS = [
    'W świetle obowiązującego stanu prawnego stanowisko wnioskodawcy w sprawie oceny prawnej przedstawionego stanu '
    'faktycznego uznaje się za nieprawidłowe.',
    'W świetle obowiązującego stanu prawnego stanowisko wnioskodawcy w sprawie oceny prawnej przedstawionego zdarzenia '
    'przyszłego uznaje się za prawidłowe.',
    'Na tle przedstawionego stanu faktycznego stwierdzam, co następuje.',
    'Na tle przedstawionego zdarzenia przyszłego, stwierdzam, co następuje.',
    'W świetle obowiązującego stanu prawnego stanowisko wnioskodawcy w sprawie oceny prawnej przedstawionego zdarzenia '
    'przyszłego uznaje się za prawidłowe mimo, iż podatnik powołał błędną podstawę prawną.',
    'Na tle przedstawionego stanu faktycznego, stwierdzam, co następuje.',
]
