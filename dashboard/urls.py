from django.conf.urls import url

from . import views

urlpatterns = [
    # View error log
    url(r'^errorLog/$', views.view_errorLog, name='view_errorLog'),
]
