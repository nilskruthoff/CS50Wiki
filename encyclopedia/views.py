from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from markdown2 import Markdown

from . import util
from . import Forms
from .Forms import SearchForm


def index(request):
    entries_dict = util.get_entries_url(util.list_entries())

    return render(request, "encyclopedia/index.html", {
        "entries": entries_dict
    })


def entry(request, page_title: str):
    try:
        file = open(f"entries/{page_title}.md", 'r')

        markdowner = Markdown()
        markdowned_content = []
        for line in file.readlines():
            markdowned_content.append(markdowner.convert(line))

        return render(request, "encyclopedia/entry.html", {
            "page_title": page_title.capitalize(),
            "content": markdowned_content
        })
    except IOError:
        return render(request, "encyclopedia/404.html")


def entry_edit(request):
    pass


def search(request):
    query = request.POST['q']
    lcs_entries = util.list_entries_lowercase(util.list_entries())

    if query.lower() in lcs_entries:
        return redirect('app_wiki_entry', page_title=query)
    else:
        search_results = []
        for entry in lcs_entries:
            result = entry.find(query.lower())

            if result != -1:
                search_results.append(entry)

        if len(search_results) > 0:
            return render(request, "encyclopedia/search_results.html", {
                "query": query,
                "search_result": util.get_entries_url([res.title() for res in search_results])
            })
        else:
            return render(request, "encyclopedia/404.html")


def random(request):
    pass


def create(request):
    pass


def edit(request):
    pass


