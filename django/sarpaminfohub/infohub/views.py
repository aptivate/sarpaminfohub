from django.shortcuts import render_to_response
from forms import SearchForm
from sarpaminfohub.infohub.results_table import ResultsTable
from sarpaminfohub.infohub.drug_searcher import DrugSearcher
from sarpaminfohub.infohub.django_backend import DjangoBackend
from sarpaminfohub.infohub.test_backend import TestBackend
from sarpaminfohub.infohub.formulation_table import FormulationTable
from sarpaminfohub.infohub.formulation_graph import FormulationGraph
import re

def get_backend(name):
    if name == "test":
        backend = TestBackend()
    else:
        backend = DjangoBackend()

    return backend

def search(request):
    search_term = request.GET.get('search', None)
    
    initial_form_values = {'search' : search_term} 

    if search_term is not None:
        backend_name = request.GET.get('backend', "django")
        
        backend = get_backend(backend_name)
            
        drug_searcher = DrugSearcher(backend)
        rows = drug_searcher.get_formulations_that_match(search_term)
    
        results_table = ResultsTable(rows, search_term)
    else:
        results_table = None
        
    search_form = SearchForm(initial = initial_form_values)
    
    return render_to_response('search.html', 
                              {'search_form': search_form,
                               'results_table': results_table})
    
def formulation(request, formulation_id, backend_name="django"):
    backend = get_backend(backend_name)

    drug_searcher = DrugSearcher(backend)
    rows = drug_searcher.get_prices_for_formulation_with_id(formulation_id)

    # Don't like that, but results is being changed in the constructor of the table.
    from copy import deepcopy
    rows_graph = deepcopy(rows)

    formulation_name = drug_searcher.get_formulation_name_with_id(formulation_id)
    formulation_msh = drug_searcher.get_formulation_msh_with_id(formulation_id)

    formulation_table = FormulationTable(rows)
    formulation_graph = FormulationGraph(rows_graph, formulation_msh)

    results_href = None

    referer = request.META.get('HTTP_REFERER')

    if referer is not None:
        referer_parts = re.sub('^https?:\/\/', '', referer).split('/')

        referer_host = referer_parts[0]

        if referer_host == '' or referer_host == request.META.get('HTTP_HOST'):
            results_href = referer

    search_form = SearchForm()

    return render_to_response('formulation.html',
                              {'formulation_table': formulation_table,
                               'formulation_graph': formulation_graph,
                               'formulation_name': formulation_name,
                               'formulation_msh': formulation_msh,
                               'results_href' : results_href,
                               'search_form' : search_form});
