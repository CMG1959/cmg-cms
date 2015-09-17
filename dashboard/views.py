from django.shortcuts import render
from models import errorLog
import datetime
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import RequestContext, loader
from django.utils import timezone

from startupshot.models import MattecProd,startUpShot
from inspection.models import passFailByPart, passFailInspection, rangeTestByPart, rangeInspection, textRecordByPart, \
    textInspection
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

            testDict = {}
            m=0
            for each_test in pfTests:
                n_tests = passFailInspection(passFailTestName=each_test,item_Number = thisSUS.item).count()
                testDict[str(m)] = {'testName':each_test,'n_tests':n_tests}
                m += 1

            for each_test in rangeTests:
                n_tests = rangeInspection(passFailTestName=each_test,item_Number = thisSUS.item).count()
                testDict[str(m)] = {'testName':each_test,'n_tests':n_tests}
                m += 1

            for each_test in textTests:
                n_tests = rangeInspection(passFailTestName=each_test,item_Number = thisSUS.item).count()
                testDict[str(m)] = {'testName':each_test,'n_tests':n_tests}
                m += 1

            resultDict[str(n)] = {
                'susInfo':thisSUS,
                'testDict':testDict
            }

            n+=1


    template = loader.get_template('dashboard/completedInspections.html')
    context = RequestContext(request, {'resultDict':resultDict})
    return HttpResponse(template.render(context))

def get_shift_range(shift_num):

    today = datetime.datetime.today()
    yesterday = datetime.date.today()-datetime.timedelta(1)

    if shift_num == 1:
        shift_begin = datetime.datetime(today.year,today.month,today.day,7,0)
        shift_end = datetime.datetime(today.year,today.month,today.day,15,0)
    elif shift_num == 2:
        shift_begin = datetime.datetime(today.year,today.month,today.day,15,0)
        shift_end = datetime.datetime(today.year,today.month,today.day,23,0)
    else:
        shift_begin = datetime.datetime(yesterday.year,yesterday.month,yesterday.day,23,0)
        shift_end = datetime.datetime(today.year,today.month,today.day,7,0)

    shift_begin = timezone.make_aware(shift_begin,timezone.get_current_timezone())
    shift_end = timezone.make_aware(shift_end,timezone.get_current_timezone())

    return shift_begin,shift_end