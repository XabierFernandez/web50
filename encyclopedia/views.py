from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import markdown2
import random 

# Create your views here.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    search_text = request.GET.get("q", "").strip()
    entries = util.list_entries()

    if search_text in entries:
        return redirect("get_entry", title=search_text)

    result = [entry for entry in entries if search_text.lower() in entry.lower()]

    content = {
        "search_text": search_text,
        "content": (
            f"<ul>{''.join(f'<li><a href=\"/wiki/{entry}/\">{entry}</a></li>' for entry in result)}</ul>"
            if result
            else f"<p>No results found for \"{search_text}\".</p>"
        ),
    }

    return render(request, "encyclopedia/search.html", content)
 
def random_entry(request):
    entries = util.list_entries()  
    if entries:
        random_entry = random.choice(entries)  
        return redirect("get_entry", title=random_entry)  
    else:
        return HttpResponse("Requested page was not found.", status=404)

def get_entry(request, title):
    raw_content = util.get_entry(title)
    if raw_content:
        content = markdown2.markdown(raw_content)
        return render(request, 'encyclopedia/entry.html', {'title': title, 'content': content})
    else:
        return HttpResponse("Requested page was not found.", status=404)

def edit_entry(request, title):

    if request.method == "POST":
        # Retrieve the updated content from the text-area
        updated_content = request.POST.get("content")
        if updated_content is not None:
            # Save the content using util.save_entry
            util.save_entry(title, updated_content)
            return redirect("get_entry", title=title)  # Redirect back to the entry page
        else:
            return HttpResponse("No content provided.", status=400)

    # Get the entry content and fill the text-area, This is for the GET methos by default.
    content = util.get_entry(title)
    if content is not None:
        md_content = content
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": md_content
        })
    else:
        return HttpResponse("The requested page was not found.", status=404)

def new_entry(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        
        if not title or not content:
            #messages.error(request, "Title and content cannot be empty.")
            return render(request, "encyclopedia/new_entry.html", {
                "title": title,
                "content": content
            })
        
        # Check if an entry already exists with the provided title
        if util.get_entry(title):
            #messages.error(request, f"An entry with the title '{title}' already exists.")
            return render(request, "encyclopedia/new_page.html", {
                "title": title,
                "content": content
            })
        
        # Save the new entry
        util.save_entry(title, content)
        #messages.success(request, f"Entry '{title}' created successfully!")
        return redirect("get_entry", title=title)
    
    # For GET requests, display the empty form
    return render(request, "encyclopedia/new_entry.html")
