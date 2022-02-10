from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from markdown2 import Markdown

from . import util
from .Forms.PageForm import PageForm


def index(request):
    entries_dict = util.get_entries_url(util.list_entries())

    return render(request, "encyclopedia/index.html", {
        "entries": entries_dict
    })


def entry(request, page_title: str):
    try:
        with open(f"entries/{page_title}.md", 'r', encoding='utf-8') as file:

            markdowner = Markdown()
            markdowned_content = [markdowner.convert(file.read())]

        return render(request, "encyclopedia/entry.html", {
            "page_title": page_title.capitalize(),
            "content": markdowned_content
        })
    except IOError:
        return render(request, "encyclopedia/404.html")


def entry_edit(request, page_title):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            with open(f"entries/{page_title}.md", 'w', encoding='utf-8') as file:
                file.write(form.cleaned_data['content'])

        return redirect('app_wiki_entry', page_title=page_title)
    else:
        entry = open(f"entries/{page_title}.md", 'r', encoding='utf-8')
        form = PageForm(initial={
            'title': page_title,
            'content': entry.read()
        })

        return render(request, 'encyclopedia/edit_entry.html', {
            "page_title": page_title.title(),
            "form": form
        })


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
    if request.method == "POST":
        page_form = PageForm(request.POST)
        if page_form.is_valid():
            title = page_form.cleaned_data['title']
            content = page_form.cleaned_data['content']

            if title.lower() not in util.list_entries_lowercase(util.list_entries()):
                with open(f"entries/{title}.md", 'w', encoding='utf-8') as new_file:
                    new_file.write(content)

                return redirect('app_wiki_entry', page_title=title)
            else:
                return HttpResponse(f'Page already exists.')
    else:
        return render(request, "encyclopedia/create_entry.html", {
            "form": PageForm()
        })


def edit(request):
    pass


