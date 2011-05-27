from django.shortcuts import render_to_response
from tagging.views import tagged_object_list
from sarpaminfohub.contactlist.tag_searcher import TagSearcher
from sarpaminfohub.contactlist.profile_adder import ProfileAdder
from sarpaminfohub.contactlist.profile_deleter import ProfileDeleter
from sarpaminfohub.contactlist.models import Contact
from django.views.generic import list_detail
from sarpaminfohub.contactlist.batch_updater import BatchUpdater

def tag_search(request):
    tag_searcher = TagSearcher(request)

    return tag_searcher.search()

def add_linked_in_profile(request, test_data=None):
    profile_adder = ProfileAdder(request, test_data)
    
    return profile_adder.get_authorization()

def authorized_add(request, test_data=None):
    profile_adder = ProfileAdder(request, test_data)
    
    return profile_adder.add_profile()    

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

def delete_linked_in_profile(request, test_data=None):
    profile_deleter = ProfileDeleter(request, test_data)
    
    return profile_deleter.get_authorization()

def authorized_delete(request, test_data=None):
    profile_deleter = ProfileDeleter(request, test_data)
    
    return profile_deleter.delete_profile()

def contact_detail(request, object_id):
    new_contact = request.GET.get('new_contact')
    
    # pylint: disable-msg = E1101
    queryset = Contact.objects.all()
    extra_context = {'new_contact' : new_contact}
    
    return list_detail.object_detail(request, queryset, object_id, \
                                     extra_context=extra_context)

def update_linked_in_profiles(request, test_data=None):
    if request.method == "GET":
        return render_to_response("contactlist/batch_update.html")

    batch_updater = BatchUpdater(request, test_data)
    
    return batch_updater.update()
