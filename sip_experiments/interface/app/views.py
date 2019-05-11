from django.shortcuts import render
from django.http import HttpResponse
import os
from app.utils import load_top_5_similar, open_raw_html, get_keywords_heur, get_subject_heur
from app.constants import SAMPLE_1000_DIR, NA_STR
from typing import Dict


def index(request):
    return HttpResponse("Hello, world.")


def build_doc_description(doc_name: str) -> Dict[str, str]:
    """
    Builds a dictionary describing a document, given the document name.

    :param doc_name: Document name. Must match pattern 'c\d\d\d\d\d\d', where '\d' is a digit.
    :return: A dictionary.
    """
    sims = load_top_5_similar(doc_name)
    raw_html = open_raw_html(doc_name)
    keywords = get_keywords_heur(raw_html)
    subject = get_subject_heur(raw_html)
    subject = subject if subject is not None else NA_STR
    return {
        'sims': sims,
        'subject': subject,
        'keywords': keywords,
        'doc_name': doc_name,
        'doc_src': 'sample1000/' + doc_name + '.html'
    }


def show(request, doc_name):
    return render(request, 'show.html', context={
        'desc': build_doc_description(doc_name=doc_name)
    })


def listall(request):
    dirpath = SAMPLE_1000_DIR
    files = os.listdir(dirpath)
    files = filter(lambda a: a.endswith('html'), files)
    files = map(lambda a: a[:-5], files)
    return render(request, 'listall.html', context={
        'files': files
    })


def compare(request, doc_name1: str, doc_name2: str):
    return render(request, 'compare.html', context={
        'desc1': build_doc_description(doc_name1),
        'desc2': build_doc_description(doc_name2)
    })
