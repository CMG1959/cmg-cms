from django.conf.urls import url

from . import views

urlpatterns = [
    # View error log
    url(r'^errorLog/$', views.view_errorLog, name='view_errorLog'),
    # Get json jawn
    url(r'^jsonError/$', views.view_jsonError, name='view_jsonError'),
    # View error log
    url(r'^inspectionLog/$', views.view_Inspections, name='view_inspectionLog'),
]
