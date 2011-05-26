from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from sarpaminfohub.contactlist.forms import SearchForm

class TagSearcher(object):
    def __init__(self, request):
        self.request = request
        
    def search(self):                
        query = None
        search = False
        
        if self.request.method == 'POST':
            form = SearchForm(self.request.POST)
            if form.is_valid():
                if form.cleaned_data.get('tags', False):
                    string_tags = [tag.name for tag in form.cleaned_data.get('tags')]
                    tag_string = " ".join(string_tags)
                    search_term = "%s %s" % (form.cleaned_data['search_term'],
                                             tag_string)
                else:
                    search_term = form.cleaned_data['search_term']
                if search_term.strip(' '):
                    query = SearchQuerySet().auto_query(search_term)
                    search = True
                else:
                    form = SearchForm()
        else:
            form = SearchForm()
            
        deleted = self.request.GET.get('deleted')
            
        extra_context = {
            'search':search,
            'query': query,
            'form': form,
            'deleted' : deleted,
        }
    
        return render_to_response('search/search_embedded.html', extra_context)
