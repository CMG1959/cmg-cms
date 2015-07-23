from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.contrib.auth.decorators import login_required
from forms import phlLookup, phlForm, moldLookup, mhlForm
from startupshot.models import MattecProd, startUpShot
from employee.models import Employees
from molds.models import Mold
from .models import ProductionHistory, MoldHistory
import datetime


@login_required
def view_index(request):
    return render(request, 'phl/index.html')


@login_required
def view_phl_form(request):
    activeInMattec = MattecProd.objects.all().order_by('machNo')
    template = loader.get_template('phl/phl_index.html')
    context = RequestContext(request, {
        'activeInMattec': activeInMattec,
    })
    return HttpResponse(template.render(context))


@login_required
def view_mold_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = moldLookup(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            mold_Number = form.cleaned_data['mold_Number']
            redirect_url = '/production_and_mold_history/mold/%s' % (mold_Number)
            # redirect to a new URL:
        return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = moldLookup()
    return render(request, 'phl/forms/moldLookup.html', {'form': form})


@login_required
def view_specific_phl_form(request, jobNo):

    active_job = startUpShot.objects.filter(jobNumber=jobNo).select_related('item')
    #if not active_job.exists():
    #    raise Http404("Need a start-up shot before proceeding")


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = phlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            newForm = ProductionHistory(
                inspectorName=Employees.objects.get(pk=form.cleaned_data['inspectorName'].pk),
                jobNumber=startUpShot.objects.get(jobNumber=jobNo),
                descEvent=form.cleaned_data['descEvent'],
            )
            newForm.save()

        redirect_url = '/production_and_mold_history/production_report/%s' % (jobNo)
        # redirect to a new URL:
        return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = phlForm()
        form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6) | \
                                                Employees.objects.filter(EmpJob__JobNum=2) | \
                                                Employees.objects.filter(EmpJob__JobNum=1)


        context = RequestContext(request, {
            'form': form,
            'active_job': active_job,
        })
        return render(request, 'phl/forms/phlForm.html', context)


@login_required
def view_specific_mold_form(request, moldNo):
    try:
        mold_info = Mold.objects.get(mold_number=moldNo)
    except ObjectDoesNotExist:
        raise Http404("The mold has not been created in the system yet.")

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = mhlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            newForm = MoldHistory(
                inspectorName=Employees.objects.get(pk=form.cleaned_data['inspectorName'].pk),
                moldNumber=Mold.objects.get(mold_number=moldNo),
                descEvent=form.cleaned_data['descEvent'],
                pm=form.cleaned_data['pm'],
                repair=form.cleaned_data['repair'],
                hours_worked=form.cleaned_data['hours_worked'],
            )
            newForm.save()

        redirect_url = '/production_and_mold_history/mold_report/%s' % (moldNo)
        # redirect to a new URL:
        return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = mhlForm()
        form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=1)

    context = RequestContext(request, {
        'form': form,
        'mold_info': mold_info,
    })
    return render(request, 'phl/forms/moldForm.html', context)


@login_required
def view_phl_report_search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = phlLookup(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            jobNo = form.cleaned_data['job_Number']
            redirect_url = '/production_and_mold_history/production_report/%s' % (jobNo)
            # redirect to a new URL:
        return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = phlLookup()
    return render(request, 'phl/forms/phlLookup.html', {'form': form})


@login_required
def view_mold_report_search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = moldLookup(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            mold_Number = form.cleaned_data['mold_Number']
            redirect_url = '/production_and_mold_history/mold_report/%s' % (mold_Number)
            # redirect to a new URL:
        return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = moldLookup()

    return render(request, 'phl/forms/moldLookup.html', {'form': form})


@login_required
def view_phl_report(request, jobNo):
    start_up_info = startUpShot.objects.filter(jobNumber=jobNo)
    PHL = ProductionHistory.objects.filter(jobNumber__jobNumber=jobNo)
    print PHL
    context_dict = {'active_job': start_up_info, 'PHL': PHL}
    template = loader.get_template('phl/reports/phl.html')
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))


@login_required
def view_mold_report(request, moldNo):
    try:
        mold_info = Mold.objects.get(mold_number=moldNo)
    except ObjectDoesNotExist:
        raise Http404("The mold has not been created in the system yet.")

    MHL = MoldHistory.objects.filter(moldNumber__mold_number=moldNo)
    context_dict = {'mold_info': mold_info, 'MHL': MHL}
    template = loader.get_template('phl/reports/mhl.html')
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))


###### Helper functions #####


# def view_mold_report(request,moldNo):
def getShift():
    currentHour = datetime.datetime.time(datetime.datetime.now()).hour

    if (currentHour >= 7) and (currentHour < 15):
        shift = 1
    elif (currentHour >= 15) and (currentHour < 23):
        shift = 2
    else:
        shift = 3

    return shift
