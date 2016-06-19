import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.
from startupshot.models import MattecProd
from part.models import Part
from molds.models import Mold
from .models import *


@login_required
def view_index(request):
    activeInMattec = MattecProd.objects.order_by('machNo').all()

    template = loader.get_template('ins/index.html')
    context = RequestContext(request, {
        'active_parts': activeInMattec,
    })
    return HttpResponse(template.render(context))


def view_job(request):
    job_number = request.GET.get('job_number', '-1')

    context = {}

    job_in_mattec = MattecProd.objects.get(jobNumber=job_number)
    part_info = Part.objects.get(item_Number=job_in_mattec.itemNo)
    mold_info = Mold.objects.get(mold_number=job_in_mattec.moldNumber)

    mach_type = get_machine_type(job_in_mattec.machNo)

    inspection_set = ['A']
    if mach_type in ['IMM', 'ISBM']:
        if StaticInspectionPart.objects.filter(part_number=part_info.item_Number,
                                               inspection_group__product_type='M').exists() or \
                StaticInspectionGroup.objects.filter(product_type='M', apply_type='All').exists():
                inspection_set.append('M')
    elif mach_type not in ['Fail', 'M']:
        inspection_set.append(mach_type)
    else:
        pass

    inspections = StaticInspectionGroup.objects.filter(product_type__in=inspection_set)

    template = loader.get_template('ins/view.html')
    context = RequestContext(request, {
        'job_number': job_number,
        'part_info': part_info,
        'mold_info': mold_info,
        'inspections': inspections
        # 'pf_inspectionType': pf_inspectionType,
        # 'range_inspectionType': range_inspectionType,
        # 'text_inspectionType': text_inspectionType,
        # 'int_inspectionType': int_inspectionType,
        # 'float_inspectionType': float_inspectionType
    })
    return HttpResponse(template.render(context))

def view_record_inspection(request):
    job_number = request.GET.get('job_number', '-1')
    inspection_id = request.GET.get('inspection_id', '-1')

    job_in_mattec = MattecProd.objects.get(jobNumber=job_number)
    part_info = Part.objects.get(item_Number=job_in_mattec.itemNo)
    mold_info = Mold.objects.get(mold_number=job_in_mattec.moldNumber)


    if request.method == 'POST':
        pass
    else:
        inspection_regime = StaticInspectionGroup.objects.get(id=inspection_id)

        template = loader.get_template('ins/record_inspection.html')
        context = RequestContext(request, {
            'job_number': job_number,
            'part_info': part_info,
            'mold_info': mold_info,
            'inspection_regime': inspection_regime
        })
        return HttpResponse(template.render(context))


def get_machine_type(machine_alias):
    match = re.search('(?P<machine_type>\D+)(?P<machine_num>\d+)', machine_alias)
    try:
        return match.group('machine_type')
    except Exception as e:
        return 'Fail'
