from django.conf.urls import url

from . import views

urlpatterns = [
    ### link to display active jobs
    url(r'^$', views.view_index, name='index'),
    ### link to job report
    url(r'^jobReport/$', views.view_jobReportSearch, name='view_jobReportSearch'),
    ### link to item report
    url(r'^itemReport/$', views.view_itemReportSearch, name='view_itemReportSearch'),
    ### link to view for job report
    url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_jobReport, name='view_jobReport'),
    ### link to view for item report
    url(r'^itemReport/(?P<itemNumber>[0-9]+(.[0-9]+)+)/$', views.view_itemReport, name='view_itemReport'),
    ### link to show which inspections can be performed on a given job
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_detailJob, name='view_detailJob'),
    ### link to visual inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/visual/$', views.view_visualInspection, name='view_visualInspection'),
    ### link to weight inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/weight/$', views.view_weightInspection, name='view_weightInspection'),
]