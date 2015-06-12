from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /startupshot/
    url(r'^$', views.index, name='index'),
    # ex: /startupshot/123-456789/
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.detailJob, name='detailJob'),
    # # ex: /startupshot/123-456789/results/
    # url(r'^(?P<part_number>[0-9]+(-[0-9]+)+)/viewCreated/$', views.viewCreatedStartUpShot, name='view'),
    # # ex: /startupshot/123-456789/vote/
    # # url(r'^(?P<part_number>[0-9]+(-[0-9]+)+)/create/$', views.createNewStartUpShot, name='create'),
    # url(r'^create/$', views.createNewStartUpShot, name='create'),
]