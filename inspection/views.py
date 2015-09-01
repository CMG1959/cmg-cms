# Create your views here.
import datetime
import numpy as np


from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.db.models import Avg, Max, Min, StdDev
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from models import passFailByPart, passFailTest, passFailInspection, passFailTestCriteria, rangeTestByPart,\
    rangeInspection, textRecord, textRecordByPart, textInspection, rangeTest
from part.models import Part
from startupshot.models import startUpShot, MattecProd
from employee.models import Employees
from molds.models import Mold,PartIdentifier
from production_and_mold_history.models import ProductionHistory
from forms import passFailInspectionForm, rangeInspectionForm, textInspectionForm, jobReportSearch, itemReportSearch



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
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if not active_job.exists():
        redir_url = '/startupshot/create/%s/' % jobNumber
        return HttpResponseRedirect(redir_url)

    # if  PartInspection object hasnt be created, make it now.
    checkPartInspection(active_job[0].item)
    # better go ahead and take care of the Mold now
    checkMoldCavs(item_Number=active_job[0].item)

    pf_inspectionType = passFailByPart.objects.filter(item_Number__item_Number=active_job[0].item)
    range_inspectionType = rangeTestByPart.objects.filter(item_Number__item_Number=active_job[0].item)
    text_inspectionType = textRecordByPart.objects.filter(item_Number__item_Number=active_job[0].item)
    template = loader.get_template('inspection/detailJob.html')
    context = RequestContext(request, {
        'active_job': active_job,
        'pf_inspectionType' : pf_inspectionType,
        'range_inspectionType': range_inspectionType,
        'text_inspectionType':text_inspectionType
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
            # process the data in form.cleaned_data as required
            # part_number = form.cleaned_data['jobID']
            redirect_url = '/inspection/%s/' % (jobNumber)
            # save the data
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = passFailInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id,
                     'passFailTestName':passFailTest.objects.get(testName=inspectionName).id}
        )
        form = presetStandardFields(form, jobID=jobNumber,test_type='pf', test_name=inspectionName)

        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(
            mold_number__mold_number=active_job[0].moldNumber)

        template = loader.get_template('inspection/forms/genInspection.html')
        context = RequestContext(request, {
            'form_title' : inspectionName,
            'form': form,
            'active_job': active_job,
            'use_checkbox2' : True,
            'id_check':'#id_inspectionResult',
            'idSelect':'#id_defectType',
            'idSelect2':'#id_headCavID'
        })
        return HttpResponse(template.render(context))


@login_required
def view_rangeInspection(request, jobNumber, inspectionName):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = rangeInspectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # part_number = form.cleaned_data['jobID']
            redirect_url = '/inspection/%s/' % (jobNumber)
            # save the data
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        rangeInfo = rangeTestByPart.objects.get(testName__testName=inspectionName,item_Number__item_Number=active_job[0].item.item_Number)

        form = rangeInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id,
                     'rangeTestName':rangeInfo.id}
        )
        form = presetStandardFields(form, jobID=jobNumber,test_type='rangeInspection', test_name=inspectionName)

        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(
            mold_number__mold_number=active_job[0].moldNumber)

        template = loader.get_template('inspection/forms/genInspection.html')
        context = RequestContext(request, {
            'form_title' : inspectionName,
            'form': form,
            'active_job': active_job,
            'use_checkbox' : True,
            'id_check':'#id_isFullShot',
            'idSelect':'#id_headCavID',
            'use_minmax': True,
            'num_id':'#id_numVal',
            'min_val':rangeInfo.rangeMin,
            'max_val':rangeInfo.rangeMax
        })
        return HttpResponse(template.render(context))

@login_required
def view_textInspection(request, jobNumber, inspectionName):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = textInspectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # part_number = form.cleaned_data['jobID']
            redirect_url = '/inspection/%s/' % (jobNumber)
            # save the data
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = textInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id,
                     'textTestName':textRecord.objects.get(testName=inspectionName).id}
        )
        form = presetStandardFields(form, jobID=jobNumber,test_type='tex', test_name=inspectionName)

        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(
            mold_number__mold_number=active_job[0].moldNumber)

        template = loader.get_template('inspection/forms/genInspection.html')
        context = RequestContext(request, {
            'form_title' : inspectionName,
            'form': form,
            'active_job': active_job,
            'use_checkbox' : True,
            'id_check':'#id_inspectionResult',
            'idSelect':'#id_headCavID'
        })
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
            job_number = form.cleaned_data['job_Number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            context_dic = createJobReportDict(job_number, date_from=date_from, date_to=date_to)
            template = loader.get_template('inspection/reports/jobReport.html')

            context = RequestContext(request, context_dic)
            return HttpResponse(template.render(context))

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
    context_dict['partDict'] = createItemReportDict(itemNumber)
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



####### Helper functions ###########

def createItemReportDict(itemNumber, date_from=None, date_to=None):
    date_from1, date_to1 = createDateRange(date_from=date_from, date_to=date_to)

    jobList = startUpShot.objects.filter(item__item_Number=itemNumber, dateCreated__range=(date_from1, date_to1))
    jobList = jobList.values_list('jobNumber', flat=True)
    partDict = {}
    n = 0
    for eachJob in jobList:
        dictID = 'Job%i' % (n)
        n += 1
        partDict[dictID] = {}
        partDict[dictID] = createJobReportDict(eachJob, date_from=date_from, date_to=date_from)

    return partDict

def createJobReportDict(jobNumber, date_from=None, date_to=None):
    date_from, date_to = createDateRange(date_from=date_from, date_to=date_to)

    context_dic = {}

    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')

    context_dic['active_job'] = active_job

    # Job number 6 and 9 should be QA and
    context_dic['phl'] = ProductionHistory.objects.filter(jobNumber__jobNumber=jobNumber,
                                                          dateCreated__range=(date_from, date_to),
                                                          inspectorName__EmpJob__JobNum=6)

    pf_inspectionType = passFailByPart.objects.filter(item_Number__item_Number=active_job[0].item)
    rangeTests = rangeTestByPart.objects.filter(item_Number__item_Number=active_job[0].item)

    context_dic['pf'] = {}
    context_dic['pfSummary']={}
    n = 1
    for each_pf_inspection in pf_inspectionType:
        context_dic['pf'][str(n)] = passFailInspection.objects.filter(passFailTestName__testName=each_pf_inspection.testName.testName,
                                                                                     jobID__jobNumber=jobNumber)

        context_dic['pfSummary'][str(n)] = {}
        context_dic['pfSummary'][str(n)]['pfName'] = each_pf_inspection.testName.testName
        context_dic['pfSummary'][str(n)]['numPass'] = context_dic['pf'][str(n)].filter(
            inspectionResult=1).count()

        ### Count number of failed inspections
        context_dic['pfSummary'][str(n)]['numFail'] = context_dic['pf'][str(n)].filter(
            inspectionResult=0).count()

        ### Calculate number of total inspections
        context_dic['pfSummary'][str(n)]['totalInspections'] = context_dic['pfSummary'][str(n)]['numPass'] + \
                                                                  context_dic['pfSummary'][str(n)]['numFail']
        ### Calculate percentage passed
        if context_dic['pfSummary'][str(n)]['totalInspections'] > 0:
            context_dic['pfSummary'][str(n)]['passPerc'] = 100 * context_dic['pfSummary'][str(n)]['numPass'] / + \
                context_dic['pfSummary'][str(n)]['totalInspections']
        else:
            context_dic['pfSummary'][str(n)]['passPerc'] = 0

        n+=1

    n = 1
    context_dic['rangeTests']={}
    context_dic['rangeTestSummary']={}
    for each_range_inspection in rangeTests:
        context_dic['rangeTests'][str(n)] = rangeInspection.objects.filter(rangeTestName__testName=each_range_inspection.testName,
                                                                                     jobID__jobNumber=jobNumber)
        context_dic['rangeTestSummary'][str(n)] = {}
        context_dic['rangeTestSummary'][str(n)]['rangeName'] = each_range_inspection.testName.testName

        rangeList = []
        for eachShot in context_dic['rangeTests'][str(n)]:
            if eachShot.isFullShot:
                rangeList.append(eachShot.numVal / active_job[0].activeCavities)
            else:
                rangeList.append(eachShot.numVal)

        if rangeList:
            context_dic['rangeTestSummary'][str(n)]['rangeStats'] = {
                    'rangeList__count' :  '%i' % (len(rangeList)),
                    'rangeList__min':    '%1.3f' % (np.amin(rangeList)),
                    'rangeList__max':    '%1.3f' % (np.amax(rangeList)),
                    'rangeList__avg':    '%1.3f' % (np.mean(rangeList)),
                    'rangeList__stddev': '%1.3f' % (np.std(rangeList))
                }
        else:
            context_dic['rangeTestSummary'][str(n)]['rangeStats'] = {
                    'rangeList__count' :  '%i' % (0),
                    'rangeList__min':    '%1.3f' % (0),
                    'rangeList__max':    '%1.3f' % (0),
                    'rangeList__avg':    '%1.3f' % (0),
                    'rangeList__stddev': '%1.3f' % (0)
                }

        n += 1

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
    my_form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9).order_by('EmpShift')
                                                                         # EmpShift=getShift())
    ### Filter the QA ladies
    my_form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6).order_by('EmpShift')
                                                                       # EmpShift=getShift())
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
    # Will probably need to create something for shot weights...


def checkMoldCavs(item_Number=None,mold_Number=None):
    if item_Number:
        mattec_info = MattecProd.objects.get(itemNo=item_Number)
        mold_Number = mattec_info.moldNumber

    if not PartIdentifier.objects.filter(mold_number__mold_number=mold_Number).exists():
        ### grab the mold information
        mold_info = Mold.objects.get(mold_number = mold_Number)
        ### add all the cavities
        for n in range(mold_info.num_cavities):
            newCavID = PartIdentifier(mold_number=mold_info,head_code='A',cavity_id = '%i' % (n))
            newCavID.save()