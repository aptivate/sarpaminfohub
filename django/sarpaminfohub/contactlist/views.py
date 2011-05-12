from django.shortcuts import render_to_response
from tagging.views import tagged_object_list
from sarpaminfohub.contactlist.tag_searcher import TagSearcher
from sarpaminfohub.contactlist.profile_adder import ProfileAdder

def tag_search(request):
    tag_searcher = TagSearcher(request)

    return tag_searcher.search()

def request_linked_in_profile(request, testing=None):
    profile_adder = create_and_return_profile_adder(request, testing)
    
    return profile_adder.request_profile()

def add_linked_in_profile(request, testing=None):
    profile_adder = create_and_return_profile_adder(request, testing)
    
    return profile_adder.add_profile()    

def create_and_return_profile_adder(request, testing):
    if testing == "testing":
        testing = True
    else:
        testing = False
    
    profile_adder = ProfileAdder(request, testing)
    
    return profile_adder

def dehex_tagged_object_list(request, queryset_or_model=None, tag=None,
        related_tags=False, related_tag_counts=True):
        dehexed = tag.decode('hex')
        return tagged_object_list(request=request, 
            queryset_or_model=queryset_or_model, 
            tag=dehexed, related_tags=related_tags, 
            related_tag_counts=related_tag_counts)
        
def contacts_iframe(request):
    extra_context = {'iframe_url':'/contacts/', 'iframe_title':"Expert Search"}
    return render_to_response('iframe/contacts.html', extra_context)
