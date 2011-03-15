from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sarpaminfohub.infohub.views',
                        url(r'^$', 'search', name='search'),
                        url(r'formulation/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)', 
                            'formulation', name='formulation'),
                        url(r'formulation_suppliers/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)',
                            'supplier'),
                        url(r'suppliers/(?P<supplier_id>\d+)/(?P<backend_name>[a-z]*)',
                            'supplier_catalogue'),
                        )
