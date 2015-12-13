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
from inspection.models import *
from production_and_mold_history.models import ProductionHistory
from django.core import serializers
from collections import Counter, OrderedDict
from django.shortcuts import render
# Create your views here.
import json
from natsort import natsorted

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


    production_errors = production_errors.values_list('machNo',flat=True)

    count_errors = Counter(production_errors)
    sort_jawn = [(l,k) for k,l in sorted([(j,i) for i,j in count_errors.items()], reverse=True)]
    counted_mach_errors = []
    for k,v in sort_jawn:
        counted_mach_errors.append({'mach_name':k,'mach_count':v})

    my_dict = {'mach':counted_mach_errors, 'errors': counted_errors}

    str_info = json.dumps(my_dict)
    return HttpResponse(str_info, content_type='text')

def view_errorProdLog(request):
    if errorLogTime.objects.first():
        n_days = errorLogTime.objects.first().number_of_days
    else:
        n_days = 1

    dt_time = datetime.date.today()-datetime.timedelta(days=n_days)
    template = loader.get_template('dashboard/errorProdLog.html')

    production_errors = ProductionHistory.objects.filter(dateCreated__gte=dt_time).order_by('-dateCreated')
    prod_errors = []
    for each_error in production_errors:
        susInfo = startUpShot.objects.filter(jobNumber = each_error.jobNumber)[0]
        if susInfo:
            machNo = susInfo.machNo
            item_Description = susInfo.item.item_Description
        else:
            machNo = 'N/A'
            item_Description = 'N/A'
        prod_errors.append({
            'dateCreated': each_error.dateCreated,
            'inspectorName': each_error.inspectorName,
            'machNo': machNo,
            'item_Description': item_Description,
            'descEvent': each_error.descEvent
        })

    context = RequestContext(request, {
        'prodErrors':prod_errors
    })
    return HttpResponse(template.render(context))

def view_Inspections(request):

    jobList = MattecProd.objects.all()
    n=0
    resultDict = collections.OrderedDict()
    for eachJob in jobList:
            pfTests = passFailByPart.objects.filter(item_Number__item_Number = eachJob.itemNo)
            rangeTests = rangeTestByPart.objects.filter(item_Number__item_Number = eachJob.itemNo)
            textTests = textRecordByPart.objects.filter(item_Number__item_Number = eachJob.itemNo)
            intTests = IntegerRecordByPart.objects.filter(item_Number__item_Number = eachJob.itemNo)
            floatTests = FloatRecordByPart.objects.filter(item_Number__item_Number = eachJob.itemNo)
            testDict = collections.OrderedDict()
            m=0
            for each_test in pfTests:
                n_tests = passFailInspection.objects.filter(passFailTestName=each_test.testName, jobID__jobNumber = eachJob.jobNumber).count()
                testDict[str(m)] = {'testName':each_test.testName,'n_tests':n_tests, 'req_tests': each_test.inspections_per_shift}
                m += 1

            for each_test in rangeTests:
                n_tests = rangeInspection.objects.filter(rangeTestName=each_test, jobID__jobNumber = eachJob.jobNumber).count()
                testDict[str(m)] = {'testName':each_test.testName,'n_tests':n_tests, 'req_tests': each_test.inspections_per_shift}
                m += 1

            for each_test in textTests:
                n_tests = textInspection.objects.filter(textTestName=each_test.testName, jobID__jobNumber = eachJob.jobNumber).count()
                testDict[str(m)] = {'testName':each_test.testName,'n_tests':n_tests, 'req_tests': each_test.inspections_per_shift}
                m += 1


            for each_test in intTests:
                n_tests = IntegerInspection.objects.filter(integerTestName=each_test.testName, jobID__jobNumber = eachJob.jobNumber).count()
                testDict[str(m)] = {'testName':each_test.testName,'n_tests':n_tests, 'req_tests': each_test.inspections_per_shift}
                m += 1

            for each_test in floatTests:
                n_tests = FloatInspection.objects.filter(floatTestName=each_test.testName, jobID__jobNumber = eachJob.jobNumber).count()
                testDict[str(m)] = {'testName':each_test.testName,'n_tests':n_tests, 'req_tests': each_test.inspections_per_shift}
                m += 1


            # added
            resultDict['%s - %s' % (eachJob.machNo, eachJob.jobNumber)] = {
                'mattecInfo':eachJob,
                'testDict':testDict
            }

            n+=1
    my_order = OrderedDict()
    for each_key in natsorted(resultDict.keys()):
        my_order[each_key] = resultDict[each_key]

    template = loader.get_template('dashboard/completedInspections.html')
    context = RequestContext(request, {'resultDict':my_order})
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