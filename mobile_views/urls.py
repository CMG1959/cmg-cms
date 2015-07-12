from django.conf.urls import url

from . import views

urlpatterns = [
    ### link to display active jobs
    url(r'^$', views.view_weightStatus, name='index'),
]
