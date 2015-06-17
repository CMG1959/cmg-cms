from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /startupshot/
    url(r'^$', views.view_index, name='index'),
    # ex: /startupshot/123-456789/
    url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_jobReport, name='view_jobReport'),
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_detailJob, name='view_detailJob'),
    # # ex: /startupshot/123-456789/results/
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/visual/$', views.view_visualInspection, name='view_visualInspection'),
    # # ex: /startupshot/123-456789/vote/
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/weight/$', views.view_weightInspection, name='view_weightInspection'),

]