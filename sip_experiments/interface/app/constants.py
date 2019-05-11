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
