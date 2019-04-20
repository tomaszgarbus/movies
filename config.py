# My API key for omdbapi.com.
OMDB_API_KEY = '7ff171ab'

# Relative path to data directory.
DATA_DIR = 'data'

# Path to cached json responses from omdbapi.com.
OMDB_JSONS_DIR = DATA_DIR + '/' + 'omdb_jsons'

# Path to cached Wikipedia articles.
WIKIPEDIA_CACHE_DIR = DATA_DIR + '/' + 'wiki_cache'

# Word2vec dimension.
W2V_DIM = 300

# Pretrained word2vec path.
PRETRAINED_W2V_PATH = DATA_DIR + '/GoogleNews-vectors-negative300.bin'

# Path to the csv containing the list of movies to fetch.
MOVIES_TO_FETCH_PATH = DATA_DIR + '/movies_to_download.csv'
