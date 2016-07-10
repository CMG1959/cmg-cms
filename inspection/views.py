# Create your views here.
import numpy as np
import re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.db.models import Avg, Max, Min, StdDev
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from models import *
from dashboard.models import errorLog
from equipment.models import EquipmentInfo
from part.models import Part
from startupshot.models import startUpShot, MattecProd
from employee.models import Employees, EmployeeAtWorkstation
from molds.models import Mold, PartIdentifier
from production_and_mold_history.models import ProductionHistory
from forms import jobReportSearch, itemReportSearch, \
    build_inspection_fields, PassFailIns, RangeIns, TextIns, FloatIns#, IntIns

from reports import JobReport
import collections
import json
import datetime
from decimal import Decimal


######################################
#
#  Section for generating indexes, etc
#
######################################

@login_required
def view_index(request):
    activeInMattec = MattecProd.objects.order_by('machNo').all()

    template = loader.get_template('inspection/index.html')
    context = RequestContext(request, {
        'active_parts': activeInMattec,
    })
    return HttpResponse(template.render(context))


@login_required
def view_detailJob(request, jobNumber):
    jobNumber = str(jobNumber).strip()

    try:
        active_job = startUpShot.objects.filter(jobNumber=jobNumber).last()

        if not active_job:
            raise Http404(str(active_job))
        # if  PartInspection object hasnt be created, make it now.
        checkPartInspection(active_job.item)
        # better go ahead and take care of the Mold now


        pf_inspectionType = passFailByPart.objects.filter(item_Number__item_Number=active_job.item,
                                                          testName__isSystemInspection=False)
        range_inspectionType = numericTestByPart.objects.filter(item_Number__item_Number=active_job.item,
                                                                testName__isSystemInspection=False)
        text_inspectionType = textRecordByPart.objects.filter(item_Number__item_Number=active_job.item,
                                                              testName__isSystemInspection=False)
        # int_inspectionType = IntegerRecordByPart.objects.filter(item_Number__item_Number=active_job.item,
        #                                                         testName__isSystemInspection=False)
        float_inspectionType = RangeRecordByPart.objects.filter(item_Number__item_Number=active_job.item,
                                                                testName__isSystemInspection=False)
        template = loader.get_template('inspection/detailJob.html')
        context = RequestContext(request, {
            'active_job': active_job,
            'pf_inspectionType': pf_inspectionType,
            'range_inspectionType': range_inspectionType,
            'text_inspectionType': text_inspectionType,
            # 'int_inspectionType': int_inspectionType,
            'float_inspectionType': float_inspectionType
        })
        return HttpResponse(template.render(context))

    except Exception as e:
        try:
            MattecInfo = MattecProd.objects.get(jobNumber=jobNumber)
            if str(MattecInfo.machNo).strip() not in ['FAS01', 'OFP01']:
                redir_url = '/startupshot/create/%s/' % jobNumber
                return HttpResponseRedirect(redir_url)
            else:
                raise Http404(str(e))
        except Exception as e1:
            raise Http404('Do not see the job number if MATTEC. %s' % str(e1))

######################################
#
#  Section for generating forms
#
######################################

@login_required
def view_inspection(request):
    job_number_id = int(request.GET.get('job_number_id', -1))
    inspection_type = request.GET.get('inspection_type', 'N/A')
    inspection_name_id = int(request.GET.get('inspection_name_id', -1))

    if request.method == 'POST':

        # try:
        active_job = startUpShot.objects.filter(id=job_number_id).last()
        context_dict = {'active_job': active_job,
                        'head_cav_id': '#id_headCavID'}
        range_info = None

        if inspection_type == 'Pass-Fail':
            test_info = passFailTest.objects.get(id=inspection_name_id)
            form = PassFailIns(request.POST)

        elif inspection_type == 'Range':
            test_info = numericTest.objects.get(id=inspection_name_id)
            range_info = numericTestByPart.objects.get(testName_id=inspection_name_id,
                                                       item_Number_id=active_job.item_id)
            form = RangeIns(request.POST)

        elif inspection_type == 'Text':
            test_info = textRecord.objects.get(id=inspection_name_id)
            form = TextIns(request.POST)

        # elif inspection_type == 'Integer':
        #     test_info = IntegerRecord.objects.get(id=inspection_name_id)
        #     form = IntIns(request.POST)

        elif inspection_type == 'Float':
            test_info = RangeRecord.objects.get(id=inspection_name_id)
            form = FloatIns(request.POST)

        else:
            raise Http404("Inspection Type Does Not Exist")

        if form.is_valid():
            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                my_form = form.save(commit=False)
                my_form.jobID_id = job_number_id
                my_form.inspectorName = is_user
                my_form.Passed_Partial = False
                if not my_form.headCavID:
                    my_form.headCavID = '-'

                if inspection_type == 'Pass-Fail':
                    my_form.passFailTestName_id = inspection_name_id
                    my_form.save()
                    form.save_m2m()
                    if my_form.inspectionResult == False and len(my_form.defectType.all()) < 1:
                        pf_test_unknown_reason, created = passFailTestCriteria.objects.get_or_create(
                            testName_id=inspection_name_id,
                            passFail='Other / Unknown')
                        my_form.defectType.add(pf_test_unknown_reason)

                elif inspection_type == 'Range':
                    my_form.rangeTestName_id = range_info.id
                    if ((my_form.numVal >= range_info.rangeMin) and (my_form.numVal <= range_info.rangeMax)):
                        inspectionResult = True
                    else:
                        inspectionResult = False
                    my_form.inspectionResult = inspectionResult

                elif inspection_type == 'Text':
                    my_form.textTestName_id = inspection_name_id

                elif inspection_type == 'Integer':
                    my_form.integerTestName_id = inspection_name_id

                elif inspection_type == 'Float':
                    my_form.floatTestName_id = inspection_name_id
                else:
                    pass

                my_form.save()

                set_new_mach_op(active_job.jobNumber, my_form.machineOperator)
                checkFormForLog(my_form, inspectionType=inspection_type,
                                inspectionName=test_info.testName,
                                activeJob=active_job, rangeInfo=range_info)

                redirect_url = '/inspection/%s/' % (active_job.jobNumber)
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))

                # except Exception as e:
                #     raise Http404(str(e))

    else:
        try:
            active_job = startUpShot.objects.filter(id=job_number_id).last()
            context_dict = {'active_job': active_job,
                            'head_cav_id': '#id_headCavID'}

            if inspection_type == 'Pass-Fail':
                test_info = passFailTest.objects.get(id=inspection_name_id)
                form = PassFailIns()
                context_dict_add = {
                    'use_checkbox2': True,
                    'id_check': '#id_inspectionResult',
                    'idSelect': '#id_defectType',
                    'idSelect2': '#id_headCavID',
                }

            elif inspection_type == 'Range':
                test_info = numericTest.objects.get(id=inspection_name_id)
                range_info = numericTestByPart.objects.get(testName_id=inspection_name_id,
                                                           item_Number_id=active_job.item_id)
                form = RangeIns()

                context_dict_add = {
                    'use_checkbox': True,
                    'id_check': '#id_isFullShot',
                    'idSelect': '#id_headCavID',
                    'use_minmax': True,
                    'num_id': '#id_numVal',
                    'min_val': range_info.rangeMin,
                    'max_val': range_info.rangeMax,
                    'id_result': '#id_inspectionResult',
                }


            elif inspection_type == 'Text':
                test_info = textRecord.objects.get(id=inspection_name_id)
                form = TextIns()
                context_dict_add = {
                    'use_checkbox': True,
                    'id_check': '#id_inspectionResult',
                    'idSelect': '#id_headCavID',
                }


            # elif inspection_type == 'Integer':
            #     test_info = IntegerRecord.objects.get(id=inspection_name_id)
            #     form = IntIns()
            #     context_dict_add = {
            #         'use_checkbox': True,
            #         'id_check': '#id_inspectionResult',
            #         'idSelect': '#id_headCavID',
            #     }


            elif inspection_type == 'Float':
                test_info = RangeRecord.objects.get(id=inspection_name_id)
                form = FloatIns()
                context_dict_add = {
                    'use_checkbox': True,
                    'id_check': '#id_inspectionResult',
                    'idSelect': '#id_headCavID',
                }


            else:
                raise Http404("Inspection Type Does Not Exist")

            machine_operator = get_previous_mach_op(job_number=active_job.jobNumber)
            if machine_operator:
                context_dict.update({'machine_operator': machine_operator.id})

            headCavID_choices, defectType_choices = build_inspection_fields(job_id=job_number_id,
                                                                            inspection_type=inspection_type,
                                                                            inspection_id=inspection_name_id,
                                                                            man_num=request.user.webappemployee.EmpNum)
            form.fields["headCavID"].widget.choices = headCavID_choices

            if defectType_choices:
                form.fields["defectType"].choices = defectType_choices

            form.fields["machineOperator"].queryset = \
                Employees.objects.filter(StatusActive=True, IsOpStaff=True).order_by('EmpShift').order_by('EmpLName')

            context_dict.update({'form_title': test_info.testName,
                                 'form': form})
            context_dict.update(context_dict_add)

            template = loader.get_template('inspection/forms/genInspection.html')
            context = RequestContext(request, context_dict)
            return HttpResponse(template.render(context))

        except Exception as e:
            raise Http404(str(e))


######################################
#
#  Section for generating reports
#
######################################


@login_required
def view_jobReportSearch(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = jobReportSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            report_type = form.cleaned_data['report_type']
            job_number = form.cleaned_data['job_Number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            if report_type == 'htmlReport':
                context_dic = createJobReportDict(job_number, date_from=date_from, date_to=date_to)
                template = loader.get_template('inspection/reports/jobReport.html')
                context = RequestContext(request, context_dic)
                return HttpResponse(template.render(context))
            elif report_type == 'htmlReport_noplot':
                context_dic = createJobReportDict(job_number, date_from=date_from, date_to=date_to)
                template = loader.get_template('inspection/reports/jobReport_noplot.html')
                context = RequestContext(request, context_dic)
                return HttpResponse(template.render(context))
            else:
                if startUpShot.objects.filter(jobNumber=job_number).exists():
                    my_report = JobReport(job_number=job_number, date_from=date_from, date_to=date_to)
                    return my_report.get_report()
                else:
                    return render(request, '404.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = jobReportSearch()

    return render(request, 'inspection/searchForms/jobReportSearch.html', {'form': form})


@login_required
def view_itemReportSearch(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = itemReportSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            item_number = form.cleaned_data['item_Number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            context_dic = {}
            context_dic['partDict'] = createItemReportDict(item_number, date_from=date_from, date_to=date_to)
            context_dic.update({'list_many': True})

            template = loader.get_template('inspection/reports/partReport.html')
            context = RequestContext(request, context_dic)
            return HttpResponse(template.render(context))


    # if a GET (or any other method) we'll create a blank form
    else:
        form = itemReportSearch()

    return render(request, 'inspection/searchForms/itemReportSearch.html', {'form': form})


@login_required
def view_itemReport(request, itemNumber):
    context_dict = {}
    context_dict = createItemReportDict(itemNumber)
    context_dict.update({'list_many': True})

    template = loader.get_template('inspection/reports/partReport.html')
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))


@login_required
def view_jobReport(request, jobNumber):
    context_dic = createJobReportDict(jobNumber)
    template = loader.get_template('inspection/reports/jobReport.html')
    context = RequestContext(request, context_dic)
    return HttpResponse(template.render(context))


@login_required
def view_jobReport_pdf(request, jobNumber):
    if startUpShot.objects.filter(jobNumber=jobNumber).exists():
        my_report = JobReport(job_number=jobNumber)
        return my_report.get_report()
    else:
        return render(request, '404.html')


####### Section for generating data for plots ###########
def view_jsonError(job_number, date_from, date_to):
    date_from, date_to = createDateRange(date_from, date_to)
    pf = passFailInspection.objects.filter(jobID__jobNumber=job_number, dateCreated__range=(date_from, date_to),
                                           inspectionResult=0)
    ri = numericInspection.objects.filter(jobID__jobNumber=job_number, dateCreated__range=(date_from, date_to),
                                          inspectionResult=0)
    ti = textInspection.objects.filter(jobID__jobNumber=job_number, dateCreated__range=(date_from, date_to),
                                       inspectionResult=0)

    if (not ri.exists()) and (not pf.exists()):
        no_errors = True
    else:
        no_errors = False

    production_errors = []
    for eachpf in pf:
        production_errors.append(eachpf.passFailTestName.testName)
    for eachri in ri:
        production_errors.append(eachri.rangeTestName.testName.testName)
    for eachti in ti:
        production_errors.append(eachti.textTestName.testName)

    count_errors = collections.Counter(production_errors)
    sort_jawn = [(l, k) for k, l in sorted([(j, i) for i, j in count_errors.items()], reverse=True)]
    counted_errors = []
    for k, v in sort_jawn:
        counted_errors.append({'error_name': k, 'error_count': v})

    if no_errors:
        return None
    else:
        return json.dumps(counted_errors, ensure_ascii=False).encode('utf8')


####### Helper functions ###########

def createItemReportDict(itemNumber, date_from=None, date_to=None):
    collapse_list = []

    date_from1, date_to1 = createDateRange(date_from=date_from, date_to=date_to)

    jobList = startUpShot.objects.filter(item__item_Number=itemNumber, dateCreated__range=(date_from1, date_to1))
    susList = jobList
    jobList = jobList.values_list('jobNumber', flat=True)

    pf_inspectionType = passFailByPart.objects.filter(item_Number__item_Number=itemNumber)
    rangeTests = numericTestByPart.objects.filter(item_Number__item_Number=itemNumber)
    textTests = textRecordByPart.objects.filter(item_Number__item_Number=itemNumber)

    partDict = {'pf': {}, 'numericTest': {}, 'activeJob': susList}

    k = 0
    for eachInspection1 in pf_inspectionType:
        eachInspection = eachInspection1.testName
        partDict['pf'][eachInspection] = collections.OrderedDict()
        thisInspection = passFailInspection.objects.filter(passFailTestName__testName=eachInspection,
                                                           dateCreated__range=(date_from1, date_to1))
        n = 0

        key = 'pf' + str(k)
        collapse_list.append('#' + key)
        partDict['pf'][eachInspection]['html_id'] = key
        k = k + 1

        for eachJob in jobList:
            partDict['pf'][eachInspection]['inspectionName'] = eachInspection
            partDict['pf'][eachInspection][n] = {}
            thisInspectionbyJob = thisInspection.filter(jobID__jobNumber=eachJob).order_by('-dateCreated')
            partDict['pf'][eachInspection][n]['jobID'] = eachJob
            partDict['pf'][eachInspection][n].update(createPFStats(thisInspectionbyJob))
            n += 1

        partDict['pf'][eachInspection][n] = {}
        partDict['pf'][eachInspection][n]['jobID'] = 'Total'
        partDict['pf'][eachInspection][n].update(
            createPFStats(thisInspection.filter(jobID__item__item_Number=itemNumber)))

    k = 0
    for eachInspection1 in rangeTests:

        eachInspection = eachInspection1.testName.testName
        partDict['numericTest'][eachInspection] = collections.OrderedDict()
        partDict['numericTest'][eachInspection]['inspectionName'] = eachInspection

        thisInspection = numericInspection.objects.filter(rangeTestName__testName__testName=eachInspection,
                                                          dateCreated__range=(date_from1, date_to1)).order_by(
            '-dateCreated')
        n = 0

        key = 'rt' + str(k)
        collapse_list.append('#' + key)
        partDict['numericTest'][eachInspection]['html_id'] = key
        k = k + 1

        totalRangeList = []
        for eachJob in jobList:
            partDict['numericTest'][eachInspection][n] = {}
            partDict['numericTest'][eachInspection][n]['jobID'] = eachJob

            thisInspectionbyJob = thisInspection.filter(jobID__jobNumber=eachJob).order_by('-dateCreated')
            active_job = startUpShot.objects.filter(jobNumber=eachJob).select_related('item')

            rangeList = []
            for eachShot in thisInspectionbyJob:
                # if its a full shot and we do not want to report the raw data (take average)
                if ((eachShot.isFullShot) and (not eachInspection1.testName.calcAvg)):
                    rangeList.append(eachShot.numVal / active_job[0].activeCavities)
                    totalRangeList.append(rangeList[-1])
                else:
                    rangeList.append(eachShot.numVal)
                    totalRangeList.append(rangeList[-1])

            partDict['numericTest'][eachInspection][n]['rangeStats'] = calcRangeStats(rangeList)
            n += 1

        partDict['numericTest'][eachInspection][n] = {'jobID': 'Total',
                                                    'rangeStats': calcRangeStats(totalRangeList)}

    n = 0
    partDict['textTests'] = collections.OrderedDict()
    for eachTextTest in textTests:
        key = 'tt' + str(n)
        collapse_list.append('#' + key)
        partDict['textTests'][n] = {
            'html_id': key,
            'testName': eachTextTest.testName,
            'textDict': textInspection.objects.filter( \
                    textTestName__testName=eachTextTest.testName,
                    jobID__item__item_Number=itemNumber)
        }

        n += 1

    partDict['phl'] = []
    for eaJob in eachJob:
        partDict['phl'].extend(ProductionHistory.objects.filter(jobNumber=eaJob).values('dateCreated', 'jobNumber',
                                                                                        'inspectorName__EmpLMName',
                                                                                        'descEvent').order_by(
            '-dateCreated'))

    partDict['phl'] = [item for sublist in partDict['phl'] for item in sublist]  # change?
    partDict['useJobNo'] = True

    collapse_list.append('#phl')

    partDict.update({'collapse_list': collapse_list})

    partDict.update({
        'headerDict': {
            'companyName': 'Custom Molders Group',
            'reportName': 'Part Report',
            'documentName': 'Part Number: %s' % itemNumber
        },
        'list_many': True
    })

    return partDict


def createJobReportDict(jobNumber, date_from=None, date_to=None):
    collapse_list = []
    context_dic = {}
    context_dic['plot_info'] = view_jsonError(job_number=jobNumber, date_from=date_from, date_to=date_to)

    date_from, date_to = createDateRange(date_from=date_from, date_to=date_to)

    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')

    context_dic['active_job'] = active_job

    # Job number 6 and 9 should be QA and
    context_dic['phl'] = ProductionHistory.objects.filter(jobNumber=jobNumber,
                                                          dateCreated__range=(date_from, date_to),
                                                          inspectorName__IsQCStaff=True).values('dateCreated',
                                                                                                'jobNumber',
                                                                                                'inspectorName__EmpLMName',
                                                                                                'descEvent').order_by(
        '-dateCreated')

    pf_inspectionType = passFailByPart.objects.filter(item_Number__item_Number=active_job[0].item)
    rangeTests = numericTestByPart.objects.filter(item_Number__item_Number=active_job[0].item)
    textTests = textRecordByPart.objects.filter(item_Number__item_Number=active_job[0].item)

    context_dic['pf'] = {}
    context_dic['pfSummary'] = {}
    n = 0
    for each_pf_inspection in pf_inspectionType:
        key = 'pf' + str(n)
        collapse_list.append('#' + key)
        context_dic['pf'][key] = passFailInspection.objects.filter(
            passFailTestName__testName=each_pf_inspection.testName.testName,
            jobID__jobNumber=jobNumber,
            dateCreated__range=(date_from, date_to)).order_by('-dateCreated')
        context_dic['pfSummary'][key] = {}
        context_dic['pfSummary'][key]['pfName'] = each_pf_inspection.testName.testName
        context_dic['pfSummary'][key].update(createPFStats(context_dic['pf'][key]))
        n += 1

    n = 0
    context_dic['rangeTests'] = {}
    context_dic['rangeTestSummary'] = {}
    for each_range_inspection in rangeTests:
        key = 'rt' + str(n)
        collapse_list.append('#' + key)
        context_dic['rangeTests'][key] = numericInspection.objects.filter(
            rangeTestName__testName=each_range_inspection.testName,
            jobID__jobNumber=jobNumber,
            dateCreated__range=(date_from, date_to)).order_by('-dateCreated')
        context_dic['rangeTestSummary'][key] = {}
        context_dic['rangeTestSummary'][key]['rangeName'] = each_range_inspection.testName.testName

        rangeList = []
        for eachShot in context_dic['rangeTests'][key]:
            if ((eachShot.isFullShot) and (not each_range_inspection.testName.calcAvg)):
                rangeList.append(eachShot.numVal / active_job[0].activeCavities)
            else:
                rangeList.append(eachShot.numVal)

        context_dic['rangeTestSummary'][key]['rangeStats'] = calcRangeStats(rangeList)

        n += 1

    n = 0
    context_dic['textTests'] = {}
    for eachTextTest in textTests:
        key = 'tt' + str(n)
        collapse_list.append('#' + key)
        context_dic['textTests'][key] = {
            'testName': eachTextTest.testName,
            'textDict': textInspection.objects.filter( \
                    textTestName__testName=eachTextTest.testName, jobID__jobNumber=jobNumber).order_by('-dateCreated')
        }

        n += 1

    context_dic['phl'] = ProductionHistory.objects.filter(jobNumber=jobNumber).values('dateCreated', 'jobNumber',
                                                                                      'inspectorName__EmpLMName',
                                                                                      'descEvent').order_by(
        '-dateCreated')
    collapse_list.append('#' + 'phl')

    context_dic.update({
        'headerDict': {
            'companyName': 'Custom Molders Group',
            'reportName': 'Job Report',
            'documentName': 'Job Number: %s' % (jobNumber)
        },
        'list_many': True
    })

    context_dic.update({'collapse_list': collapse_list})
    return context_dic


######################
#
# Helper functions
#
######################

def createDateRange(date_from=None, date_to=None):
    if date_from is None:
        date_from = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
        date_from = timezone.make_aware(date_from, timezone.get_current_timezone())

    if date_to is None:
        date_to = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        date_to = timezone.make_aware(date_to, timezone.get_current_timezone())

    return (date_from, date_to)


def presetStandardFields(my_form, jobID, test_type, test_name):
    # this will preset machine and qa fields
    ### Filter the machine operators
    my_form.fields["machineOperator"].queryset = Employees.objects.filter(StatusActive=True,
                                                                          IsOpStaff=True).order_by('EmpShift').order_by(
        'EmpLName')

    my_form.fields["jobID"].queryset = startUpShot.objects.filter(jobNumber=jobID)

    #
    # if test_type == 'pf':
    #     my_form.fields["defectType"].queryset = passFailTestCriteria.objects.filter(testName__testName=test_name)

    return my_form


def getShift():
    currentHour = datetime.datetime.time(datetime.datetime.now()).hour

    if (currentHour >= 7) and (currentHour < 15):
        shift = 1
    elif (currentHour >= 15) and (currentHour < 23):
        shift = 2
    else:
        shift = 3

    return shift


def checkPartInspection(item_Number):
    for requiredTests in passFailTest.objects.filter(requireAll=True):
        if not passFailByPart.objects.filter(item_Number__item_Number=item_Number,
                                             testName__testName=requiredTests.testName).exists():
            newPartInspection = passFailByPart(item_Number=Part.objects.get(item_Number=item_Number),
                                               testName=requiredTests)
            newPartInspection.save()

    for requiredTests in numericTest.objects.filter(requireAll=True):
        if not numericTestByPart.objects.filter(item_Number__item_Number=item_Number,
                                                testName__testName=requiredTests.testName).exists():
            try:
                exp_part_weight = Part.objects.get(item_Number=item_Number).exp_part_weight
                low_exp = Decimal(exp_part_weight * 0.95)
                high_exp = Decimal(exp_part_weight * 1.05)
                newPartInspection = numericTestByPart(item_Number=Part.objects.get(item_Number=item_Number),
                                                      testName=requiredTests,
                                                      rangeMin=low_exp,
                                                      rangeMax=high_exp)
            except Exception as e:
                newPartInspection = numericTestByPart(item_Number=Part.objects.get(item_Number=item_Number),
                                                      testName=requiredTests,
                                                      rangeMin=0,
                                                      rangeMax=999999)
            newPartInspection.save()

    for requiredTests in textRecord.objects.filter(requireAll=True):
        if not textRecordByPart.objects.filter(item_Number__item_Number=item_Number,
                                               testName__testName=requiredTests.testName).exists():
            newPartInspection = textRecordByPart(testName=requiredTests,
                                                 item_Number=Part.objects.get(item_Number=item_Number))
            newPartInspection.save()

    # for requiredTests in IntegerRecord.objects.filter(requireAll=True):
    #     if not IntegerRecordByPart.objects.filter(item_Number__item_Number=item_Number,
    #                                               testName__testName=requiredTests.testName).exists():
    #         newPartInspection = IntegerRecordByPart(testName=requiredTests,
    #                                                 item_Number=Part.objects.get(item_Number=item_Number))
    #         newPartInspection.save()

    for requiredTests in RangeRecord.objects.filter(requireAll=True):
        if not RangeRecordByPart.objects.filter(item_Number__item_Number=item_Number,
                                                testName__testName=requiredTests.testName).exists():
            newPartInspection = RangeRecordByPart(testName=requiredTests,
                                                  item_Number=Part.objects.get(item_Number=item_Number))
            newPartInspection.save()

            # Will probably need to create something for shot weights...


def checkFormForLog(form, inspectionType, inspectionName, activeJob, rangeInfo=None):
    create_log = False
    errorDescription = 'None'

    shiftID = getShift()
    jobID = activeJob.jobNumber
    machNo = activeJob.machNo.part_identifier
    partDesc = activeJob.item.item_Description
    inspectionName = inspectionName

    if inspectionType == 'Pass-Fail':
        if not form.inspectionResult:
            errorDescription = form.defectType.all()
            error_list = []
            for each_error in errorDescription:
                newForm = errorLog(
                        shiftID=shiftID,
                        machNo=machNo,
                        partDesc=partDesc,
                        jobID=jobID,
                        inspectionName=inspectionName,
                        errorDescription=each_error.passFail,
                )
                newForm.save()

    if inspectionType == 'Range':
        measured_val = form.numVal

        if measured_val < rangeInfo.rangeMin:
            errorDescription = 'Measured value is %1.3f which is less than tolerance (%1.3f)' % (
            measured_val, rangeInfo.rangeMin)
            create_log = True
        if measured_val > rangeInfo.rangeMax:
            errorDescription = 'Measured value is %1.3f which is greater than tolerance (%1.3f)' % (
            measured_val, rangeInfo.rangeMax)
            create_log = True

    if inspectionType == 'Text':
        if not form.inspectionResult:
            errorDescription = '%s' % form.inspectionResult
            create_log = True

    if inspectionType == 'Integer':
        if not form.inspectionResult:
            errorDescription = '%s' % form.inspectionResult
            create_log = True

    if inspectionType == 'Float':
        if not form.inspectionResult:
            errorDescription = '%s' % form.inspectionResult
            create_log = True

    if create_log:
        newForm = errorLog(
                shiftID=shiftID,
                machNo=machNo,
                partDesc=partDesc,
                jobID=jobID,
                inspectionName=inspectionName,
                errorDescription=errorDescription,
        )
        newForm.save()


def createPFStats(qSet):
    resultDict = {
        'numPass': qSet.filter(inspectionResult=1).count(),
        'numFail': qSet.filter(inspectionResult=0).count()}
    resultDict['totalInspections'] = resultDict['numPass'] + resultDict['numFail']
    if resultDict['totalInspections'] > 0:
        resultDict['passPerc'] = 100 * resultDict['numPass'] / resultDict['totalInspections']
    else:
        resultDict['passPerc'] = 0

    return resultDict


def calcRangeStats(rangeList):
    if rangeList:
        resultDict = {
            'rangeList__count': '%i' % (len(rangeList)),
            'rangeList__min': '%1.3f' % (np.amin(rangeList)),
            'rangeList__max': '%1.3f' % (np.amax(rangeList)),
            'rangeList__avg': '%1.3f' % (np.mean(rangeList)),
            'rangeList__stddev': '%1.3f' % (np.std(rangeList))
        }
    else:
        resultDict = {
            'rangeList__count': '%i' % (0),
            'rangeList__min': '%1.3f' % (0),
            'rangeList__max': '%1.3f' % (0),
            'rangeList__avg': '%1.3f' % (0),
            'rangeList__stddev': '%1.3f' % (0)
        }
    return resultDict


def check_HeadCavID(cav_str):
    cav_str.strip(' ')
    cav_str.lower()
    re_pattern = '[a-zA-Z]\s*-\s*\d{1,3}|[a-zA-Z]\s*-\s*all|\d{1,3}|all|none'
    possible_match = re.search(re_pattern, cav_str)
    if possible_match:
        return possible_match.group(0)
    else:
        return None


def get_user_info(man_num):
    try:
        this_user = Employees.objects.get(EmpNum=man_num)
    except Employees.DoesNotExist:
        this_user = None
    return this_user


def get_previous_mach_op(job_number):
    try:
        mattec_info = MattecProd.objects.get(jobNumber=job_number)
        this_machine_operator = EmployeeAtWorkstation.objects.get(workstation=mattec_info.machNo)
        employee_info = this_machine_operator.employee
    except Exception as e:
        print str(e)
        employee_info = None
    return employee_info


def set_new_mach_op(job_number, employee_info):
    try:
        mattec_info = MattecProd.objects.get(jobNumber=job_number)
        current_station = EmployeeAtWorkstation.objects.get(workstation=mattec_info.machNo)
        current_station.employee = employee_info
        current_station.save()
    except EmployeeAtWorkstation.DoesNotExist:
        mattec_info = MattecProd.objects.get(jobNumber=job_number)
        EmployeeAtWorkstation(workstation=mattec_info.machNo, employee=employee_info).save()
    except Exception as e:
        pass
