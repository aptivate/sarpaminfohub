from django.views.generic import list_detail
from sarpaminfohub.contactlist.models import Contact
from django.conf.urls.defaults import patterns, url
from sarpaminfohub.contactlist.views import tag_search, dehex_tagged_object_list,\
    contacts_iframe, request_linked_in_profile, add_linked_in_profile

contacts_info = {
    # pylint: disable-msg = E1101
    'queryset': Contact.objects.all()
}

tags_info = {
    'queryset_or_model': Contact
}
urlpatterns = patterns('',
    url(r'^$', tag_search, name='home'),
    (r'^(?P<object_id>\d+)/$', list_detail.object_detail, contacts_info),
    (r'^tags/(?P<tag>[\w]+)/$', dehex_tagged_object_list, tags_info),
    url(r'^iframe/', contacts_iframe),
    url(r'^request_linked_in_profile/$', request_linked_in_profile),
    url(r'^request_linked_in_profile/(?P<test_data>[a-f0-9]*)', 
        request_linked_in_profile),
    url(r'^add_linked_in_profile/$', add_linked_in_profile, name='add_profile'),
    url(r'^add_linked_in_profile/(?P<test_data>[a-f0-9]*)', add_linked_in_profile, 
        name='add_profile'),
)
