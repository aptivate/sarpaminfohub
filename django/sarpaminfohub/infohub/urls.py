from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sarpaminfohub.infohub.views',
                        url(r'^$', 'search'),
                        url(r'formulation/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)', 
                            'formulation', name='formulation'))
