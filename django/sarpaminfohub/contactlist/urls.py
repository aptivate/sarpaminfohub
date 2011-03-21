from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'^search/', include('haystack.urls')),
)