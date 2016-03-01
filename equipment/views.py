from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from employee.models import Employees

from models import EquipmentType, EquipmentInfo, PM, PMFreq, EquipmentPM, EquipmentRepair, EquipmentClass
from forms import equipmentPMForm, equipmentRepairForm

# Create your views here.
@login_required
def view_index(request):
    # equipmentTypes = EquipmentType.objects.order_by('equipment_type').all()
    equipment_classes = EquipmentClass.objects.order_by('group_name').all()
    # active_parts = Production.objects.filter(inProduction=True).select_related('item')

    template = loader.get_template('equipment/index.html')
    context = RequestContext(request, {
        # 'equipmentTypes': equipmentTypes,
        'equipment_classes': equipment_classes,
    })
    return HttpResponse(template.render(context))

@login_required
def view_equipment_types(request, equipment_class_id):
    equipment_types = EquipmentType.objects.filter(equipment_class_id =equipment_class_id).order_by('equipment_type')
    template = loader.get_template('equipment/equipment_types.html')
    context = RequestContext(request, {
        # 'equipmentTypes': equipmentTypes,
        'equipment_class' : equipment_class_id,
        'equipment_types': equipment_types,
    })
    return HttpResponse(template.render(context))


@login_required
def view_equipment(request, equipment_class_id, equip_type):
    equipmentTypes = EquipmentInfo.objects.filter(equipment_type__equipment_type=equip_type,
                                                  equipment_type__equipment_class_id=equipment_class_id,
                                                  is_active=True).order_by('part_identifier')


    # active_parts = Production.objects.filter(inProduction=True).select_related('item')



    template = loader.get_template('equipment/equipment_index.html')
    context = RequestContext(request, {
        'equipment_class_id': equipment_class_id,
        'equipmentTypes': equipmentTypes,
    })
    return HttpResponse(template.render(context))


@login_required
def view_equipment_info(request, equipment_class_id, equip_type, equip_name):
    equip_info = EquipmentInfo.objects.get(equipment_type__equipment_type=equip_type,
                                           equipment_type__equipment_class_id=equipment_class_id,
                                           part_identifier=equip_name)
    PMinfo = PM.objects.filter(equipment_type__equipment_type=equip_type).values_list('pm_frequency__pm_frequency',
                                                                                      flat=True).distinct()

    template = loader.get_template('equipment/equipment_info.html')
    context = RequestContext(request, {
        'equipment_class_id': equipment_class_id,
        'equip_info': equip_info,
        'PM_info': PMinfo,
    })
    return HttpResponse(template.render(context))


@login_required
def view_pm_form(request, equipment_class_id, equip_type, equip_name, pm_type):
    equip_info = EquipmentInfo.objects.get(equipment_type__equipment_type=equip_type,
                                           equipment_type__equipment_class_id=equipment_class_id,
                                           part_identifier=equip_name)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = equipmentPMForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                # process the data in form.cleaned_data as required
                # job_number = form.cleaned_data['job_Number']
                redirect_url = '/equipment/%s/%s' % (equip_type, equip_name)
                #     # redirect to a new URL:
                    # save the data
                my_form = form.save(commit=False)
                my_form.employee = is_user
                my_form.save()
                form.save_m2m()

                return HttpResponseRedirect(redirect_url)

            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))

    # if a GET (or any other method) we'll create a blank form
    else:

        lastPM = EquipmentPM.objects.filter(equipment_ID__part_identifier=equip_name,
                                            equipment_ID__equipment_type__equipment_type=equip_type).order_by('-dateCreated')[:3]

        form = equipmentPMForm(
            initial={'equipment_ID': equip_info.id,
                     'pm_frequency': PMFreq.objects.get(pm_frequency=pm_type).id},
        )
        form.fields["pm_frequency"].queryset = PMFreq.objects.filter(pm_frequency=pm_type)
        form.fields["logged_pm"].queryset = PM.objects.filter(equipment_type__equipment_type=equip_type,
                                                              pm_frequency__pm_frequency=pm_type)

        context_dic = {'form': form, 'equip_info': equip_info, 'pm_id': '#id_logged_pm'}
        if lastPM:
            context_dic['PM_info'] = lastPM

    return render(request, 'equipment/forms/pm.html', context_dic)


@login_required
def view_pm_report(request, equipment_class_id, equip_type, equip_name):
    equip_info = EquipmentInfo.objects.get(equipment_type__equipment_type=equip_type,
                                           equipment_type__equipment_class_id=equipment_class_id,
                                           part_identifier=equip_name)
    pm_report = EquipmentPM.objects.filter(equipment_ID__part_identifier=equip_name).order_by('dateCreated').reverse()

    template = loader.get_template('equipment/reports/equipment_pm_report.html')
    context = RequestContext(request, {
        'equip_info': equip_info,
        'PM_info': pm_report,
    })
    return HttpResponse(template.render(context))


@login_required
def view_repair_form(request, equipment_class_id, equip_type, equip_name):
    equip_info = EquipmentInfo.objects.get(equipment_type__equipment_type=equip_type,
                                           equipment_type__equipment_class_id=equipment_class_id,
                                           part_identifier=equip_name)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = equipmentRepairForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                # process the data in form.cleaned_data as required
                # job_number = form.cleaned_data['job_Number']
                redirect_url = '/equipment/%s/%s' % (equip_type, equip_name)
                #     # redirect to a new URL:
                my_form = form.save(commit=False)
                my_form.employee = is_user
                my_form.save()

                return HttpResponseRedirect(redirect_url)

            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = equipmentRepairForm(
            initial={'equipment_ID': equip_info.id,
                     },
        )

    return render(request, 'equipment/forms/repair.html', {'form': form, 'equip_info': equip_info})


@login_required
def view_repair_report(request, equipment_class_id,  equip_type, equip_name):
    equip_info = EquipmentInfo.objects.get(equipment_type__equipment_type=equip_type,
                                           equipment_type__equipment_class_id=equipment_class_id,
                                           part_identifier=equip_name)
    repair_report = EquipmentRepair.objects.filter(equipment_ID__part_identifier=equip_name).order_by('dateCreated').reverse()

    template = loader.get_template('equipment/reports/equipment_repair_report.html')
    context = RequestContext(request, {
        'equip_info': equip_info,
        'repair_info': repair_report,
    })
    return HttpResponse(template.render(context))

def get_user_info(man_num):
    try:
        this_user = Employees.objects.get(EmpNum=man_num)
    except Employees.DoesNotExist:
        this_user = None
    return this_user
    