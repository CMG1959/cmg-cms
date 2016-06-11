from django.conf.urls import url

from . import views

urlpatterns = [
    ### link to display active jobs
    url(r'^$', views.view_index, name='index'),
    url(r'^entry/', views.view_inspection, name='inspection_entry'),
    ### link to job report
    url(r'^jobReport/$', views.view_jobReportSearch, name='view_jobReportSearch'),
    ### link to item report
    url(r'^itemReport/$', views.view_itemReportSearch, name='view_itemReportSearch'),
    ### link to view for job report
    url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_jobReport, name='view_jobReport'),
    ### link to view for pdf job report
    url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/pdf/$', views.view_jobReport_pdf, name='view_jobReport_pdf'),
    ### link to view for item report
    url(r'^itemReport/(?P<itemNumber>[0-9]+(.[0-9]+)+)/$', views.view_itemReport, name='view_itemReport'),
    ### link to show which inspections can be performed on a given job
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_detailJob, name='view_detailJob'),
    ### link to visual inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/pf/(?P<inspectionName>[^/]+)/$', views.view_pfInspection, name='view_pfInspection'),
    ### link to view range inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/rangeInspection/(?P<inspectionName>[^/]+)/$', views.view_rangeInspection, name='view_rangeInspection'),
    ### link to view text inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/textInspection/(?P<inspectionName>[^/]+)/$', views.view_textInspection, name='view_textInspection'),
    ### link to view integer inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/IntegerInspection/(?P<inspectionName>[^/]+)/$', views.view_IntegerInspection, name='view_IntegerInspection'),
    ### link to view float inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/FloatInspection/(?P<inspectionName>[^/]+)/$', views.view_FloatInspection, name='view_FloatInspection'),
    ### Get a json dict with error information
    url(r'^job_errors/$', views.view_jsonError, name='view_jsonError'),
]
