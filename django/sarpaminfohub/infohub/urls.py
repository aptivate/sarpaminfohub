from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from infohub.views import formulation

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('sarpaminfohub.infohub.views',
                        url(r'^$', view='search', name='search'),
                        url(r'formulation/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)', 
                            view=formulation, name='formulation-by-id'),
                        url(r'formulation_products/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)',
                            view='formulation_products', name='formulation_products'),
                        url(r'suppliers/(?P<supplier_id>\d+)/(?P<backend_name>[a-z]*)',
                            view='supplier_catalogue', name='suppliers'),
                        )
