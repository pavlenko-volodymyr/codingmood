from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'', include('common.urls')),
    url(r'^badges/', include('badges.urls', namespace='badges')),

    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

