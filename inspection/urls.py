from django.conf.urls import url

from . import views

urlpatterns = [
    ### link to display active jobs
    url(r'^$', views.view_index, name='index'),
    ### link to job report
    url(r'^jobReport/$', views.view_jobReportSearch, name='view_jobReportSearch'),
    ### link to item report
    url(r'^itemReport/$', views.view_itemReportSearch, name='view_itemReportSearch'),
    ### link to view for job report
    url(r'^jobReport/(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_jobReport, name='view_jobReport'),
    ### link to view for item report
    url(r'^itemReport/(?P<itemNumber>[0-9]+(.[0-9]+)+)/$', views.view_itemReport, name='view_itemReport'),
    ### link to show which inspections can be performed on a given job
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/$', views.view_detailJob, name='view_detailJob'),
    ### link to visual inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/visual/$', views.view_visualInspection, name='view_visualInspection'),
    ### link to part weight inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/part_weight/$', views.view_partWeightInspection,
        name='view_partWeightInspection'),
    ### link to weight inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/shot_weight/$', views.view_shotWeightInspection,
        name='view_shotWeightInspection'),
    ### link to outside diameter form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/outside_diameter/$', views.view_outsideDiameterInspection,
        name='view_outsideDiameterInspection'),
    ### link to volume inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/volume_test/$', views.view_volumeInspectionForm,
        name='view_volumeInspectionForm'),
    ### link to neck diameter form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/neck_diameter/$', views.view_neckDiameterForm,
        name='view_neckDiameterForm'),
    ### link to assembly inspection form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/assembly_test/$', views.view_assemblyInspectionForm,
        name='view_assemblyInspectionForm'),
    ### link to carton temp form
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/carton_temp/$', views.view_cartonTempForm,
        name='view_cartonTempForm'),
    ### link to vision system inspection
    url(r'^(?P<jobNumber>[0-9]+(.[0-9]+)+)/vision_system/$', views.view_visionInspectionForm,
        name='view_visionInspectionForm'),
]
