from typing import List, Tuple
import os
from app.constants import SAMPLE_1000_DIR


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
