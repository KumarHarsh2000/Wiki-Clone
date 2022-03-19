import markdown2
from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from random import randint

from . import util
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request,entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request,"encyclopedia/nonExistingEntry.html",{
            "entryTitle": entry
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "entry": markdowner.convert(entryPage),
            "entryTitle": entry
        })

def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():    # if querry is found call to above entry function
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {
        "entries": util.search(q), 
        "q": q
        })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        #if title or content is missing in input
        if title == "" or content == "":
            return render(request, "encyclopedia/add.html", {
                "message": "Can't save with empty field.", 
                "title": title, 
                "content": content
                })
        #if the created file is already present
        if title in util.list_entries():
            return render(request, "encyclopedia/add.html", {
                "message": "Title already exist. Try another.", 
                "title": title, 
                "content": content
                })
        #if entry is valid we save the file
        util.save_entry(title, content)
        # redirected to above def entry() function, which will render the given entry
        return redirect("entry", entry=title)
    return render(request, "encyclopedia/add.html")

def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Can't save with empty field.", "entryTitle": title, "entry": content})
        #if some editable content is present
        util.save_entry(title, content)
        return redirect("entry", entry=title)
    return render(request, "encyclopedia/edit.html", {'entry': content, 'entryTitle': title})

def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry", entry=random_title)