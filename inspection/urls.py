from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /startupshot/
    url(r'^$', views.index, name='index'),
    # ex: /startupshot/123-456789/
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.detailJob, name='detailJob'),
    # # ex: /startupshot/123-456789/results/
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/visual/$', views.visualInspection, name='visualInspection'),
    # # ex: /startupshot/123-456789/vote/
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/weight/$', views.weightInspection, name='weightInspection'),

]