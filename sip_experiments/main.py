from typing import List, Optional
import os
from sip_experiments.constants_sip import SAMPLE_1000_PATH
from lxml import html
from tqdm import tqdm
from word_vectors_model.model_base import ModelBase
from word_vectors_model.bert_pretrained import BertPretrained
from word_vectors_model.flair_pretrained import FlairPretrained
from flair.embeddings import BertEmbeddings, FlairEmbeddings
import nltk
import numpy as np
from visualize_json import VisualizeJson, NumberContext


def list_sample_files() -> List[str]:
    """
    Provides the list of filenames selected in the sample.

    :return: A list of strings - filenames.
    """
    return list(filter(lambda f: f.endswith('.html'), os.listdir(SAMPLE_1000_PATH)))


def read_sample_file(fname: str) -> str:
    """
    Reads one of the sample tax files. Parses the html to provide more readable text.

    :param fname: Filename.
    :return: File contents.
    """
    with open(os.path.join(SAMPLE_1000_PATH, fname), 'r') as file:
        text = file.read()
    parsed_html = html.document_fromstring(bytes(text, 'utf-8'))
    return parsed_html.text_content()


def cut_text_by_phrase(text: str, phrase: str = 'Typ dokumentu') -> str:
    """
    Cuts |text| from the first occurrence of |phrase|.

    :param text: Text.
    :param phrase: Phrase.
    :return: Substring of |text|.
    """
    return text[text.find(phrase):]


def filter_non_alphanumeric_tokens(tokens: List[str]) -> List[str]:
    """
    Filters non-alphanumeric tokens from the list of tokens.

    :param tokens: List of tokens.
    :return: Sublist of |tokens|.
    """
    return list(filter(lambda s: s.isalnum(), tokens))


def load_embedding_from_cache(fname: str) -> Optional[np.ndarray]:
    """
    Loads embedding for filename from cache.

    :param fname: Filename.
    :return: None if not found, else numpy array.
    """
    fpath = os.path.join(SAMPLE_1000_PATH, fname + '.npy')
    if os.path.isfile(fpath):
        return np.load(fpath)
    else:
        return None


def embed_and_cache(sample: str, fname: str, model: ModelBase) -> np.ndarray:
    """
    Constructs or reads from cache embedding for the sample and caches it.

    :param sample: A raw sample.
    :param fname: Filename.
    :param model: Model used to vectorize |sample|.
    :return: A numpy array - an embedding.
    """
    loaded = load_embedding_from_cache(fname)
    if loaded is not None:
        return loaded
    else:
        fpath = os.path.join(SAMPLE_1000_PATH, fname + '.npy')
        tokenized = nltk.word_tokenize(cut_text_by_phrase(sample, 'Typ dokumentu'))
        tokenized = filter_non_alphanumeric_tokens(tokenized)
        embedding = model.vectorize_context(tokenized)
        np.save(fpath, embedding)
        return embedding


if __name__ == '__main__':
    # bert_model = BertPretrained(BertEmbeddings('bert-base-multilingual-cased'))
    # print("Instantiated bert_model")
    flair_model = FlairPretrained(FlairEmbeddings('polish-forward'))
    print("Instantiated flair_model")

    sample_files_list = list_sample_files()
    samples = []
    print("Loading samples")
    for fname in tqdm(sample_files_list):
        contents = read_sample_file(fname)
        samples.append(contents)

    print("Loading embeddings")
    embeddings = []
    for fname, sample in tqdm(zip(sample_files_list, samples)):
        embeddings.append(embed_and_cache(sample, fname, flair_model))
        assert embeddings[-1] is not None

    print("Building number-context pairs")
    numcons: List[NumberContext] = []
    for fname, embedding, sample in tqdm(zip(sample_files_list, embeddings, samples)):
        numcons.append((fname, embedding, sample))

    print("Finding k-closest")
    json_viz = VisualizeJson(model=flair_model)
    found = json_viz.k_closest_contexts(numcons[0][1], numcons, k=1000)
    print(numcons[0][0])
    for numcon, sim in found:
        print(sim, numcon[0])
