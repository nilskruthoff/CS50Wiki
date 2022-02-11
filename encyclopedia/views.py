import random as rnd

import markdown
from django.contrib import messages
from django.shortcuts import render, redirect

from . import util
from .Forms.PageForm import PageForm


def index(request):
    entries_dict = util.get_entries_url(util.list_entries())

    return render(request, "encyclopedia/index.html", {
        "entries": entries_dict
    })


def entry(request, page_title):
    """
    Looks if file with page_title exists and parse its markdown content to html.

    params -> page_title: title of entry page
    return -> Renders a page for the entry OR renders 404 Error
    route: /wiki/entry/{page}
    """
    try:
        with open(f"entries/{page_title}.md", 'r', encoding='utf-8') as file:
            html = markdown.markdown(''.join(file.readlines()))

        return render(request, "encyclopedia/entry.html", {
            "page_title": page_title.capitalize(),
            "content": html
        })
    except IOError:
        return render(request, "encyclopedia/404.html")


def entry_edit(request, page_title):
    """
    POST -> Overwrites an entry md file with new comment from an edit form
    GET -> Renders a form with prepopulated data for title and content from page form

    params -> page_title: title of entry page
    return -> Redirect to the entry page OR Render the page form
    route: /wiki/entry/{page}/edit
    """
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
    """
    Fetches a search keyword from search bar and renders the page if entry exists.
    Search for substring in all entries and create a search result page

    return -> Redirect to the entry page OR Render the page form
    route: /wiki/search
    """
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
    """
    Chooses a random entry and redirects to entry page

    return -> Redirect to the entry page
    route: /wiki/random
    """
    entries = util.list_entries()
    r = rnd.randint(0, len(entries) - 1)
    return redirect('app_wiki_entry', page_title=entries[r])


def create(request):
    """
    POST -> Creates a new entry with the posted form data if entry doesn't already exist. Else it
            Adds an alert on the page and redirects back to the create page
    GET -> Renders a new page form to create a new entry

    return -> Redirect to entry page OR redirect back to create page OR Renders a create page
    route: wiki/create
    """
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
                messages.add_message(request, messages.INFO, 'Hello world.')
                return render(request, "encyclopedia/create_entry.html", {
                    "form": PageForm(initial={
                        'title': title,
                        'content': content
                    }),
                    "error": True
                })
    else:
        return render(request, "encyclopedia/create_entry.html", {
            "form": PageForm(),
            "error": False
        })
