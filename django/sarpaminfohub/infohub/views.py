# Create your views here.

from django.shortcuts import render_to_response
from forms import SearchForm
from sarpaminfohub.infohub.results_table import ResultsTable
from sarpaminfohub.infohub.drug_searcher import DrugSearcher
from sarpaminfohub.infohub.test_backend import TestBackend

def search(request):
    search_form = SearchForm()
#    countries = [{'name': 'Australia', 'population': 21, 'tz': 'UTC +10', 'visits': 1}]
    #,{'name': 'Germany', 'population', 81, 'tz': 'UTC +1', 'visits': 2},{'name': 'Mexico', 'population': 107, 'tz': 'UTC -6', 'visits': 0}]
    
    search_term = request.GET.get('search', None)
    
    if search_term is not None:
        backend = TestBackend()
        drug_searcher = DrugSearcher(backend)
        rows = drug_searcher.get_rows(search_term)
    
        results_table = ResultsTable(rows)
    else:
        results_table = None
        
    return render_to_response('search.html', 
                              {'search_form': search_form,
                               'results_table': results_table})