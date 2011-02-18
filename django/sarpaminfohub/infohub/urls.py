from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sarpaminfohub.infohub.views',
                        url(r'^$', 'search_form', name='search.html'))
