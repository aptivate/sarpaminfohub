# Create your views here.

from django.shortcuts import render_to_response
from forms import SearchForm

def search(request):
    search_form = SearchForm()
    return render_to_response('search.html', {'search_form': search_form})