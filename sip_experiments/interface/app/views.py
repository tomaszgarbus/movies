from django.shortcuts import render
from django.http import HttpResponse
import os
from interface import settings


def index(request):
    return HttpResponse("Hello, world.")


def show(request, doc_name):
    return render(request, 'show.html', context={
        'doc_name': doc_name,
        'doc_src': 'sample1000/' + doc_name + '.html'
    })


def listall(request):
    dirpath = 'app/sample1000'
    return HttpResponse('<br>'.join(os.listdir(dirpath)))


def compare(request, doc_name1: str, doc_name2: str):
    return render(request, 'compare.html', context={
        'doc1_name': doc_name1,
        'doc2_name': doc_name2,
        'doc1_src': 'sample1000/' + doc_name1 + '.html',
        'doc2_src': 'sample1000/' + doc_name2 + '.html',
    })
