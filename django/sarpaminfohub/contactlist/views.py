from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response, redirect
from sarpaminfohub.contactlist.forms import SearchForm
from django.conf import settings
from django.core.cache import cache
from sarpaminfohub.contactlist.custom_fields import COUNTRY_DICT
from django.core.exceptions import ObjectDoesNotExist
from linkedin import linkedin
from sarpaminfohub.contactlist.models import Contact
from django.core.urlresolvers import reverse

def tag_search(request):
    query = None
    search = False
    
    url = request.build_absolute_uri(reverse('home'))
    
    api_key = settings.LINKED_IN_API_KEY
    secret_key = settings.LINKED_IN_SECRET_KEY
    
    api = linkedin.LinkedIn(api_key, secret_key, url)
    api.requestToken()
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
    elif request.method == 'GET':
        form = SearchForm()
        if request.GET.get('oauth_verifier',False) and request.GET.get('oauth_token',False):
            verifier = request.GET.get('oauth_verifier')
            request_token = request.GET.get('oauth_token')
            request_token_secret = cache.get(request_token)
            if not request_token_secret:
                return redirect('/contacts/')
            if api.accessToken(request_token=request_token,request_token_secret=request_token_secret,verifier=verifier):
                profile = api.GetProfile(fields=["first-name","last-name","honors","specialties","positions","public-profile-url","summary","location","phone-numbers"])
                contact_data = {
                    'given_name':profile.first_name,
                    'family_name':profile.last_name,
                    'linked_in_url':profile.public_url,
                    'note':profile.summary,
                    'tags':profile.specialties,
                    'role':profile.positions[0].title,
                    'organization':profile.positions[0].company,
                    'address_line_1':profile.location.split(',')[0],
                    'country':COUNTRY_DICT.get(profile.location.split(',')[1],""),
                    'linked_in_approval':True,
                }
                try:
                    contact = Contact.objects.get(linked_in_url=profile.public_url)
                    contact.given_name = contact_data['given_name']
                    contact.family_name = contact_data['family_name']
                    contact.linked_in_url = contact_data['linked_in_url']
                    contact.note = contact_data['note']
                    contact.tags = contact_data['tags']
                    contact.role = contact_data['role']
                    contact.organization = contact_data['organization']
                    contact.address_line_1 = contact_data['address_line_1']
                    contact.country = contact_data['country']
                    contact.linked_in_approval = contact_data['linked_in_approval']
                except ObjectDoesNotExist:
                    contact = Contact.objects.create(**contact_data)
                contact.save()
                cache.delete(request_token)
                extra_context = {
                    'contact_url':contact.get_absolute_url()
                }

                return render_to_response('contactlist/closeme.html',extra_context)

        cache.set(api.request_token,api.request_token_secret,30*60)
    else:
        form = SearchForm()
    extra_context = {
        'auth_url':api.getAuthorizeURL(),
        'search':search,
        'query': query,
        'form': form,
    }

    return render_to_response('search/search_embedded.html', extra_context)