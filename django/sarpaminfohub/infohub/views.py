from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from copy import deepcopy

from sarpaminfohub.infohub.django_backend import DjangoBackend
from sarpaminfohub.infohub.drug_searcher import DrugSearcher
from sarpaminfohub.infohub.forms import SearchForm
from sarpaminfohub.infohub.formulation_graph import FormulationGraph
from sarpaminfohub.infohub.formulation_table import FormulationTable
from sarpaminfohub.infohub.menu import Menu
from sarpaminfohub.infohub.models import Product
from sarpaminfohub.infohub.price_popup import PricePopup
from sarpaminfohub.infohub.product_table import ProductTable
from sarpaminfohub.infohub.results_table import ResultsTable
from sarpaminfohub.infohub.test_backend import TestBackend

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
        search_results_tab = get_search_results_tab()
        menu = Menu([search_results_tab])
    else:
        menu = None
        results_table = None
        
    search_form = SearchForm(initial = initial_form_values)
    
    return render_to_response('search.html', 
                              {'search_form': search_form,
                               'results_table': results_table,
                               'menu' : menu},RequestContext(request))
    
def formulation(request, formulation_id, backend_name="django"):
    backend = get_backend(backend_name)

    drug_searcher = DrugSearcher(backend)
    rows = drug_searcher.get_prices_for_formulation_with_id(formulation_id)

    # Don't like that, but results is being changed in the constructor of the table.
    rows_graph = deepcopy(rows)

    formulation_name = drug_searcher.get_formulation_name_with_id(formulation_id)
    formulation_msh = drug_searcher.get_formulation_msh_with_id(formulation_id)

    formulation_table = FormulationTable(rows)
    formulation_graph = FormulationGraph(rows_graph, formulation_msh)

    search_form = SearchForm()

    products_href = reverse('formulation_products', args=[str(formulation_id),
                                                           backend_name])
    formulation_tab = get_formulation_tab(None)
    similar_products_tab = get_similar_products_tab(products_href)
    menu = Menu([formulation_tab, similar_products_tab])

    price_popups = []
    for price_fields in rows:
        price_popups.append(PricePopup(price_fields))
                
    return render_to_response('formulation.html',
                              {'formulation_table': formulation_table,
                               'formulation_graph': formulation_graph,
                               'formulation_msh': formulation_msh,
                               'price_popups': price_popups,
                               'menu' : menu,
                               'search_form' : search_form,
                               'sub_title' : "Formulation",
                               'sub_sub_title' : formulation_name},
                               RequestContext(request))

def formulation_products(request, formulation_id, backend_name="django"):
    backend = get_backend(backend_name)
    
    drug_searcher = DrugSearcher(backend)
    
    rows = drug_searcher.get_product_registrations_based_on_formulation_with_id(formulation_id)
    
    supplier_table = ProductTable(rows)
    search_form = SearchForm()

    formulation_name = drug_searcher.get_formulation_name_with_id(formulation_id)
    formulation_href = reverse('formulation-by-id', args=[str(formulation_id),
                                                    backend_name])

    formulation_tab = get_formulation_tab(formulation_href)
    similar_products_tab = get_similar_products_tab()
    menu = Menu([formulation_tab, similar_products_tab])

    return render_to_response('formulation_products.html',
                              {'supplier_table' : supplier_table,
                               'search_form' : search_form,
                               'menu' : menu,
                               'sub_title' : "Formulation",
                               'sub_sub_title' : formulation_name,
                               },
                               RequestContext(request))

def supplier_catalogue(request, supplier_id, backend_name="django"):
    backend = get_backend(backend_name)

    drug_searcher = DrugSearcher(backend)
    registrations = drug_searcher.get_registrations_from_supplier_with_id(supplier_id)
    search_form = SearchForm()
    catalogue_tab = get_catalogue_tab()
    menu = Menu([catalogue_tab])
    supplier_name = drug_searcher.get_name_of_supplier_with_id(supplier_id)
    
    return render_to_response('supplier_catalogue.html',
                              {'registrations': registrations,
                               'menu': menu,
                               'search_form': search_form,
                               'sub_title': "Supplier",
                               'sub_sub_title': supplier_name,
                               'backend': backend_name},
                               RequestContext(request))

def get_formulation_tab(formulation_href=None):
    return get_tab(formulation_href, "Procurement Prices")

def get_similar_products_tab(products_href=None):
    return get_tab(products_href, "Related Products")

def get_catalogue_tab():
    return get_tab(None, "Product Catalogue")

def get_search_results_tab():
    return get_tab(None, "Search Results")

def get_tab(href, text):
    return {'href' : href, 'text' : text}

def product_page_tab(product, selected):
    if selected:
        href = None
    else:
        href = reverse(product_page, args=[product.name])
    
    return get_tab(href, "Details")

def product_page(request, product_id):
    product = Product.objects.get(id=product_id)
    return render_to_response('product_page.html',
        RequestContext(request, 
                       dict(
            sub_title="Product",
            menu = Menu([product_page_tab(product, selected=True)]),
            product=product,
            search_form = SearchForm(),
            sub_sub_title=product.name)))
    
def pricing_iframe(request):
    extra_context = {'iframe_url':'/', 'iframe_title':"Drug Price Database"}
    return render_to_response('iframe/pricing.html', extra_context)
