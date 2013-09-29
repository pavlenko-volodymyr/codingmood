from django.conf.urls import patterns, url

from .views import BadgeUserList


urlpatterns = patterns('',
    url(r'^$', BadgeUserList.as_view(), name='list'),
)
