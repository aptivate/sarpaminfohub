from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
import sarpaminfohub.infohub.views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('sarpaminfohub.infohub.views',
    url(r'^$', view='search', name='search'),
    url(r'formulation/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)', 
        view=sarpaminfohub.infohub.views.formulation,
        name='formulation-by-id'),
    url(r'formulation_products/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)',
        view='formulation_products', name='formulation_products'),
    url(r'suppliers/(?P<supplier_id>\d+)/(?P<backend_name>[a-z]*)',
        view=sarpaminfohub.infohub.views.supplier_catalogue,
        name='suppliers'),
    url(r'product/(?P<product_name>.+)$',
        view=sarpaminfohub.infohub.views.product_page,
        name='product-page'),
)
