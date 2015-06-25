from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render

from models import EquipmentType, EquipmentInfo, PM

# Create your views here.

def view_index(request):
    equipmentTypes = EquipmentType.objects.all()

    # active_parts = Production.objects.filter(inProduction=True).select_related('item')

    template = loader.get_template('equipment/index.html')
    context = RequestContext(request, {
        'equipmentTypes': equipmentTypes,
        })
    return HttpResponse(template.render(context))


def view_equipment(request,equip_type):
    equipmentTypes = EquipmentInfo.objects.filter(equipment_type__equipment_type=equip_type)


    # active_parts = Production.objects.filter(inProduction=True).select_related('item')

    template = loader.get_template('equipment/equipment_index.html')
    context = RequestContext(request, {
        'equipmentTypes': equipmentTypes,
        })
    return HttpResponse(template.render(context))

def view_equipment_info(request,equip_type,equip_name):
    equip_info = EquipmentInfo.objects.get(equipment_type__equipment_type=equip_type,part_identifier=equip_name)
    PMinfo = PM.objects.filter(equipment_type__equipment_type=equip_type).select_related()
    print PMinfo

    template = loader.get_template('equipment/equipment_info.html')
    context = RequestContext(request, {
        'equip_info': equip_info,
        'PM_info': PMinfo,
        })
    return HttpResponse(template.render(context))