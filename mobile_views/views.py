from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.db.models import Avg, Max, Min, StdDev, F

### bring in models
from startupshot.models import MattecProd, startUpShot
from part.models import Part, PartInspection
from inspection.models import partWeightInspection, shotWeightInspection

# Create your views here.



def view_weightStatus(request):
    ### get list of active parts and order by machine
    active_list = MattecProd.objects.values_list('itemNo', 'machNo', 'jobNumber').order_by('machNo')

    ### Create dictionary of active parts, TMM part weight, startup part weight and some statistics
    active_parts = {}
    idx = 0
    for each_part in active_list:
        idx_id = '%i' % (idx)
        active_parts[idx_id] = {}
        active_parts[idx_id]['partID'] = each_part[0]
        active_parts[idx_id]['machID'] = each_part[1]
        quick_part = Part.objects.filter(item_Number=each_part[0])
        if quick_part.exists():
            active_parts[idx_id]['tmmWeight'] = quick_part[0].exp_part_weight
        else:
            active_parts[idx_id]['tmmWeight'] = 0

        quick_part = startUpShot.objects.filter(jobNumber=each_part[2])
        if quick_part.exists():
            active_parts[idx_id]['startWeight'] = quick_part[0].shotWeight / quick_part[0].activeCavities
        else:
            active_parts[idx_id]['startWeight'] = 0

        quick_part = PartInspection.objects.filter(item_Number__item_Number=each_part[0])
        if quick_part.exists():
            if quick_part[0].part_weight_inspection:
                avg_weight = partWeightInspection.objects.filter(jobID__jobNumber=each_part[2]).aggregate(Avg('partWeight'))
                active_parts[idx_id]['avgPartWeight'] = avg_weight['avg_weight']

            elif quick_part[0].shot_weight_inspection:
                avg_weight = shotWeightInspection.objects.filter(jobID__jobNumber=each_part[2]).aggregate(Avg(F('shotWeight')/F('activeCavities')))
                active_parts[idx_id]['avgPartWeight'] = avg_weight['avg_weight']

        idx += 1
    ### Create a dictionary with
    print active_parts

    # active_parts = Production.objects.filter(inProduction=True).select_related('item')

    template = loader.get_template('mobile_views/partWeight.html')
    context = RequestContext(request, {
        'active_parts': active_parts,

    })
    return HttpResponse(template.render(context))
