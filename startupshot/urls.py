from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    # ex: /startupshot/
    url(r'^$', cache_page(60*60)(views.viewActive), name='viewActive'),
    # ex: /startupshot/view/
    url(r'^view/$', cache_page(60*60)(views.index), name='viewIndex'),
    # ex: /startupshot/123-456789/
    url(r'^(?P<part_number>[0-9]+(-[0-9]+)+)/$', views.detailPart, name='detail'),
    # ex: /startupshot/123-456789/results/
    url(r'^(?P<part_number>[0-9]+(-[0-9]+)+)/viewCreated/$', views.viewCreatedStartUpShot, name='view'),
    # ex: /startupshot/123-456789/vote/
    # url(r'^(?P<part_number>[0-9]+(-[0-9]+)+)/create/$', views.createNewStartUpShot, name='create'),
    url(r'^create/(?P<jobNo>[0-9]+(.[0-9]+)+)/$', views.createNewStartUpShot, name='create'),
]
