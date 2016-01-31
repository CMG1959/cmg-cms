# Create your views here.
import numpy as np
import re
from django.http import HttpResponse, HttpResponseRedirect,Http404
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
from molds.models import Mold,PartIdentifier
from production_and_mold_history.models import ProductionHistory
from forms import passFailInspectionForm, rangeInspectionForm, textInspectionForm, jobReportSearch, itemReportSearch

from reports import JobReport
import collections
import json
import datetime
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
    MattecInfo = MattecProd.objects.get(jobNumber=jobNumber)
    jobNumber = str(jobNumber).strip()
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')

    if not active_job.exists():
        if MattecProd.objects.get(jobNumber=jobNumber).machNo.strip() != 'FAS01':
            redir_url = '/startupshot/create/%s/' % jobNumber
            return HttpResponseRedirect(redir_url)
        else:
            newForm = startUpShot(item=Part.objects.get(item_Number=MattecInfo.itemNo), \
                jobNumber=jobNumber, \
                moldNumber=Mold.objects.get(mold_number=MattecInfo.moldNumber),
                inspectorName=Employees.objects.get(EmpNum=10075), \
                machineOperator=Employees.objects.get(EmpNum=10075), \
                shotWeight=0.0, \
                activeCavities=MattecInfo.activeCavities, \
                cycleTime=MattecInfo.cycleTime, \
                machNo=EquipmentInfo.objects.filter(part_identifier=MattecInfo.machNo)[0])
            newForm.save()




    # if  PartInspection object hasnt be created, make it now.
    checkPartInspection(active_job[0].item)
    # better go ahead and take care of the Mold now


    pf_inspectionType = passFailByPart.objects.filter(item_Number__item_Number=active_job[0].item, testName__isSystemInspection=False)
    range_inspectionType = rangeTestByPart.objects.filter(item_Number__item_Number=active_job[0].item, testName__isSystemInspection=False)
    text_inspectionType = textRecordByPart.objects.filter(item_Number__item_Number=active_job[0].item, testName__isSystemInspection=False)
    int_inspectionType = IntegerRecordByPart.objects.filter(item_Number__item_Number=active_job[0].item, testName__isSystemInspection=False)
    float_inspectionType = FloatRecordByPart.objects.filter(item_Number__item_Number=active_job[0].item, testName__isSystemInspection=False)
    template = loader.get_template('inspection/detailJob.html')
    context = RequestContext(request, {
        'active_job': active_job,
        'pf_inspectionType' : pf_inspectionType,
        'range_inspectionType': range_inspectionType,
        'text_inspectionType':text_inspectionType,
        'int_inspectionType': int_inspectionType,
        'float_inspectionType': float_inspectionType
    })
    return HttpResponse(template.render(context))


######################################
#
#  Section for generating forms
#
######################################


@login_required
def view_pfInspection(request, jobNumber, inspectionName):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = passFailInspectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:

                # process the data in form.cleaned_data as required
                # part_number = form.cleaned_data['jobID']
                redirect_url = '/inspection/%s/' % (jobNumber)

                checkFormForLog(form, inspectionType = 'pf',
                                inspectionName = passFailTest.objects.get(testName=inspectionName).testName,
                                activeJob=active_job, rangeInfo=None)

                # save the data
                my_form = form.save(commit=False)

                set_new_mach_op(jobNumber, my_form.machineOperator)

                my_form.inspectorName = is_user

                if my_form.headCavID:
                    my_form.headCavID = check_HeadCavID(my_form.headCavID)
                my_form.save()



                form.save_m2m()

                # redirect to a new URL:
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))
        else:
            template = loader.get_template('inspection/bad_cav.html')
            context = RequestContext(request)
            return HttpResponse(template.render(context))

    # if a GET (or any other method) we'll create a blank form
    else:

        machine_operator = get_previous_mach_op(jobNumber)

        initial_dictionary = {'jobID': startUpShot.objects.get(jobNumber=jobNumber).id,
                     'passFailTestName':passFailTest.objects.get(testName=inspectionName).id}

        form = passFailInspectionForm(initial=initial_dictionary)

        form = presetStandardFields(form, jobID=jobNumber,test_type='pf', test_name=inspectionName)

        template = loader.get_template('inspection/forms/genInspection.html')

        context_dict = {
            'form_title' : inspectionName,
            'form': form,
            'active_job': active_job,
            'use_checkbox2' : True,
            'id_check':'#id_inspectionResult',
            'idSelect':'#id_defectType',
            'idSelect2':'#id_headCavID',
            'head_cav_id':'#id_headCavID',
        }
        if machine_operator:
            context_dict.update({'machine_operator': machine_operator.id})

        context = RequestContext(request, context_dict)

        return HttpResponse(template.render(context))



@login_required
def view_rangeInspection(request, jobNumber, inspectionName):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')

    rangeInfo = rangeTestByPart.objects.get(testName__testName=inspectionName,item_Number__item_Number=active_job[0].item.item_Number)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = rangeInspectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                
                # process the data in form.cleaned_data as required
                # part_number = form.cleaned_data['jobID']
                redirect_url = '/inspection/%s/' % (jobNumber)

                # process the data in form.cleaned_data as required
                redirect_url = '/inspection/%s/' % (jobNumber)
                # save the data
                checkFormForLog(form, inspectionType = 'rangeInspection',
                                inspectionName = rangeInfo.testName,
                                activeJob=active_job, rangeInfo=rangeInfo)

                if ((form.cleaned_data['numVal'] >=  rangeInfo.rangeMin) and (form.cleaned_data['numVal'] <= rangeInfo.rangeMax)):
                    inspectionResult = True
                else:
                    inspectionResult = False

               # save the data
                my_form = form.save(commit=False)
                set_new_mach_op(jobNumber, my_form.machineOperator)
                my_form.inspectorName = is_user
                my_form.inspectionResult = inspectionResult

                if my_form.headCavID:
                    my_form.headCavID = check_HeadCavID(my_form.headCavID)
                my_form.save()

                # redirect to a new URL:
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))
        else:
            template = loader.get_template('inspection/bad_cav.html')
            context = RequestContext(request)
            return HttpResponse(template.render(context))

    # if a GET (or any other method) we'll create a blank form
    else:

        machine_operator = get_previous_mach_op(jobNumber)

        form = rangeInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id,
                     'rangeTestName':rangeInfo.id}
        )
        form = presetStandardFields(form, jobID=jobNumber,test_type='rangeInspection', test_name=inspectionName)
        form.fields["rangeTestName"].queryset = rangeTestByPart.objects.filter(item_Number__item_Number = active_job[0].item.item_Number,
                                                                            testName__testName=inspectionName)

        template = loader.get_template('inspection/forms/genInspection.html')
        context_dict = {
            'form_title' : inspectionName,
            'form': form,
            'active_job': active_job,
            'use_checkbox' : True,
            'id_check':'#id_isFullShot',
            'idSelect':'#id_headCavID',
            'use_minmax': True,
            'num_id':'#id_numVal',
            'min_val':rangeInfo.rangeMin,
            'max_val':rangeInfo.rangeMax,
            'id_result':'#id_inspectionResult',
            'head_cav_id':'#id_headCavID',
        }

        if machine_operator:
            context_dict.update({'machine_operator': machine_operator.id})

        context = RequestContext(request, context_dict)

        return HttpResponse(template.render(context))

@login_required
def view_textInspection(request, jobNumber, inspectionName):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = textInspectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                
                # process the data in form.cleaned_data as required
                # part_number = form.cleaned_data['jobID']
                redirect_url = '/inspection/%s/' % (jobNumber)

                # process the data in form.cleaned_data as required
                # part_number = form.cleaned_data['jobID']
                redirect_url = '/inspection/%s/' % (jobNumber)
                # save the data
                # save the data
                my_form = form.save(commit=False)

                set_new_mach_op(jobNumber, my_form.machineOperator)

                my_form.inspectorName = is_user

                if my_form.headCavID:
                    my_form.headCavID = check_HeadCavID(my_form.headCavID)
                my_form.save()
                # save the data
                checkFormForLog(form, inspectionType = 'textInspection',
                                inspectionName = inspectionName,
                                activeJob=active_job)
                # redirect to a new URL:

                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))

        else:
            template = loader.get_template('inspection/bad_cav.html')
            context = RequestContext(request)
            return HttpResponse(template.render(context))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = textInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id,
                     'textTestName':textRecord.objects.get(testName=inspectionName).id}
        )
        form = presetStandardFields(form, jobID=jobNumber,test_type='tex', test_name=inspectionName)

        machine_operator = get_previous_mach_op(jobNumber)

        template = loader.get_template('inspection/forms/genInspection.html')
        context_dict = {
            'form_title' : inspectionName,
            'form': form,
            'active_job': active_job,
            'use_checkbox' : True,
            'id_check':'#id_inspectionResult',
            'idSelect':'#id_headCavID',
            'head_cav_id':'#id_headCavID',
        }
        if machine_operator:
            context_dict.update({'machine_operator': machine_operator.id})

        context = RequestContext(request, context_dict)

        return HttpResponse(template.render(context))

@login_required
def view_IntegerInspection(request, jobNumber, inspectionName):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = textInspectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                
                # process the data in form.cleaned_data as required
                # part_number = form.cleaned_data['jobID']
                redirect_url = '/inspection/%s/' % (jobNumber)

                # process the data in form.cleaned_data as required
                # part_number = form.cleaned_data['jobID']
                redirect_url = '/inspection/%s/' % (jobNumber)

                # save the data
                my_form = form.save(commit=False)

                set_new_mach_op(jobNumber, my_form.machineOperator)

                my_form.inspectorName = is_user

                if my_form.headCavID:
                    my_form.headCavID = check_HeadCavID(my_form.headCavID)
                my_form.save()

                checkFormForLog(form, inspectionType = 'IntegerInspection',
                                inspectionName = inspectionName,
                                activeJob=active_job)
                # redirect to a new URL:
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))
        else:
            template = loader.get_template('inspection/bad_cav.html')
            context = RequestContext(request)
            return HttpResponse(template.render(context))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = textInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id,
                     'textTestName':textRecord.objects.get(testName=inspectionName).id}
        )
        form = presetStandardFields(form, jobID=jobNumber,test_type='IntegerType', test_name=inspectionName)

        machine_operator = get_previous_mach_op(jobNumber)

        template = loader.get_template('inspection/forms/genInspection.html')
        context_dict = {
            'form_title' : inspectionName,
            'form': form,
            'active_job': active_job,
            'use_checkbox' : True,
            'id_check':'#id_inspectionResult',
            'idSelect':'#id_headCavID',
            'head_cav_id':'#id_headCavID',
        }

        if machine_operator:
            context_dict.update({'machine_operator': machine_operator.id})

        context = RequestContext(request, context_dict)
        return HttpResponse(template.render(context))

@login_required
def view_FloatInspection(request, jobNumber, inspectionName):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = textInspectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                
                # process the data in form.cleaned_data as required
                # part_number = form.cleaned_data['jobID']
                redirect_url = '/inspection/%s/' % (jobNumber)

                # process the data in form.cleaned_data as required
                # part_number = form.cleaned_data['jobID']
                redirect_url = '/inspection/%s/' % (jobNumber)
                # save the data
                my_form = form.save(commit=False)

                set_new_mach_op(jobNumber, my_form.machineOperator)

                if my_form.headCavID:
                    my_form.headCavID = check_HeadCavID(my_form.headCavID)
                my_form.save()

                # save the data
                checkFormForLog(form, inspectionType = 'FloatInspection',
                                inspectionName = inspectionName,
                                activeJob=active_job)
                # redirect to a new URL:
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))
        else:
            template = loader.get_template('inspection/bad_cav.html')
            context = RequestContext(request)
            return HttpResponse(template.render(context))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = textInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id,
                     'textTestName':textRecord.objects.get(testName=inspectionName).id}
        )
        form = presetStandardFields(form, jobID=jobNumber,test_type='FloatType', test_name=inspectionName)

        machine_operator = get_previous_mach_op(jobNumber)

        template = loader.get_template('inspection/forms/genInspection.html')

        context_dict={
            'form_title' : inspectionName,
            'form': form,
            'active_job': active_job,
            'use_checkbox' : True,
            'id_check':'#id_inspectionResult',
            'idSelect':'#id_headCavID',
            'head_cav_id':'#id_headCavID',
        }

        if machine_operator:
            context_dict.update({'machine_operator': machine_operator.id})

        context = RequestContext(request, context_dict)
        return HttpResponse(template.render(context))




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
            else:
                if startUpShot.objects.filter(jobNumber=job_number).exists():
                    my_report = JobReport(job_number=job_number, date_from=date_from, date_to=date_to)
                    return my_report.get_report()
                else:
                    return render(request,'404.html')

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
    print context_dict

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
        return render(request,'404.html')


####### Section for generating data for plots ###########
def view_jsonError(job_number, date_from, date_to):
    date_from, date_to = createDateRange(date_from,date_to)
    pf = passFailInspection.objects.filter(jobID__jobNumber=job_number,dateCreated__range=(date_from, date_to),inspectionResult=0)
    ri = rangeInspection.objects.filter(jobID__jobNumber=job_number, dateCreated__range=(date_from, date_to),inspectionResult=0)
    ti = textInspection.objects.filter(jobID__jobNumber=job_number, dateCreated__range=(date_from, date_to),inspectionResult=0)


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
    sort_jawn = [(l,k) for k,l in sorted([(j,i) for i,j in count_errors.items()], reverse=True)]
    counted_errors = []
    for k,v in sort_jawn:
        counted_errors.append({'error_name':k,'error_count':v})

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
    rangeTests = rangeTestByPart.objects.filter(item_Number__item_Number=itemNumber)
    textTests = textRecordByPart.objects.filter(item_Number__item_Number=itemNumber)

    partDict = {'pf':{},'rangeTest':{},'activeJob':susList}

    k=0
    for eachInspection1 in pf_inspectionType:
        eachInspection = eachInspection1.testName
        partDict['pf'][eachInspection] = collections.OrderedDict()
        thisInspection = passFailInspection.objects.filter(passFailTestName__testName = eachInspection,
                                                           dateCreated__range=(date_from1, date_to1))
        n=0

        key = 'pf'+str(k)
        collapse_list.append('#'+key)
        partDict['pf'][eachInspection]['html_id'] = key
        k=k+1

        for eachJob in jobList:
            partDict['pf'][eachInspection]['inspectionName'] = eachInspection
            partDict['pf'][eachInspection][n]={}
            thisInspectionbyJob = thisInspection.filter(jobID__jobNumber = eachJob).order_by('-dateCreated')
            partDict['pf'][eachInspection][n]['jobID'] = eachJob
            partDict['pf'][eachInspection][n].update(createPFStats(thisInspectionbyJob))
            n += 1

        partDict['pf'][eachInspection][n]={}
        partDict['pf'][eachInspection][n]['jobID'] = 'Total'
        partDict['pf'][eachInspection][n].update(createPFStats(thisInspection.filter(jobID__item__item_Number=itemNumber)))

    k = 0
    for eachInspection1 in rangeTests:


        eachInspection = eachInspection1.testName.testName
        partDict['rangeTest'][eachInspection] = collections.OrderedDict()
        partDict['rangeTest'][eachInspection]['inspectionName'] = eachInspection

        thisInspection = rangeInspection.objects.filter(rangeTestName__testName__testName = eachInspection,
                                                           dateCreated__range=(date_from1, date_to1)).order_by('-dateCreated')
        n=0

        key = 'rt'+str(k)
        collapse_list.append('#'+key)
        partDict['rangeTest'][eachInspection]['html_id'] = key
        k=k+1

        totalRangeList = []
        for eachJob in jobList:
            partDict['rangeTest'][eachInspection][n] = {}
            partDict['rangeTest'][eachInspection][n]['jobID']=eachJob

            thisInspectionbyJob = thisInspection.filter(jobID__jobNumber = eachJob).order_by('-dateCreated')
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

            partDict['rangeTest'][eachInspection][n]['rangeStats'] = calcRangeStats(rangeList)
            n += 1

        partDict['rangeTest'][eachInspection][n] = {'jobID' :'Total',
                                                         'rangeStats':calcRangeStats(totalRangeList)}




    n = 0
    partDict['textTests']=collections.OrderedDict()
    for eachTextTest in textTests:
        key = 'tt'+str(n)
        collapse_list.append('#'+key)
        partDict['textTests'][n] = {
            'html_id': key,
            'testName': eachTextTest.testName,
            'textDict': textInspection.objects.filter(\
            textTestName__testName=eachTextTest.testName,
            jobID__item__item_Number=itemNumber)
        }

        n += 1

    partDict['phl']=[]
    for eaJob in eachJob:
        partDict['phl'].extend(ProductionHistory.objects.filter(jobNumber=eaJob).values('dateCreated','jobNumber','inspectorName__EmpLMName','descEvent').order_by('-dateCreated'))

    partDict['phl'] = [item for sublist in partDict['phl'] for item in sublist] #change?
    partDict['useJobNo'] = True


    collapse_list.append('#phl')

    partDict.update({'collapse_list':collapse_list})

    partDict.update({
        'headerDict':{
            'companyName':'Custom Molders Group',
            'reportName':'Part Report',
            'documentName':'Part Number: %s' % itemNumber
        }
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
                                                          inspectorName__IsQCStaff=True).values('dateCreated','jobNumber','inspectorName__EmpLMName','descEvent').order_by('-dateCreated')

    pf_inspectionType = passFailByPart.objects.filter(item_Number__item_Number=active_job[0].item)
    rangeTests = rangeTestByPart.objects.filter(item_Number__item_Number=active_job[0].item)
    textTests = textRecordByPart.objects.filter(item_Number__item_Number=active_job[0].item)


    context_dic['pf'] = {}
    context_dic['pfSummary']={}
    n = 0
    for each_pf_inspection in pf_inspectionType:
        key = 'pf'+str(n)
        collapse_list.append('#'+key)
        context_dic['pf'][key] = passFailInspection.objects.filter(passFailTestName__testName=each_pf_inspection.testName.testName,
                                                                      jobID__jobNumber=jobNumber,
                                                                      dateCreated__range=(date_from, date_to)).order_by('-dateCreated')
        context_dic['pfSummary'][key] = {}
        context_dic['pfSummary'][key]['pfName'] = each_pf_inspection.testName.testName
        context_dic['pfSummary'][key].update(createPFStats(context_dic['pf'][key]))
        n+=1

    n = 0
    context_dic['rangeTests']={}
    context_dic['rangeTestSummary']={}
    for each_range_inspection in rangeTests:
        key = 'rt'+str(n)
        collapse_list.append('#'+key)
        context_dic['rangeTests'][key] = rangeInspection.objects.filter(rangeTestName__testName=each_range_inspection.testName,
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

        context_dic['rangeTestSummary'][key]['rangeStats']=calcRangeStats(rangeList)

        n += 1


    n = 0
    context_dic['textTests']={}
    for eachTextTest in textTests:
        key = 'tt'+ str(n)
        collapse_list.append('#'+key)
        context_dic['textTests'][key] = {
            'testName': eachTextTest.testName,
            'textDict': textInspection.objects.filter(\
            textTestName__testName=eachTextTest.testName,jobID__jobNumber=jobNumber).order_by('-dateCreated')
        }

        n += 1


    context_dic['phl'] = ProductionHistory.objects.filter(jobNumber=jobNumber).values('dateCreated','jobNumber','inspectorName__EmpLMName','descEvent').order_by('-dateCreated')
    collapse_list.append('#'+'phl')

    context_dic.update({
        'headerDict':{
            'companyName':'Custom Molders Group',
            'reportName':'Job Report',
            'documentName':'Job Number: %s' % (jobNumber)
        }
    })

    context_dic.update({'collapse_list':collapse_list})
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
                                                                          IsOpStaff=True).order_by('EmpShift').order_by('EmpLName')

    my_form.fields["jobID"].queryset = startUpShot.objects.filter(jobNumber=jobID)

    if test_type == 'pf':
        my_form.fields["defectType"].queryset = passFailTestCriteria.objects.filter(testName__testName=test_name)

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
        if not passFailByPart.objects.filter(item_Number__item_Number=item_Number,testName__testName=requiredTests.testName).exists():
            newPartInspection = passFailByPart(item_Number = Part.objects.get(item_Number=item_Number),
                                           testName = requiredTests)
            newPartInspection.save()


    for requiredTests in rangeTest.objects.filter(requireAll=True):
        if not rangeTestByPart.objects.filter(item_Number__item_Number=item_Number,testName__testName=requiredTests.testName).exists():
            newPartInspection = rangeTestByPart(item_Number = Part.objects.get(item_Number=item_Number),
                                               testName = requiredTests,
                                                rangeMin=0,
                                                rangeMax=9999999)
            newPartInspection.save()


    for requiredTests in textRecord.objects.filter(requireAll=True):
        if not textRecordByPart.objects.filter(item_Number__item_Number=item_Number,testName__testName=requiredTests.testName).exists():
            newPartInspection = textRecordByPart(testName = requiredTests,item_Number = Part.objects.get(item_Number=item_Number))
            newPartInspection.save()

    for requiredTests in IntegerRecord.objects.filter(requireAll=True):
        if not IntegerRecordByPart.objects.filter(item_Number__item_Number=item_Number,testName__testName=requiredTests.testName).exists():
            newPartInspection = IntegerRecordByPart(testName = requiredTests,item_Number = Part.objects.get(item_Number=item_Number))
            newPartInspection.save()

    for requiredTests in FloatRecord.objects.filter(requireAll=True):
        if not FloatRecordByPart.objects.filter(item_Number__item_Number=item_Number,testName__testName=requiredTests.testName).exists():
            newPartInspection = FloatRecordByPart(testName = requiredTests,item_Number = Part.objects.get(item_Number=item_Number))
            newPartInspection.save()

    # Will probably need to create something for shot weights...


def checkFormForLog(form, inspectionType, inspectionName, activeJob, rangeInfo=None):
    create_log = False
    errorDescription = 'None'

    shiftID = getShift()
    jobID = activeJob[0].jobNumber
    machNo = activeJob[0].machNo.part_identifier
    partDesc = activeJob[0].item.item_Description
    inspectionName = inspectionName

    if inspectionType == 'pf':
        if not form.cleaned_data['inspectionResult']:
            errorDescription = form.cleaned_data['defectType']
            error_list = []
            for each_error in errorDescription:
                error_list.append(each_error.passFail)
            errorDescription = ', '.join(error_list)
            create_log = True

    if inspectionType == 'rangeInspection':
        measured_val = form.cleaned_data['numVal']

        if measured_val<rangeInfo.rangeMin:
            errorDescription = 'Measured value is %1.3f which is less than tolerance (%1.3f)' % (measured_val,rangeInfo.rangeMin)
            create_log = True
        if measured_val>rangeInfo.rangeMax:
            errorDescription = 'Measured value is %1.3f which is greater than tolerance (%1.3f)' % (measured_val,rangeInfo.rangeMax)
            create_log = True

    if inspectionType == 'textInspection':
        if not form.cleaned_data['inspectionResult']:
            errorDescription = '%s' % form.cleaned_data['inspectionResult']
            create_log = True

    if inspectionType == 'IntegerInspection':
        if not form.cleaned_data['inspectionResult']:
            errorDescription = '%s' % form.cleaned_data['inspectionResult']
            create_log = True

    if inspectionType == 'FloatInspection':
        if not form.cleaned_data['inspectionResult']:
            errorDescription = '%s' % form.cleaned_data['inspectionResult']
            create_log = True

    if create_log:
        newForm = errorLog(
                shiftID = shiftID,
                machNo = machNo,
                partDesc = partDesc,
                jobID = jobID,
                inspectionName=inspectionName,
                errorDescription = errorDescription,
            )
        newForm.save()


def createPFStats(qSet):
    resultDict = {
        'numPass': qSet.filter(inspectionResult=1).count(),
        'numFail': qSet.filter(inspectionResult=0).count()}
    resultDict['totalInspections'] = resultDict['numPass']+resultDict['numFail']
    if resultDict['totalInspections'] > 0:
        resultDict['passPerc']=100*resultDict['numPass']/resultDict['totalInspections']
    else:
        resultDict['passPerc']=0

    return resultDict

def calcRangeStats(rangeList):
    if rangeList:
        resultDict = {
                    'rangeList__count' :  '%i' % (len(rangeList)),
                    'rangeList__min':    '%1.3f' % (np.amin(rangeList)),
                    'rangeList__max':    '%1.3f' % (np.amax(rangeList)),
                    'rangeList__avg':    '%1.3f' % (np.mean(rangeList)),
                    'rangeList__stddev': '%1.3f' % (np.std(rangeList))
                }
    else:
        resultDict = {
                    'rangeList__count' :  '%i' % (0),
                    'rangeList__min':    '%1.3f' % (0),
                    'rangeList__max':    '%1.3f' % (0),
                    'rangeList__avg':    '%1.3f' % (0),
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
        EmployeeAtWorkstation.objects.get(workstation=mattec_info.machNo).update(employee=employee_info)
    except EmployeeAtWorkstation.DoesNotExist:
        mattec_info = MattecProd.objects.get(jobNumber=job_number)
        EmployeeAtWorkstation(workstation=mattec_info.machNo, employee=employee_info).save()
    except Exception as e:
        pass