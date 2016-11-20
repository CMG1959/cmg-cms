from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    # View error log
    url(r'^errorLog/$', cache_page(60*10)(views.view_errorLog), name='view_errorLog'),
    # View error log
    url(r'^errorProdLog/$', cache_page(60*10)(views.view_errorProdLog), name='view_errorProdLog'),
    # Get json jawn
    url(r'^jsonError/$', cache_page(60*10)(views.view_jsonError), name='view_jsonError'),
    # View error log
    url(r'^inspectionLog/$',cache_page(60*10)(views.view_Inspections), name='view_inspectionLog'),
    url(r'^Production_Summary/$', views.ProductionSummary.as_view(), name ='order_list_json')
    ]
