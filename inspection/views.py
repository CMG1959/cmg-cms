# Create your views here.
import datetime

from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.db.models import Avg, Max, Min, StdDev
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from models import partWeightInspection, visualInspection, shotWeightInspection, outsideDiameterInspection, \
    volumeInspection, \
    neckDiameterInspection, assemblyInspection, cartonTemperature, visionInspection
from part.models import PartInspection, Part
from startupshot.models import startUpShot, MattecProd
from employee.models import Employees
from molds.models import Mold,PartIdentifier
from forms import partWeightForm, visualInspectionForm, jobReportSearch, itemReportSearch, shotWeightForm, \
    outsideDiameterForm, volumeInspectionForm, neckDiameterForm, assemblyInspectionForm, cartonTempForm, \
    visionInspectionForm


######################################
#
#  Section for generating indexes, etc
#
######################################

@login_required
def view_index(request):
    activeInMattec = MattecProd.objects.all().order_by('machNo')


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

    inspectionTypes = PartInspection.objects.get(item_Number__item_Number=active_job[0].item)

    template = loader.get_template('inspection/detailJob.html')
    context = RequestContext(request, {
        'active_job': active_job,
        'inspectionTypes': inspectionTypes
    })
    return HttpResponse(template.render(context))


######################################
#
#  Section for generating forms
#
######################################


@login_required
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
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)
        ### Filter the cavity and molds
        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(
            mold_number__mold_number=active_job[0].moldNumber)

    return render(request, 'inspection/forms/visualInspection.html', {'form': form, 'active_job': active_job})


@login_required
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
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

        ### Filter the cavity and molds
        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(
            mold_number__mold_number=active_job[0].moldNumber)

    return render(request, 'inspection/forms/partWeightInspection.html', {'form': form, 'active_job': active_job})


@login_required
def view_shotWeightInspection(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = shotWeightForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            act_cav = MattecProd.objects.get(jobNumber=jobNumber)

            newForm = shotWeightInspection(
                jobID=startUpShot.objects.get(jobNumber=jobNumber),
                machineOperator=Employees.objects.get(pk=form.cleaned_data['machineOperator'].pk),
                inspectorName=Employees.objects.get(pk=form.cleaned_data['inspectorName'].pk),
                shotWeight=form.cleaned_data['shotWeight'],
                activeCavities=act_cav.activeCavities
            )
            # process the data in form.cleaned_data as required
            # part_number = form.cleaned_data['jobID']
            redirect_url = '/inspection/%s/' % (jobNumber)
            # save the data
            newForm.save()
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = shotWeightForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

    return render(request, 'inspection/forms/shotWeightInspection.html', {'form': form, 'active_job': active_job})


@login_required
def view_outsideDiameterInspection(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = outsideDiameterForm(request.POST)
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
        form = outsideDiameterForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

    return render(request, 'inspection/forms/shotWeightInspection.html', {'form': form, 'active_job': active_job})


@login_required
def view_volumeInspectionForm(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = volumeInspectionForm(request.POST)
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
        form = volumeInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

    return render(request, 'inspection/forms/shotWeightInspection.html', {'form': form, 'active_job': active_job})


@login_required
def view_neckDiameterForm(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = neckDiameterForm(request.POST)
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
        form = neckDiameterForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

    return render(request, 'inspection/forms/shotWeightInspection.html', {'form': form, 'active_job': active_job})


@login_required
def view_assemblyInspectionForm(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = assemblyInspectionForm(request.POST)
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
        form = assemblyInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

    return render(request, 'inspection/forms/shotWeightInspection.html', {'form': form, 'active_job': active_job})


@login_required
def view_cartonTempForm(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = cartonTempForm(request.POST)
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
        form = cartonTempForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

    return render(request, 'inspection/forms/shotWeightInspection.html', {'form': form, 'active_job': active_job})


@login_required
def view_visionInspectionForm(request, jobNumber):
    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = visionInspectionForm(request.POST)
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
        form = visionInspectionForm(
            initial={'jobID': startUpShot.objects.get(jobNumber=jobNumber).id},
        )
        form = presetStandardFields(form, jobID=jobNumber)
        ### Filter the machine operators
        # form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
        ### Filter the QA ladies
        # form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

    return render(request, 'inspection/forms/shotWeightInspection.html', {'form': form, 'active_job': active_job})


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

        if inspectionTypes.od_inspection:
            partDict[dictID]['od_inspection'] = outsideDiameterInspection.objects.filter(jobID__jobNumber=eachJob,
                                                                                         dateCreated__range=(
                                                                                             date_from, date_to))
            partDict[dictID]['od_inspectionDict'] = {}
            partDict[dictID]['od_inspectionDict'] = partDict[dictID]['od_inspection'].aggregate(
                Avg('outsideDiameter'),
                Max('outsideDiameter'),
                Min('outsideDiameter'),
                StdDev('outsideDiameter'))

        if inspectionTypes.vol_inspection:
            partDict[dictID]['vol_inspection'] = volumeInspection.objects.filter(jobID__jobNumber=eachJob,
                                                                                 dateCreated__range=(
                                                                                     date_from, date_to))
            partDict[dictID]['vol_inspectionDict'] = {}
            partDict[dictID]['vol_inspectionDict'] = partDict[dictID]['od_inspection'].aggregate(
                Avg('liquidWeight'),
                Max('liquidWeight'),
                Min('liquidWeight'),
                StdDev('liquidWeight'))

        if inspectionTypes.neck_diameter_inspection:
            partDict[dictID]['neckDiam_inspection'] = neckDiameterInspection.objects.filter(jobID__jobNumber=eachJob,
                                                                                            dateCreated__range=(
                                                                                                date_from, date_to))
            partDict[dictID]['neckDiam_inspectionDict'] = {}
            partDict[dictID]['neckDiam_inspectionDict']['numPass'] = partDict[dictID]['neckDiam_inspection'].filter(
                testResult=1).count()
            partDict[dictID]['neckDiam_inspectionDict']['numFail'] = partDict[dictID]['neckDiam_inspection'].filter(
                testResult=0).count()
            partDict[dictID]['neckDiam_inspectionDict']['totalInspections'] = \
            partDict[dictID]['neckDiam_inspectionDict']['numPass'] + \
            partDict[dictID]['neckDiam_inspectionDict']['numFail']

            ### Calculate percentage passed
            if partDict[dictID]['neckDiam_inspectionDict']['totalInspections'] > 0:
                partDict[dictID]['neckDiam_inspectionDict']['passPerc'] = 100 * \
                                                                          partDict[dictID]['neckDiam_inspectionDict'][
                                                                              'numPass'] / \
                                                                          partDict[dictID]['neckDiam_inspectionDict'][
                                                                              'totalInspections']
            else:
                partDict[dictID]['neckDiam_inspectionDict']['passPerc'] = 0

        if inspectionTypes.assembly_test_inspection:
            partDict[dictID]['assembly_inspection'] = assemblyInspection.objects.filter(jobID__jobNumber=eachJob,
                                                                                        dateCreated__range=(
                                                                                            date_from, date_to))
        if inspectionTypes.carton_temp_inspection:
            partDict[dictID]['cartonTemp_inspection'] = cartonTemperature.objects.filter(jobID__jobNumber=eachJob,
                                                                                         dateCreated__range=(
                                                                                             date_from, date_to))
            partDict[dictID]['cartonTemp_inspectionDict'] = {}
            partDict[dictID]['cartonTemp_inspectionDict'] = partDict[dictID]['cartonTemp_inspection'].aggregate(
                Avg('cartonTemp'),
                Max('cartonTemp'),
                Min('cartonTemp'),
                StdDev('cartonTemp'))

        if inspectionTypes.vision_system_inspection:
            partDict[dictID]['visionSys_inspection'] = visionInspection.objects.filter(jobID__jobNumber=eachJob,
                                                                                       dateCreated__range=(
                                                                                           date_from, date_to))


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

    if inspectionTypes.od_inspection:
        context_dic['od_inspection'] = outsideDiameterInspection.objects.filter(jobID__jobNumber=jobNumber,
                                                                                dateCreated__range=(
                                                                                    date_from, date_to))
        context_dic['od_inspectionDict'] = {}
        context_dic['od_inspectionDict'] = context_dic['od_inspection'].aggregate(
            Avg('outsideDiameter'),
            Max('outsideDiameter'),
            Min('outsideDiameter'),
            StdDev('outsideDiameter'))

    if inspectionTypes.vol_inspection:
        context_dic['vol_inspection'] = volumeInspection.objects.filter(jobID__jobNumber=jobNumber,
                                                                        dateCreated__range=(
                                                                            date_from, date_to))
        context_dic['vol_inspectionDict'] = {}
        context_dic['vol_inspectionDict'] = context_dic['od_inspection'].aggregate(
            Avg('liquidWeight'),
            Max('liquidWeight'),
            Min('liquidWeight'),
            StdDev('liquidWeight'))

    if inspectionTypes.neck_diameter_inspection:
        context_dic['neckDiam_inspection'] = neckDiameterInspection.objects.filter(jobID__jobNumber=jobNumber,
                                                                                   dateCreated__range=(
                                                                                       date_from, date_to))
        context_dic['neckDiam_inspectionDict'] = {}
        context_dic['neckDiam_inspectionDict']['numPass'] = context_dic['neckDiam_inspection'].filter(
            testResult=1).count()
        context_dic['neckDiam_inspectionDict']['numFail'] = context_dic['neckDiam_inspection'].filter(
            testResult=0).count()
        context_dic['neckDiam_inspectionDict']['totalInspections'] = context_dic['neckDiam_inspectionDict']['numPass'] + \
                                                                     context_dic['neckDiam_inspectionDict']['numFail']

        ### Calculate percentage passed
        if context_dic['neckDiam_inspectionDict']['totalInspections'] > 0:
            context_dic['neckDiam_inspectionDict']['passPerc'] = 100 * context_dic['neckDiam_inspectionDict'][
                'numPass'] / context_dic['neckDiam_inspectionDict']['totalInspections']
        else:
            context_dic['neckDiam_inspectionDict']['passPerc'] = 0

    if inspectionTypes.assembly_test_inspection:
        context_dic['assembly_inspection'] = assemblyInspection.objects.filter(jobID__jobNumber=jobNumber,
                                                                               dateCreated__range=(
                                                                                   date_from, date_to))
    if inspectionTypes.carton_temp_inspection:
        context_dic['cartonTemp_inspection'] = cartonTemperature.objects.filter(jobID__jobNumber=jobNumber,
                                                                                dateCreated__range=(
                                                                                    date_from, date_to))
        context_dic['cartonTemp_inspectionDict'] = {}
        context_dic['cartonTemp_inspectionDict'] = context_dic['cartonTemp_inspection'].aggregate(
            Avg('cartonTemp'),
            Max('cartonTemp'),
            Min('cartonTemp'),
            StdDev('cartonTemp'))

    if inspectionTypes.vision_system_inspection:
        context_dic['visionSys_inspection'] = visionInspection.objects.filter(jobID__jobNumber=jobNumber,
                                                                              dateCreated__range=(
                                                                                  date_from, date_to))


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


def presetStandardFields(my_form, jobID):
    # this will preset machine and qa fields
    ### Filter the machine operators
    my_form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9).order_by('EmpShift')
                                                                         # EmpShift=getShift())
    ### Filter the QA ladies
    my_form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6).order_by('EmpShift')
                                                                       # EmpShift=getShift())
    my_form.fields["jobID"].queryset = startUpShot.objects.filter(jobNumber=jobID)


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
    if not PartInspection.objects.filter(item_Number__item_Number=item_Number).exists():
        newPartInspection = PartInspection(item_Number = Part.objects.get(item_Number=item_Number))
        # will probably need to add a switch for CMC vs Canada
        newPartInspection.save()

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