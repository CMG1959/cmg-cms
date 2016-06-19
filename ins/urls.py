from django.conf.urls import url

from . import views

urlpatterns = [
    ### link to display active jobs
    url(r'^$', views.view_index, name='index'),
    url(r'^view', views.view_job, name='view_job'),
    # url(r'^entry/', views.view_inspection, name='inspection_entry'),
    # ### link to job report
    # url(r'^jobReport/$', views.view_jobReportSearch, name='view_jobReportSearch'),
    # ### link to item report
    # url(r'^itemReport/$', views.view_itemReportSearch, name='view_itemReportSearch'),
    # ### link to view for job report
    # url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_jobReport, name='view_jobReport'),
    # ### link to view for pdf job report
    # url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/pdf/$', views.view_jobReport_pdf, name='view_jobReport_pdf'),
    # ### link to view for item report
    # url(r'^itemReport/(?P<itemNumber>[0-9]+(.[0-9]+)+)/$', views.view_itemReport, name='view_itemReport'),
    # ### link to show which inspections can be performed on a given jo
    # url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_detailJob, name='view_detailJob'),
    # url(r'^job_errors/$', views.view_jsonError, name='view_jsonError'),
]
