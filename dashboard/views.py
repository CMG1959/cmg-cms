from django.shortcuts import render
from models import errorLog
import datetime
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import RequestContext, loader

from startupshot.models import MattecProd,startUpShot
from inspection.models import passFailByPart, rangeTestByPart, textRecordByPart
from django.shortcuts import render
# Create your views here.

def view_errorLog(request):
    dt_yesterday = datetime.date.today()-datetime.timedelta(days=1)
    production_errors = errorLog.objects.filter(dateCreated__gte=dt_yesterday).order_by('-dateCreated')
    template = loader.get_template('dashboard/errorLog.html')
    context = RequestContext(request, {
        'prodErrors':production_errors
    })
    return HttpResponse(template.render(context))



def view_Inspections(request):

    jobList = MattecProd.objects.all().values_list('jobNumber', flat=True)
    n=0
    resultDict = {}
    for eachJob in jobList:
        if startUpShot.objects.filter(jobNumber=eachJob).exists():
            thisSUS = startUpShot.objects.get(jobNumber=eachJob)
            pfTests = passFailByPart.objects.filter(item_Number = thisSUS.item)
            rangeTests = rangeTestByPart.objects.filter(item_Number = thisSUS.item)
            textTests = textRecordByPart.objects.filter(item_Number = thisSUS.item)

            resultDict[str(n)] = {
                'susInfo':thisSUS,
                'pfTests':pfTests,
                'rangeTests':rangeTests,
                'textTests':textTests
            }

            n+=1


    template = loader.get_template('dashboard/completedInspections.html')
    context = RequestContext(request, {'resultDict':resultDict})
    return HttpResponse(template.render(context))
