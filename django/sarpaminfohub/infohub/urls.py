from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.generic.simple import direct_to_template
import sarpaminfohub.infohub.views
from sarpaminfohub.infohub.views import pricing_iframe

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('sarpaminfohub.infohub.views',
    (r'^$', direct_to_template, {
        "template" : "license.html",
    }, 'licence'),
    url(r'search/$', view='search', name='search'),
    url(r'formulation/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)', 
        view=sarpaminfohub.infohub.views.formulation,
        name='formulation-by-id'),
    url(r'formulation_products/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)',
        view='formulation_products', name='formulation_products'),
    url(r'suppliers/(?P<supplier_id>\d+)/(?P<backend_name>[a-z]*)',
        view=sarpaminfohub.infohub.views.supplier_catalogue,
        name='suppliers'),
    url(r'product/(?P<product_id>\d+)$',
        view=sarpaminfohub.infohub.views.product_page,
        name='product-page'),
    url(r'iframe/', view=pricing_iframe),
)
