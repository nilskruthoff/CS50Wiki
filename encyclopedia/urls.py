from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/entry/<str:page_title>', views.entry, name='app_wiki_entry'),
    path('wiki/entry/<str:page_title>/edit', views.entry_edit, name='app_wiki_entry_edit'),
    path('wiki/search', views.search, name='app_wiki_search'),
    path('wiki/random', views.random, name='app_wiki_random'),
    path('wiki/create', views.create, name='app_wiki_create')
]
