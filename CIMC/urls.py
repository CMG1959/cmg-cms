"""CIMC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from shared_router import SharedAPIRootRouter
from home.views import index

def api_urls():
    from importlib import import_module
    for app in settings.INSTALLED_APPS:
        try:
            import_module(app + '.urls')
        except (ImportError, AttributeError):
            pass
    return SharedAPIRootRouter.shared_router.urls

urlpatterns = [
                  url(r'^$', index),
                  url(r'^StartupShot/', include('startupshot.urls')),
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^inspection/', include('inspection.urls')),
                  url(r'^inspection_v2/', include('ins.urls')),
                  url(r'^equipment/', include('equipment.urls')),
                  url(r'^dashboard/',include('dashboard.urls')),
                  url(r'^production_and_mold_history/', include('production_and_mold_history.urls')),
                  url(r'^accounts/login/$', auth_views.login),
                  url(r'^mobile/', include('mobile_views.urls')),
                  url(r'^logout$', auth_views.logout, {'next_page': '/'}),
                  url(r'^API/', include(api_urls())),
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
