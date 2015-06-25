from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render

from employee.models import employee

from models import EquipmentType, EquipmentInfo, PM, PMFreq
from forms import equipmentPMForm

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


def view_pm_form(request, equip_type, equip_name, pm_type):
    equip_info = EquipmentInfo.objects.get(equipment_type__equipment_type=equip_type, part_identifier=equip_name)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = equipmentPMForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # job_number = form.cleaned_data['job_Number']
            redirect_url = '/equipment/%s/%s' % (equip_type, equip_name)
        #     # redirect to a new URL:
            form.save()
        return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = equipmentPMForm(
            initial={'equipment_ID': equip_info.id,
                     'pm_frequency': PMFreq.objects.get(pm_frequency=pm_type)},
        )
        form.fields["employee"].queryset = employee.objects.filter(organization_name__org_name='Engineering')
        form.fields["logged_pm"].queryset = PM.objects.filter(equipment_type__equipment_type=equip_type,
                                                              pm_frequency__pm_frequency=pm_type)
    return render(request, 'equipment/forms/pm.html', {'form': form, 'equip_info': equip_info})
