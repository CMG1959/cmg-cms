from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render
# Create your views here.
from forms import phlLookup, phlForm, moldLookup, mhlForm
from startupshot.models import MattecProd, startUpShot
from employee.models import employee
from molds.models import Mold
from .models import ProductionHistory, MoldHistory

def view_index(request):
    return render(request, 'phl/index.html')

def view_phl_form(request):
    activeInMattec = MattecProd.objects.all()
    template = loader.get_template('phl/phl_index.html')
    context = RequestContext(request, {
        'activeInMattec': activeInMattec,
    })
    return HttpResponse(template.render(context))

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

def view_specific_phl_form(request, jobNo):
    activeInMattec = MattecProd.objects.get(jobNumber=jobNo)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = phlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            newForm = ProductionHistory(
                inspectorName=employee.objects.get(pk=form.cleaned_data['inspectorName'].pk),
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

    context = RequestContext(request, {
        'form':form,
        'activeInMattec': activeInMattec,
    })
    return render(request,'phl/forms/phlForm.html',context)

def view_specific_mold_form(request,moldNo):
    specific_mold = Mold.objects.get(mold_number=moldNo)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = mhlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            newForm = MoldHistory(
                inspectorName=employee.objects.get(pk=form.cleaned_data['inspectorName'].pk),
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

    context = RequestContext(request, {
        'form':form,
        'specific_mold': specific_mold,
    })
    return render(request,'phl/forms/moldForm.html',context)


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

def view_phl_report(request,jobNo):
    start_up_info = startUpShot.objects.filter(jobNumber=jobNo)
    PHL = ProductionHistory.objects.filter(jobNumber__jobNumber=jobNo)
    print PHL
    context_dict = {'active_job':start_up_info,'PHL':PHL}
    template = loader.get_template('phl/reports/phl.html')
    context = RequestContext(request,context_dict)
    return HttpResponse(template.render(context))

def view_mold_report(request,moldNo):
    mold_info = Mold.objects.get(mold_number = moldNo)
    MHL = MoldHistory.objects.filter(moldNumber__mold_number=moldNo)
    context_dict = {'mold_info':mold_info,'MHL':MHL}
    template = loader.get_template('phl/reports/mhl.html')
    context = RequestContext(request,context_dict)
    return HttpResponse(template.render(context))



# def view_mold_report(request,moldNo):
