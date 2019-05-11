from django.shortcuts import render
from django.http import HttpResponse
import os
from app.utils import load_top_5_similar
from interface import settings
from app.constants import SAMPLE_1000_DIR


def index(request):
    return HttpResponse("Hello, world.")


def show(request, doc_name):
    sims = load_top_5_similar(doc_name)
    return render(request, 'show.html', context={
        'sims': sims,
        'doc_name': doc_name,
        'doc_src': 'sample1000/' + doc_name + '.html'
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
        'doc1_name': doc_name1,
        'doc2_name': doc_name2,
        'doc1_src': 'sample1000/' + doc_name1 + '.html',
        'doc2_src': 'sample1000/' + doc_name2 + '.html',
    })
