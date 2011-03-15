from django.conf.urls.defaults import patterns, include
from django.conf.urls.defaults import handler500, handler404 #@UnusedImport
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sarpaminfohub/', include('sarpaminfohub.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT }),
    (r'^search/', include('haystack.urls')),
    (r'', include('sarpaminfohub.infohub.urls')),
)
