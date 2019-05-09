from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show/<str:doc_name>/', views.show, name='show'),
    path('compare/<str:doc_name1>/<str:doc_name2>', views.compare, name='compare'),
    path('listall/', views.listall, name='listall'),
]