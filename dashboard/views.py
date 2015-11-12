from django.shortcuts import render
from models import errorLog
import datetime
from django.http import HttpResponse, HttpResponseRedirect,Http404, JsonResponse
from django.template import RequestContext, loader
from django.utils import timezone
import collections
from django.db.models import Count
from models import errorLogTime
from startupshot.models import MattecProd,startUpShot
from inspection.models import passFailByPart, passFailInspection, rangeTestByPart, rangeInspection, textRecordByPart, \
    textInspection
from production_and_mold_history.models import ProductionHistory
from django.core import serializers
from collections import Counter, OrderedDict
from django.shortcuts import render
# Create your views here.
import json


def view_errorLog(request):
    if errorLogTime.objects.first():
        n_days = errorLogTime.objects.first().number_of_days
    else:
        n_days = 1

    dt_time = datetime.date.today()-datetime.timedelta(days=n_days)

    template = loader.get_template('dashboard/errorLog.html')
    production_errors = errorLog.objects.filter(dateCreated__gte=dt_time).order_by('-dateCreated')
    context = RequestContext(request, {
        'prodErrors':production_errors
    })
    return HttpResponse(template.render(context))

def view_jsonError(request):
    if errorLogTime.objects.first():
        n_days = errorLogTime.objects.first().number_of_days
    else:
        n_days = 1

    dt_time = datetime.date.today()-datetime.timedelta(days=n_days)

    production_errors = errorLog.objects.filter(dateCreated__gte=dt_time).order_by('-dateCreated')
    production_errors = production_errors.values_list('inspectionName',flat=True)

    count_errors = Counter(production_errors)
    sort_jawn = [(l,k) for k,l in sorted([(j,i) for i,j in count_errors.items()], reverse=True)]
    counted_errors = []
    for k,v in sort_jawn:
        counted_errors.append({'error_name':k,'error_count':v})
    str_info = json.dumps(counted_errors)
    return HttpResponse(str_info, content_type='text')

def view_errorProdLog(request):
    if errorLogTime.objects.first():
        n_days = errorLogTime.objects.first().number_of_days
    else:
        n_days = 1

    dt_time = datetime.date.today()-datetime.timedelta(days=n_days)
    template = loader.get_template('dashboard/errorProdLog.html')

    production_errors = ProductionHistory.objects.filter(dateCreated__gte=dt_time).order_by('-dateCreated')
    context = RequestContext(request, {
        'prodErrors':production_errors
    })
    return HttpResponse(template.render(context))

def view_Inspections(request):

    jobList = MattecProd.objects.all().values_list('jobNumber', flat=True)
    n=0
    resultDict = collections.OrderedDict()
    for eachJob in jobList:
        if startUpShot.objects.filter(jobNumber=eachJob).exists():
            thisSUS = startUpShot.objects.get(jobNumber=eachJob)
            pfTests = passFailByPart.objects.filter(item_Number = thisSUS.item)
            rangeTests = rangeTestByPart.objects.filter(item_Number = thisSUS.item)
            textTests = textRecordByPart.objects.filter(item_Number = thisSUS.item)

            testDict = collections.OrderedDict()
            m=0
            for each_test in pfTests:
                n_tests = passFailInspection.objects.filter(passFailTestName=each_test.testName,jobID__item = thisSUS.item).count()
                testDict[str(m)] = {'testName':each_test.testName,'n_tests':n_tests, 'req_tests': each_test.inspections_per_shift}
                m += 1

            for each_test in rangeTests:
                n_tests = rangeInspection.objects.filter(rangeTestName=each_test,jobID__item = thisSUS.item).count()
                testDict[str(m)] = {'testName':each_test.testName,'n_tests':n_tests, 'req_tests': each_test.inspections_per_shift}
                m += 1

            for each_test in textTests:
                n_tests = textInspection.objects.filter(textTestName=each_test.testName,jobID__item = thisSUS.item).count()
                testDict[str(m)] = {'testName':each_test.testName,'n_tests':n_tests, 'req_tests': each_test.inspections_per_shift}
                m += 1
            # added
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