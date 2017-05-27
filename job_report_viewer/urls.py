from django.conf.urls import url

from job_report_viewer import views

urlpatterns = [
    ### link to display active jobs
    #  cache_page(60*60)(views.view_index)
    url(r'^$', view=views.JobReportBase.as_view(), name=''),
    url(r'/Tree$', view=views.get_tree, name='tree'),
    url(r'/CoverPage$', view=views.cover_page, name='cover_page'),
    url(r'/DataTable$', view=views.data_table_view, name='data_table'),
    url(r'/DataTableSummary$', view=views.data_table_summary_view, name='data_table_summary'),
    url(r'/Plots$', view=views.plots, name='plots')
]
