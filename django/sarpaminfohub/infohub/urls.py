from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('sarpaminfohub.infohub.views',
                        url(r'^$', 'search', name='search'),
                        url(r'formulation/(?P<formulation_id>\d+)/(?P<backend_name>[a-z]*)', 
                            'formulation', name='formulation'))
