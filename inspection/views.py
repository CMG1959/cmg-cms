
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render

from models import partWeightInspection, visualInspection
from startupshot.models import CIMC_Production
from employee.models import cimc_organizations, employee
from forms import partWeightForm, visualInspectionForm


def view_index(request):
    # item_id = CIMC_Part.objects.get(item_Number = part_number)
    # different_shots = CIMC_Production.objects.filter(item_id = item_id.id)
    active_parts = CIMC_Production.objects.filter(inProduction = True).select_related('item')

    template = loader.get_template('inspection/index.html')
    context = RequestContext(request, {
        'active_parts' : active_parts,
        })
    return HttpResponse(template.render(context))


def view_detailJob(request, jobNumber):
    active_job = CIMC_Production.objects.filter(jobNumber = jobNumber).select_related('item')

    template = loader.get_template('inspection/detailJob.html')
    context = RequestContext(request, {
        'active_job' : active_job,
        })
    return HttpResponse(template.render(context))


def view_jobReport(request, jobNumber):
    active_job = CIMC_Production.objects.filter(jobNumber = jobNumber).select_related('item')

    context_dic = {'active_job': active_job}

    first_item = active_job[0]

    if first_item.item.visual_inspection:
        context_dic['visualInspection'] = visualInspection.objects.filter(jobID__jobNumber=jobNumber)
    if first_item.item.weight_inspection:
        context_dic['partWeightInspection'] = partWeightInspection.objects.filter(jobID__jobNumber=jobNumber)

    template = loader.get_template('inspection/jobReport.html')
    context = RequestContext(request, context_dic)

    return HttpResponse(template.render(context))


def view_visualInspection(request, jobNumber):
    active_job = CIMC_Production.objects.filter(jobNumber=jobNumber).select_related('item')
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
            initial={'jobID':CIMC_Production.objects.get(jobNumber=jobNumber).id}
        )
        ### Filter the machine operators
        machOp = cimc_organizations.objects.get(org_name='Machine Operator')
        form.fields["machineOperator"].queryset = employee.objects.filter(organization_name=machOp.id)
        ### Filter the QA ladies
        QA = cimc_organizations.objects.get(org_name='QA')
        form.fields["inspectorName"].queryset = employee.objects.filter(organization_name=QA.id)

    return render(request, 'inspection/visualInspection.html' , {'form': form, 'active_job':active_job})


def view_weightInspection(request, jobNumber):
    active_job = CIMC_Production.objects.filter(jobNumber = jobNumber).select_related('item')
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
            initial={'jobID':CIMC_Production.objects.get(jobNumber=jobNumber).id}
        )
        ### Filter the machine operators
        machOp = cimc_organizations.objects.get(org_name='Machine Operator')
        form.fields["machineOperator"].queryset = employee.objects.filter(organization_name=machOp.id)
        ### Filter the QA ladies
        QA = cimc_organizations.objects.get(org_name='QA')
        form.fields["inspectorName"].queryset = employee.objects.filter(organization_name=QA.id)

    return render(request, 'inspection/weightInspection.html', {'form': form, 'active_job': active_job})
