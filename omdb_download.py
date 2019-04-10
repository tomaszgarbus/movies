import requests
import json
import os
from typing import Dict, Optional
from config import OMDB_API_KEY, OMDB_JSONS_DIR


def cache_movie_json(title: str, json_response: Dict) -> None:
    """
    Caches OMDb API response json on disk.

    :param title: Title provided when searching omdapi for the movie, also the filename for cached json file.
    :param json_response: Response provided by omdapi.com
    """
    fpath = os.path.join(OMDB_JSONS_DIR, title)
    with open(fpath, 'a+') as fp:
        json.dump(json_response, fp)


def load_movie_json_from_cache(title: str) -> Optional[Dict]:
    """
    Fetches the movie json from disk, if available.

    :param title: Filename to search for movie json.
    :return: Either a cached json or None.
    """
    fpath = os.path.join(OMDB_JSONS_DIR, title)
    if os.path.exists(fpath):
        with open(fpath, 'r') as fp:
            return json.load(fp)
    return None


def get_and_cache_movie_json(title: str) -> Dict:
    """
    Fetches json for the movie titled |title| from omdapi.com or from local cache.
    If the json response is not cached yet, caches it on disk.
    """
    cached = load_movie_json_from_cache(title)
    if cached:
        return cached
    rsp = requests.get(url='http://www.omdbapi.com',
                       params={
                           't': title,
                           'plot': 'full',
                           'apikey': OMDB_API_KEY
                       })
    json_response = rsp.json()
    cache_movie_json(title, json_response)
    return json_response
