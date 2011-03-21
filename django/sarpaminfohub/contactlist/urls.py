from django.conf.urls.defaults import *
from django.views.generic import list_detail
from contactlist.models import Contact

contacts_info = {
    'queryset': Contact.objects.all()
}
urlpatterns = patterns('',
    (r'^$', include('haystack.urls')),
    (r'^(?P<object_id>\d+)/$', list_detail.object_detail, contacts_info)
)