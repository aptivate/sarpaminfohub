from django.views.generic import list_detail
from tagging.views import tagged_object_list
from sarpaminfohub.contactlist.models import Contact
from django.conf.urls.defaults import patterns
from sarpaminfohub.contactlist.views import tag_search

contacts_info = {
    'queryset': Contact.objects.all()
}

tags_info = {
    'queryset_or_model': Contact
}
urlpatterns = patterns('',
    (r'^$', tag_search),
    (r'^(?P<object_id>\d+)/$', list_detail.object_detail, contacts_info),
    (r'^tags/(?P<tag>[-\w]+)/$', tagged_object_list, tags_info),
)