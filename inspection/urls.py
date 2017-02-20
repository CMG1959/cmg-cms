from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    ### link to display active jobs
    #  cache_page(60*60)(views.view_index)
    url(r'^$', views.view_index, name='inspection_index'),
    url(r'^entry/', views.view_inspection, name='inspection_entry'),
    ### link to job report
    url(r'^JobReport/$', views.view_jobReportSearch, name='inspection_job_report'),
    ### link to item report
    url(r'^ItemReport/$',views.view_itemReportSearch, name='inspection_item_report'),
    ### link to view for job report
    url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_jobReport, name='view_jobReport'),
    ### link to view for pdf job report
    url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/pdf/$', views.view_jobReport_pdf, name='view_jobReport_pdf'),
    ### link to view for item report
    url(r'^itemReport/(?P<itemNumber>[0-9]+(.[0-9]+)+)/$', views.view_itemReport, name='view_itemReport'),
    ### link to show which inspections can be performed on a given jo
    url(r'^JobAndWorkstation$', views.view_job_detail, name='inspection_view_job_machine'),
    url(r'^job_errors/$', views.view_jsonError, name='view_jsonError'),
]
