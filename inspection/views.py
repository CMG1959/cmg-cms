# Create your views here.
import datetime

from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.db.models import Avg, Max, Min, StdDev
from django.core.exceptions import ObjectDoesNotExist
from models import partWeightInspection, visualInspection, shotWeightInspection
from part.models import PartInspection
from startupshot.models import startUpShot, MattecProd
from employee.models import employee
from molds.models import PartIdentifier
from forms import partWeightForm, visualInspectionForm, jobReportSearch, itemReportSearch, shotWeightForm
from django.utils import timezone


def view_index(request):
    activeInMattec = MattecProd.objects.all()

    # active_parts = Production.objects.filter(inProduction=True).select_related('item')

    template = loader.get_template('inspection/index.html')
    context = RequestContext(request, {
        'active_parts': activeInMattec,
    })
    return HttpResponse(template.render(context))


def view_detailJob(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if not active_job.exists():
        raise Http404("Part number does not exist")

    inspectionTypes = PartInspection.objects.get(item_Number__item_Number=active_job[0].item)

    template = loader.get_template('inspection/detailJob.html')
    context = RequestContext(request, {
        'active_job': active_job,
        'inspectionTypes': inspectionTypes
    })
    return HttpResponse(template.render(context))


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


def view_itemReport(request, itemNumber):
    context_dict = {}
    context_dict['partDict'] = createItemReportDict(itemNumber)
    print context_dict

    template = loader.get_template('inspection/reports/partReport.html')
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))


def view_jobReport(request, jobNumber):
    context_dic = createJobReportDict(jobNumber)
    template = loader.get_template('inspection/reports/jobReport.html')
    context = RequestContext(request, context_dic)
    return HttpResponse(template.render(context))


def view_visualInspection(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = visualInspectionForm(request.POST)
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
        form = visualInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id}
        )
        form = presetStandardFields(form)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = employee.objects.filter(organization_name__org_name='Machine Operator')
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = employee.objects.filter(organization_name__org_name='QA')
        ### Filter the cavity and molds
        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(
            mold_number__mold_number=active_job[0].moldNumber)

    return render(request, 'inspection/forms/visualInspection.html', {'form': form, 'active_job': active_job})


def view_partWeightInspection(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = partWeightForm(request.POST)
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
        form = partWeightForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = employee.objects.filter(organization_name__org_name='Machine Operator')
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = employee.objects.filter(organization_name__org_name='QA')

        ### Filter the cavity and molds
        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(
            mold_number__mold_number=active_job[0].moldNumber)

    return render(request, 'inspection/forms/partWeightInspection.html', {'form': form, 'active_job': active_job})


def view_shotWeightInspection(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = shotWeightForm(request.POST)
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
        form = shotWeightForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = employee.objects.filter(organization_name__org_name='Machine Operator')
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = employee.objects.filter(organization_name__org_name='QA')

    return render(request, 'inspection/forms/shotWeightInspection.html', {'form': form, 'active_job': active_job})


def createItemReportDict(itemNumber, date_from=None, date_to=None):
    date_from, date_to = createDateRange(date_from=date_from, date_to=date_to)

    try:
        inspectionTypes = PartInspection.objects.get(item_Number__item_Number=itemNumber)
    except ObjectDoesNotExist:
        raise Http404("No inspections types were set")

    jobList = startUpShot.objects.filter(item__item_Number=itemNumber, dateCreated__range=(date_from, date_to))
    jobList = jobList.values_list('jobNumber', flat=True)
    partDict = {}
    n = 0
    for eachJob in jobList:
        dictID = 'Job%i' % (n)
        n += 1
        partDict[dictID] = {}
        partDict[dictID]['startupInfo'] = startUpShot.objects.filter(jobNumber=eachJob, dateCreated__range=(
            date_from, date_to)).select_related('item')

        if inspectionTypes.visual_inspection:
            temp_obj = visualInspection.objects.filter(jobID__jobNumber=eachJob,
                                                       dateCreated__range=(date_from, date_to))
            partDict[dictID]['InspectionDates'] = {}
            partDict[dictID]['InspectionDates'] = temp_obj.aggregate(Min('dateCreated'), Max('dateCreated'))

            partDict[dictID]['visualInspectionDict'] = {}
            ### Count number of passed inspections
            partDict[dictID]['visualInspectionDict']['numPass'] = temp_obj.filter(inspectionResult=1).count()

            ### Count number of failed inspections
            partDict[dictID]['visualInspectionDict']['numFail'] = temp_obj.filter(inspectionResult=0).count()

            ### Calculate number of total inspections
            partDict[dictID]['visualInspectionDict']['totalInspections'] = partDict[dictID]['visualInspectionDict'][
                                                                               'numPass'] + \
                                                                           partDict[dictID]['visualInspectionDict'][
                                                                               'numFail']
            ### Calculate percentage passed
            if partDict[dictID]['visualInspectionDict']['totalInspections'] > 0:
                partDict[dictID]['visualInspectionDict']['passPerc'] = 100 * partDict[dictID]['visualInspectionDict'][
                    'numPass'] / partDict[dictID]['visualInspectionDict']['totalInspections']
            else:
                partDict[dictID]['visualInspectionDict']['passPerc'] = 0

        if inspectionTypes.part_weight_inspection:
            temp_obj = partWeightInspection.objects.filter(jobID__jobNumber=eachJob,
                                                           dateCreated__range=(date_from, date_to))
            partDict[dictID]['partWeightInspection'] = temp_obj
            partDict[dictID]['partWeightInspectionDict'] = {}
            partDict[dictID]['partWeightInspectionDict'] = temp_obj.aggregate(Avg('partWeight'),
                                                                              Max('partWeight'),
                                                                              Min('partWeight'),
                                                                              StdDev('partWeight'))
        if inspectionTypes.shot_weight_inspection:
            partDict[dictID]['shotWeightInspection'] = shotWeightInspection.objects.filter(jobID__jobNumber=eachJob,
                                                                                           dateCreated__range=(
                                                                                               date_from, date_to))
            partDict[dictID]['shotWeightInspectionDict'] = {}
            partDict[dictID]['shotWeightInspectionDict'] = partDict[dictID]['shotWeightInspection'].aggregate(
                Avg('shotWeight'),
                Max('shotWeight'),
                Min('shotWeight'),
                StdDev('shotWeight'))
    return partDict


def createJobReportDict(jobNumber, date_from=None, date_to=None):
    date_from, date_to = createDateRange(date_from=date_from, date_to=date_to)

    context_dic = {}

    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')

    try:
        inspectionTypes = PartInspection.objects.get(item_Number__item_Number=active_job[0].item)
    except ObjectDoesNotExist:
        raise Http404("No inspections types were set")


    context_dic['active_job'] = active_job

    # first_item = active_job[0]

    if inspectionTypes.visual_inspection:
        context_dic['visualInspection'] = visualInspection.objects.filter(jobID__jobNumber=jobNumber,
                                                                          dateCreated__range=(date_from, date_to))
        context_dic['InspectionDates'] = {}
        context_dic['InspectionDates'] = context_dic['visualInspection'].aggregate(Min('dateCreated'),
                                                                                   Max('dateCreated'))
        print context_dic['InspectionDates']
        ### Initialize dictionary for summary stats
        context_dic['visualInspectionDict'] = {}
        ### Count number of passed inspections
        context_dic['visualInspectionDict']['numPass'] = context_dic['visualInspection'].filter(
            inspectionResult=1).count()

        ### Count number of failed inspections
        context_dic['visualInspectionDict']['numFail'] = context_dic['visualInspection'].filter(
            inspectionResult=0).count()

        ### Calculate number of total inspections
        context_dic['visualInspectionDict']['totalInspections'] = context_dic['visualInspectionDict']['numPass'] + \
                                                                  context_dic['visualInspectionDict']['numFail']
        ### Calculate percentage passed
        if context_dic['visualInspectionDict']['totalInspections'] > 0:
            context_dic['visualInspectionDict']['passPerc'] = 100 * context_dic['visualInspectionDict']['numPass'] / + \
                context_dic['visualInspectionDict']['totalInspections']
        else:
            context_dic['visualInspectionDict']['passPerc'] = 0

    if inspectionTypes.part_weight_inspection:
        context_dic['partWeightInspection'] = partWeightInspection.objects.filter(jobID__jobNumber=jobNumber,
                                                                                  dateCreated__range=(
                                                                                      date_from, date_to))
        context_dic['partWeightInspectionDict'] = {}
        context_dic['partWeightInspectionDict'] = context_dic['partWeightInspection'].aggregate(Avg('partWeight'),
                                                                                                Max('partWeight'),
                                                                                                Min('partWeight'),
                                                                                                StdDev('partWeight'))

    if inspectionTypes.shot_weight_inspection:
        context_dic['shotWeightInspection'] = shotWeightInspection.objects.filter(jobID__jobNumber=jobNumber,
                                                                                  dateCreated__range=(
                                                                                      date_from, date_to))
        context_dic['shotWeightInspectionDict'] = {}
        context_dic['shotWeightInspectionDict'] = context_dic['shotWeightInspection'].aggregate(Avg('shotWeight'),
                                                                                                Max('shotWeight'),
                                                                                                Min('shotWeight'),
                                                                                                StdDev('shotWeight'))

    return context_dic


def createDateRange(date_from=None, date_to=None):
    if date_from is None:
        date_from = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
        date_from = timezone.make_aware(date_from, timezone.get_current_timezone())

    if date_to is None:
        date_to = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        date_to = timezone.make_aware(date_to, timezone.get_current_timezone())

    return (date_from, date_to)


def presetStandardFields(my_form):
    # this will preset machine and qa fields
    ### Filter the machine operators
    my_form.fields["machineOperator"].queryset = employee.objects.filter(organization_name__org_name='Machine Operator',
                                                                         shift_id=getShift())
    ### Filter the QA ladies
    my_form.fields["inspectorName"].queryset = employee.objects.filter(organization_name__org_name='QA',
                                                                       shift_id=getShift())

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
