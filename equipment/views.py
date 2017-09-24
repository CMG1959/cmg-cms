from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.template.loader import render_to_string

from employee.models import Employees

from models import EquipmentType, EquipmentInfo, PM, PMFreq, EquipmentPM, EquipmentRepair, EquipmentClass
from forms import equipmentPMForm, equipmentRepairForm
from tree import Tree, Node


# Create your views here.
@login_required
def view_index(request):
    # equipmentTypes = EquipmentType.objects.order_by('equipment_type').all()
    equipment_classes = EquipmentClass.objects.all().exclude(group_name='unknown / unspecified').order_by('group_name')

    template = loader.get_template('equipment/index.html')
    context = RequestContext(request, {
        'equipment_classes': equipment_classes,
    })
    return HttpResponse(template.render(context))

@login_required
def view_equipment_types(request, equipment_class_id):
    equipment_types = EquipmentType.objects.filter(equipment_class_id =equipment_class_id).order_by('equipment_type')
    template = loader.get_template('equipment/equipment_types.html')
    context = RequestContext(request, {
        # 'equipmentTypes': equipmentTypes,
        # 'equipment_class' : equipment_class_id,
        'equipment_types': equipment_types,
    })
    return HttpResponse(template.render(context))


@login_required
def view_equipment(request, equip_type_id):
    equipmentTypes = EquipmentInfo.objects.filter(equipment_type_id=equip_type_id,
                                                  # equipment_type__equipment_class_id=equipment_class_id,
                                                  is_active=True).order_by('part_identifier')

    template = loader.get_template('equipment/equipment_index.html')
    context = RequestContext(request, {
        # 'equipment_class_id': equipment_class_id,
        'equipmentTypes': equipmentTypes,
    })
    return HttpResponse(template.render(context))


@login_required
def view_equipment_info(request, equip_name_id):
    equip_info = EquipmentInfo.objects.get(id=equip_name_id)

    PMinfo = PM.objects.filter(equipment_type=equip_info.equipment_type).values('pm_frequency__pm_frequency','pm_frequency__id').distinct()

    template = loader.get_template('equipment/equipment_info.html')
    context = RequestContext(request, {
        # 'equipment_class_id': equipment_class_id,
        'equip_info': equip_info,
        'PM_info': PMinfo,
    })
    return HttpResponse(template.render(context))


@login_required
def view_pm_form(request, equip_info_id, pm_type_id):
    equip_info = EquipmentInfo.objects.get(id=equip_info_id)

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
                redirect_url = '/equipment/view_equipment/view_pm_report/%s/' % (equip_info_id)

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

        lastPM = EquipmentPM.objects.filter(equipment_ID__id=equip_info_id).order_by('-dateCreated')[:3]

        #PMinfo = PM.objects.get(id=pm_type_id)

        form = equipmentPMForm(
            initial={'equipment_ID': equip_info.id,
                     'pm_frequency': PMFreq.objects.get(id=pm_type_id).id},
        )

        form.fields["pm_frequency"].queryset = PMFreq.objects.filter(id=pm_type_id)
        form.fields["logged_pm"].queryset = PM.objects.filter(equipment_type=equip_info.equipment_type,
                                                              pm_frequency_id=pm_type_id)

        context_dic = {'form': form, 'equip_info': equip_info, 'pm_id': '#id_logged_pm'}
        if lastPM:
            context_dic['PM_info'] = lastPM

    return render(request, 'equipment/forms/pm.html', context_dic)


@login_required
def view_pm_report(request, equip_info_id):
    equip_info = EquipmentInfo.objects.get(id=equip_info_id)
    pm_report = EquipmentPM.objects.filter(equipment_ID=equip_info).order_by('dateCreated').reverse()

    template = loader.get_template('equipment/reports/equipment_pm_report.html')
    context = RequestContext(request, {
        'equip_info': equip_info,
        'PM_info': pm_report,
    })
    return HttpResponse(template.render(context))


@login_required
def view_repair_form(request, equip_info_id):
    equip_info = EquipmentInfo.objects.get(id = equip_info_id)

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
                redirect_url = '/equipment/view_equipment/view_repair_report/%s/' % (equip_info_id)
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
def view_repair_report(request, equip_info_id):
    equip_info = EquipmentInfo.objects.get(id=equip_info_id)
    repair_report = EquipmentRepair.objects.filter(equipment_ID=equip_info_id).order_by('dateCreated').reverse()

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

class EquipmentReportBase(TemplateView):
    template_name = 'equipment/reports/report.html'

    def get_context_data(self, **kwargs):
        equipment_id = self.request.GET.get('equipment_id')
        equipment_information = EquipmentInfo.objects.get(id=equipment_id)
        context = super(EquipmentReportBase, self).get_context_data(**kwargs)
        context['equipment_information'] = equipment_information
        context['equipment_id'] = equipment_id
        return context


def get_tree(request):
    equipment_id = request.GET.get('equipment_id')



    node_cover_page = Node('Cover Page', 'cover_page',
                           reverse('equipment_api_device', kwargs={'equipment_id':equipment_id}), equipment_id)

    node_repair = Node('Repair', 'repair',
                           reverse('equipment_api_repair', kwargs={'equipment_id':equipment_id}), equipment_id)

    node_pm = Node('PM', 'pm',
                           reverse('equipment_api_pm', kwargs={'equipment_id':equipment_id}), equipment_id)

    tree = [x.to_jstree() for x in [node_cover_page, node_pm, node_repair]]

    return JsonResponse(tree, safe=False)


def api_device(request, equipment_id):
    equipment_information = EquipmentInfo.objects.get(id=equipment_id)
    data = {
        'equipment_type': equipment_information.equipment_type.equipment_type,
        'alias': equipment_information.part_identifier,
        'manufacturer_name': equipment_information.manufacturer_name.manufacturer_name,
        'serial_number': equipment_information.serial_number,
        'date_of_manufacture': equipment_information.date_of_manufacture
    }

    device_html = render_to_string('equipment/reports/modules/cover_page.html', {
        'cover_page': [(k.replace('_',' ').title(), v) for k,v in data.iteritems()]
    })

    return_dict = {
        'html': device_html,
        'data': None
    }
    return JsonResponse(return_dict)


def api_preventative_maintenance(request, equipment_id):
    key_value_pairs = [
        ('employee__EmpLMName', 'employee'),
        ('Date_Performed', 'date_performed'),
        ('pm_frequency__pm_frequency', 'pm_frequency'),
        ('logged_pm__pm_item', 'pm_tasks'),
        ('comments', 'comments'),
    ]

    output_list = []
    for row in EquipmentPM.objects.filter(
            equipment_ID=equipment_id).values(*[x[0] for x in key_value_pairs]).\
            order_by('Date_Performed').reverse():
        output_list.append([row[x[0]] for x in key_value_pairs])

    return_dict = {
        'html': get_data_table_html('Preventative Maintenance',
                                    [x[1].replace('_',' ').title() for x in
                                     key_value_pairs]),
        'data': output_list
    }

    return JsonResponse(return_dict)

def api_repair(request, equipment_id):

    key_value_pairs = [
        ('employee__EmpLMName', 'employee'),
        ('Date_Performed', 'date_performed'),
        ('po_num', 'po'),
        ('part_supplier__supplier_name', 'supplier'),
        ('part_name', 'part_name'),
        ('part_number', 'part_number'),
        ('part_cost', 'part_cost'),
        ('part_quantity', 'part_quantity'),
        ('comments', 'comments')
    ]

    output_list = []
    for row in EquipmentRepair.objects.filter(
        equipment_ID=equipment_id).values(*[x[0] for x in key_value_pairs]).\
        order_by('Date_Performed').reverse():
        output_list.append([row[x[0]] for x in key_value_pairs])

    return_dict = {
        'html': get_data_table_html('Preventative Maintenance',
                                    [x[1].replace('_',' ').title() for x in
                                     key_value_pairs]),
        'data' : output_list
    }

    return JsonResponse(return_dict)


def get_data_table_html(caption, headers):
    device_html = render_to_string('equipment/reports/modules/data_table_base.html',
                                   {
                                       'caption': caption,
                                       'table_headers': headers
                                   })
    return device_html