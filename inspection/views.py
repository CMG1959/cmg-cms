
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render
from django.db.models import Avg, Max, Min, StdDev

from models import partWeightInspection, visualInspection
from part.models import PartInspection
from startupshot.models import Production, MattecProd
from employee.models import cimc_organizations, employee
from molds.models import PartIdentifier
from forms import partWeightForm, visualInspectionForm, jobReportSearch, itemReportSearch


def view_index(request):
    activeInMattec = MattecProd.objects.all()

    # active_parts = Production.objects.filter(inProduction=True).select_related('item')

    template = loader.get_template('inspection/index.html')
    context = RequestContext(request, {
        'active_parts': activeInMattec,
        })
    return HttpResponse(template.render(context))


def view_detailJob(request, jobNumber):

    active_job = Production.objects.filter(jobNumber=jobNumber).select_related('item')
    inspectionTypes = PartInspection.objects.get(item_Number__item_Number=active_job[0].item)

    template = loader.get_template('inspection/detailJob.html')
    context = RequestContext(request, {
        'active_job' : active_job,
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
            redirect_url = '/inspection/jobReport/%s/' % (job_number)
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = jobReportSearch()

    return render(request, 'inspection/jobReportSearch.html', {'form': form})


def view_itemReportSearch(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = itemReportSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            part_number = form.cleaned_data['item_Number']
            redirect_url = '/inspection/itemReport/%s/' % (part_number)
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = itemReportSearch()

    return render(request, 'inspection/itemReportSearch.html', {'form': form})


def view_itemReport(request, itemNumber):

    inspectionTypes = PartInspection.objects.get(item_Number__item_Number=itemNumber)

    jobList = Production.objects.filter(item__item_Number=itemNumber)
    jobList = jobList.values_list('jobNumber', flat=True)
    partDict = {}
    n = 0
    for eachJob in jobList:
        dictID = 'Job%i' % (n)
        n += 1
        partDict[dictID] = {}
        partDict[dictID]['startupInfo'] = Production.objects.filter(jobNumber=eachJob).select_related('item')

        if inspectionTypes.visual_inspection:
            partDict[dictID]['visualInspectionDict'] = {}
            ### Count number of passed inspections
            partDict[dictID]['visualInspectionDict']['numPass'] = \
                visualInspection.objects.filter(jobID__jobNumber=eachJob, inspectionResult=1).count()
            ### Count number of failed inspections
            partDict[dictID]['visualInspectionDict']['numFail'] = \
                visualInspection.objects.filter(jobID__jobNumber=eachJob, inspectionResult=0).count()
            ### Calculate number of total inspections
            partDict[dictID]['visualInspectionDict']['totalInspections'] = partDict[dictID]['visualInspectionDict'][
                                                                               'numPass'] + \
                                                                           partDict[dictID]['visualInspectionDict'][
                                                                               'numFail']
            ### Calculate percentage passed
            if partDict[dictID]['visualInspectionDict']['totalInspections']>0:
                partDict[dictID]['visualInspectionDict']['passPerc'] = 100 * partDict[dictID]['visualInspectionDict'][
                    'numPass'] / partDict[dictID]['visualInspectionDict']['totalInspections']
            else:
                partDict[dictID]['visualInspectionDict']['passPerc']=0

        if inspectionTypes.weight_inspection:
            partDict[dictID]['partWeightInspection'] = partWeightInspection.objects.filter(jobID__jobNumber=eachJob)
            partDict[dictID]['partWeightInspectionDict'] = {}
            partDict[dictID]['partWeightInspectionDict'] = \
                partWeightInspection.objects.filter(jobID__jobNumber=eachJob).aggregate(Avg('partWeight'),
                                                                                        Max('partWeight'),
                                                                                        Min('partWeight'),
                                                                                        StdDev('partWeight'))

    context_dict = {}
    context_dict['partDict'] = partDict
    print context_dict

    template = loader.get_template('inspection/partReport.html')
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))



def view_jobReport(request, jobNumber):
    active_job = Production.objects.filter(jobNumber=jobNumber).select_related('item')

    inspectionTypes = PartInspection.objects.get(item_Number__item_Number=active_job[0].item)

    context_dic = {'active_job': active_job}

    # first_item = active_job[0]

    if inspectionTypes.visual_inspection:
        context_dic['visualInspection'] = visualInspection.objects.filter(jobID__jobNumber=jobNumber)
        ### Initialize dictionary for summary stats
        context_dic['visualInspectionDict'] = {}
        ### Count number of passed inspections
        context_dic['visualInspectionDict']['numPass'] = \
            visualInspection.objects.filter(jobID__jobNumber=jobNumber, inspectionResult=1).count()
        ### Count number of failed inspections
        context_dic['visualInspectionDict']['numFail'] = \
            visualInspection.objects.filter(jobID__jobNumber=jobNumber, inspectionResult=0).count()
        ### Calculate number of total inspections
        context_dic['visualInspectionDict']['totalInspections'] = context_dic['visualInspectionDict']['numPass'] + \
                                                                  context_dic['visualInspectionDict']['numFail']
        ### Calculate percentage passed
        if context_dic['visualInspectionDict']['totalInspections']>0:
            context_dic['visualInspectionDict']['passPerc'] = 100 * context_dic['visualInspectionDict']['numPass'] / + \
                context_dic['visualInspectionDict']['totalInspections']
        else:
            context_dic['visualInspectionDict']['passPerc'] = 0

    if inspectionTypes.weight_inspection:
        context_dic['partWeightInspection'] = partWeightInspection.objects.filter(jobID__jobNumber=jobNumber)
        context_dic['partWeightInspectionDict'] = {}
        context_dic['partWeightInspectionDict'] = \
            partWeightInspection.objects.filter(jobID__jobNumber=jobNumber).aggregate(Avg('partWeight'),
                                                                                      Max('partWeight'),
                                                                                      Min('partWeight'),
                                                                                      StdDev('partWeight'))

    template = loader.get_template('inspection/jobReport.html')
    context = RequestContext(request, context_dic)

    return HttpResponse(template.render(context))


def view_visualInspection(request, jobNumber):
    active_job = Production.objects.filter(jobNumber=jobNumber).select_related('item')
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
            initial={'jobID': Production.objects.get(jobNumber=jobNumber).id}
        )
        ### Filter the machine operators
        # machOp = cimc_organizations.objects.get(org_name='Machine Operator')
        form.fields["machineOperator"].queryset = employee.objects.filter(organization_name__org_name='Machine Operator')
        ### Filter the QA ladies
        # QA = cimc_organizations.objects.get(org_name='QA')
        form.fields["inspectorName"].queryset = employee.objects.filter(organization_name__org_name='QA')
        ### Filter the cavity and molds
        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(mold_number__mold_number=active_job[0].moldNumber)


    return render(request, 'inspection/visualInspection.html' , {'form': form, 'active_job':active_job})


def view_weightInspection(request, jobNumber):
    active_job = Production.objects.filter(jobNumber = jobNumber).select_related('item')
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
            initial={'jobID': Production.objects.get(jobNumber=jobNumber).id},
        )
        ### Filter the machine operators
        # machOp = cimc_organizations.objects.get(org_name='Machine Operator')
        form.fields["machineOperator"].queryset = employee.objects.filter(organization_name__org_name='Machine Operator')
        ### Filter the QA ladies
        # QA = cimc_organizations.objects.get(org_name='QA')
        form.fields["inspectorName"].queryset = employee.objects.filter(organization_name__org_name='QA')
        ### Filter the cavity and molds
        form.fields["headCavID"].queryset = PartIdentifier.objects.filter(mold_number__mold_number=active_job[0].moldNumber)
        ### lets see if we can change weight
        form.fields["partWeight"].min_value = 9

    return render(request, 'inspection/weightInspection.html', {'form': form, 'active_job': active_job})
