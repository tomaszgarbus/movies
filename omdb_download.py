import requests
import json
from config import OMDB_API_KEY


def download_movie_json(title: str) -> json:
    rsp = requests.get(url='http://www.omdbapi.com',
                       params={
                           't': title,
                           'plot': 'full',
                           'apikey': OMDB_API_KEY
                       })
    return rsp.json()
