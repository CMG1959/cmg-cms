from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    # ex: /startupshot/
    url(r'^$', views.viewActive, name='start_up_shot_view_active'),
    # ex: /startupshot/view/
    url(r'^view/$', views.index, name='start_up_shot_view'),
    # ex: /startupshot/123-456789/
    url(r'^(?P<part_number>[0-9]+(-[0-9]+)+)/$', views.detailPart,
        name='start_up_shot_part_detail'),
    # ex: /startupshot/123-456789/results/
    url(r'^(?P<part_number>[0-9]+(-[0-9]+)+)/viewCreated/$',
        views.viewCreatedStartUpShot, name='start_up_shot_part_entries'),
    # ex: /startupshot/123-456789/vote/
    # url(r'^(?P<part_number>[0-9]+(-[0-9]+)+)/create/$', views.create_new_start_up_shot, name='create'),
    url(r'^create$',
        views.create_new_start_up_shot, name='start_up_shot_create_new'),
]
