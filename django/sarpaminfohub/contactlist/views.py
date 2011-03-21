from haystack.query import SearchQuerySet
from contactlist.forms import SearchForm
from django.shortcuts import render_to_response
from tagging.models import Tag

def tag_search(request):
    query = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('tag', False):
                search_term = "%s %s"%(form.cleaned_data['search_term'],form.cleaned_data['tag'])
            else:
                search_term = form.cleaned_data['search_term']
            query = SearchQuerySet().auto_query(search_term)
    else:
        form = SearchForm()
    extra_context = {
        'query': query,
        'form': form,
    }
    return render_to_response('search/search.html', extra_context)