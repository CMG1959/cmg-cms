from django.conf.urls import url
from CIMC.shared_router import SharedAPIRootRouter
from rest_views import EquipmentTypeViewSet, EquipmentManufacturerViewSet, EquipmentInfoViewSet
from . import views

urlpatterns = [
    ### classes
    url(r'^$', views.view_index, name='view_equipmentIndex'),

    ### types
    url(r'^(?P<equipment_class_id>[^/]+)/?$', views.view_equipment_types, name='view_equipment_types'),

    ### list filtered by type
    url(r'^view_list/(?P<equip_type_id>[^/]+)/?$', views.view_equipment, name='view_equipment'),

    ### specific equipment page
    url(r'^view_equipment/(?P<equip_name_id>[^/]+)/?$', views.view_equipment_info, name='view_equipment_info'),

    ### Go to PM page
    url(r'^view_equipment/pm_form/(?P<equip_info_id>[^/]+)/(?P<pm_type_id>[^/]+)/?$', views.view_pm_form,
        name='view_pm_form'),

    ### Go to Repair form
    url(r'^view_equipment/repair_form/(?P<equip_info_id>[^/]+)/$', views.view_repair_form, name='view_repair_form'),

    ### Go to PM Report
    url(r'^view_equipment/view_pm_report/(?P<equip_info_id>[^/]+)/$', views.view_pm_report, name='view_pm_report'),

    ### Go to Repair report
    url(r'^view_equipment/view_repair_report/(?P<equip_info_id>[^/]+)/$', views.view_repair_report,
        name='view_repair_report'),

]

router = SharedAPIRootRouter()
router.register(r'EquipmentType', EquipmentTypeViewSet)
router.register(r'EquipmentManufacturer', EquipmentManufacturerViewSet)
router.register(r'EquipmentInfo', EquipmentInfoViewSet)