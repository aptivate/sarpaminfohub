from haystack.query import SearchQuerySet
from contactlist.forms import SearchForm
from django.shortcuts import render_to_response

def tag_search(request):
    # sqs = SearchQuerySet().filter(tags='recipe').auto_query('banana')
    # 
    # query = ''
    # results = EmptySearchQuerySet()
    
    if request.POST.get('search_term'):
        form = SearchForm(request.POST)
    else:
        form = SearchForm()
    extra_context = {
        'form': form,
    }

    return render_to_response('search/search.html', extra_context)