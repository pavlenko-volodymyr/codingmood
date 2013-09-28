from django.conf.urls import patterns, url

from .views import BadgesList


urlpatterns = patterns('',
    url(r'^$', BadgesList.as_view(), name='list'),
)
