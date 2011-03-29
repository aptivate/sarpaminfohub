from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from sarpaminfohub.contactlist.forms import SearchForm
from linkedin import linkedin
from django.conf import settings
from django.core.cache import cache
def tag_search(request):
    query = None
    search = False
    if request.method == 'POST':
        form = SearchForm(request.POST)
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
    extra_context = {
        'search':search,
        'query': query,
        'form': form,
    }

    return render_to_response('search/search_embedded.html', extra_context)

def linked_in(request):
    api = linkedin.LinkedIn(*settings.LI_LIST)
    api.requestToken()
    if request.GET.get('oauth_verifier',False) and request.GET.get('oauth_token',False):
        verifier = request.GET.get('oauth_verifier')
        request_token = request.GET.get('oauth_token')
        request_token_secret = cache.get(request_token)
        if api.accessToken(request_token=request_token,request_token_secret=request_token_secret,verifier=verifier):
            profile = api.GetProfile(fields=["first-name","last-name","honors","specialties","positions","public-profile-url","summary","location","phone-numbers"])
            extra_context = {
                'given_name':profile.first_name,
                'family_name':profile.last_name,
                'public_url':profile.public_url,
                'notes':profile.summary,
                'tags':profile.specialties,
                'position':profile.positions[0].title,
                'organization':profile.positions[0].company,
                'address':profile.location
            }
            return render_to_response('search/linked_in.html', extra_context)
    cache.set(api.request_token,api.request_token_secret,30*60)
    extra_context = {
        'auth_url':api.getAuthorizeURL()
    }
    return render_to_response('search/linked_in.html', extra_context)