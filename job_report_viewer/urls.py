from django.conf.urls import url

from job_report_viewer import views

urlpatterns = [
    ### link to display active jobs
    #  cache_page(60*60)(views.view_index)
    url(r'^$', view=views.JobReportBase.as_view(), name=''),
    url(r'CoverPage$', view=views.CoverPage.as_view(), name='cover_page'),
    url(r'DataTable$', view=views.data_table, name=''),
    url(r'Plots$', view=views.plots, name='')
]
