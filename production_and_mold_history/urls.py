from django.conf.urls import url

from . import views

urlpatterns = [
    ### link to view equipment types
    url(r'^$', views.view_index, name='view_PHL_index'),
    ### link to create production history log item
    url(r'^production$', views.view_phl_form, name='view_phl_form'),
    ### link to view specific production history log
    url(r'^production/(?P<jobNo>[0-9]+(.[0-9]+)+)$', views.view_specific_phl_form, name='view_specific_phl_form'),
    ### link to create mold history log item
    url(r'^mold$', views.view_mold_form, name='view_mold_form'),
    ### link to view specific mold history log
    url(r'^mold/(?P<moldNo>[0-9]+(.[0-9]+)+)$', views.view_specific_mold_form, name='view_specific_mold_form'),
    ### link to view production history log
    url(r'^production_report$', views.view_phl_report_search, name='view_phl_report_search'),
    ### link to view mold report
    url(r'^mold_report$', views.view_mold_report_search, name='view_mold_report_search'),
    ### link to view specific production history log
    url(r'^production_report/(?P<jobNo>[0-9]+(.[0-9]+)+)$', views.view_phl_report, name='view_phl_report'),
    ### link to view specific mold report
    url(r'^mold_report/(?P<moldNo>[0-9]+(-[0-9]+)+)$', views.view_mold_report, name='view_mold_report'),
]
