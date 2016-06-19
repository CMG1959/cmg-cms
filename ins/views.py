from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.
from startupshot.models import MattecProd
from part.models import Part
from molds.models import Mold

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

    job_in_mattec = MattecProd.objects.get(jobNumber=job_number)
    part_info = Part.objects.get(item_Number=job_in_mattec.itemNo)
    mold_info = Mold.objects.get(mold_number=job_in_mattec.moldNumber)


    template = loader.get_template('ins/view.html')
    context = RequestContext(request, {
        'part_info': part_info,
        'mold_info': mold_info
        # 'pf_inspectionType': pf_inspectionType,
        # 'range_inspectionType': range_inspectionType,
        # 'text_inspectionType': text_inspectionType,
        # 'int_inspectionType': int_inspectionType,
        # 'float_inspectionType': float_inspectionType
    })
    return HttpResponse(template.render(context))
