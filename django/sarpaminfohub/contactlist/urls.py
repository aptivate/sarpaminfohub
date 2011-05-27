from sarpaminfohub.contactlist.models import Contact
from django.conf.urls.defaults import patterns, url
from sarpaminfohub.contactlist.views import tag_search, dehex_tagged_object_list,\
    contacts_iframe, add_linked_in_profile,\
    delete_linked_in_profile, authorized_delete, authorized_add, contact_detail,\
    update_linked_in_profiles

tags_info = {
    'queryset_or_model': Contact
}
urlpatterns = patterns('',
    url(r'^$', tag_search, name='home'),
    (r'^(?P<object_id>\d+)/$', contact_detail),
    (r'^tags/(?P<tag>[\w]+)/$', dehex_tagged_object_list, tags_info),
    url(r'^iframe/', contacts_iframe),

    url(r'^add_linked_in_profile/$', add_linked_in_profile),
    url(r'^add_linked_in_profile/test/(?P<test_data>[a-f0-9]*)', 
        add_linked_in_profile),
    url(r'^authorized_add/$', authorized_add, name='authorized_add'),
    url(r'^authorized_add/test/(?P<test_data>[a-f0-9]*)', authorized_add, 
        name='authorized_add'),

    url(r'^delete_linked_in_profile/$', delete_linked_in_profile),
    url(r'^delete_linked_in_profile/test/(?P<test_data>[a-f0-9]*)', 
        delete_linked_in_profile),
    url(r'^authorized_delete/$', authorized_delete, name='authorized_delete'),
    url(r'^authorized_delete/test/(?P<test_data>[a-f0-9]*)', authorized_delete, 
        name='authorized_delete'),
    url(r'^batch_update/$', update_linked_in_profiles),
    url(r'^batch_update/test/(?P<test_data>[a-f0-9]*)', update_linked_in_profiles),
)
