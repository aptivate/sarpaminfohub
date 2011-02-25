# Create your views here.

from django.shortcuts import render_to_response
from forms import SearchForm
from sarpaminfohub.infohub.results_table import ResultsTable
from sarpaminfohub.infohub.drug_searcher import DrugSearcher
from sarpaminfohub.infohub.django_backend import DjangoBackend
from sarpaminfohub.infohub.test_backend import TestBackend

def search(request):
    search_term = request.GET.get('search', None)
    
    initial_form_values = {'search' : search_term} 

    if search_term is not None:
        backend_param = request.GET.get('backend', "django")
        
        if backend_param == "test":
            backend = TestBackend()
        else:
            backend = DjangoBackend()
            
        drug_searcher = DrugSearcher(backend)
        rows = drug_searcher.get_rows(search_term)
    
        results_table = ResultsTable(rows, search_term)
    else:
        results_table = None
        
    search_form = SearchForm(initial = initial_form_values)
    
    return render_to_response('search.html', 
                              {'search_form': search_form,
                               'results_table': results_table})