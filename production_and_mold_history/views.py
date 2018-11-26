from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.contrib.auth.decorators import login_required
from forms import phlLookup, phlForm, moldLookup, mhlForm, moldLookupForm
from startupshot.models import MattecProd, startUpShot
from employee.models import Employees
from molds.models import Mold
from part.models import Part
from equipment.models import EquipmentInfo
from equipment.models import EquipmentInfo
from .models import ProductionHistory, MoldHistory, MaintenanceRequests
import datetime
from django.utils import timezone
from sql_sp import call_phl_insert_sp

@login_required
def view_index(request):
    return render(request, 'phl/index.html')


@login_required
def view_tooling_requests(request):
    dt_time = datetime.date.today()-datetime.timedelta(days=10)
    phl_list = ProductionHistory.objects.filter(notifyToolroom=True, dateCreated__gte=dt_time).values('dateCreated','jobNumber','inspectorName__EmpLMName','descEvent').order_by('-dateCreated')

    report_list = []
    for phl_item in phl_list:
        susInfo = startUpShot.objects.filter(jobNumber = phl_item['jobNumber'])
        if susInfo:
            moldNo = susInfo[0].moldNumber.mold_number
            machNo = susInfo[0].machNo
        else:
            mattec_info = MattecProd.objects.filter(jobNumber= phl_item['jobNumber'])
            if mattec_info[0]:
                moldNo = mattec_info[0].moldNumber
                machNo = mattec_info[0].machNo
            else:
                moldNo = 'N/A'
                machNo = 'N/A'

        report_list.append({
            'moldNo':moldNo,
            'machNo':machNo,
            'dateCreated':phl_item['dateCreated'],
            'inspectorName': phl_item['inspectorName__EmpLMName'],
            'descEvent':phl_item['descEvent']
        })

    template = loader.get_template('phl/reports/mhl_request.html')
    context = RequestContext(request, {
            'reportList': report_list
        })

    return HttpResponse(template.render(context))



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
        form = moldLookupForm()
        activeInMattec = MattecProd.objects.all().order_by('machNo')
        return render(request, 'phl/forms/moldLookup.html', {'form': form, 'activeInMattec':activeInMattec})



@login_required
def view_specific_phl_form(request, jobNo):

    active_job = startUpShot.objects.filter(jobNumber=jobNo).select_related('item')
    mattec_prod = MattecProd.objects.filter(jobNumber=jobNo)
    sta = 0 # preset machine number
    if mattec_prod[0]:
        machInfo = EquipmentInfo.objects.filter(part_identifier=mattec_prod[0].machNo, is_active=True)
        if machInfo:
            sta = machInfo[0].id

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = phlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:

                # process the data in form.cleaned_data as required
                newForm = ProductionHistory(
                    inspectorName=is_user,
                    jobNumber=jobNo.strip(),
                    descEvent=form.cleaned_data['descEvent'],
                    STA_Reported=sta,
                    Prod_shift=getShift(),
                    Prod_Date=timezone.localtime(timezone.now()).date(),
                    notifyToolroom = form.cleaned_data['notifyToolroom']
                )
                newForm.save()

                if form.cleaned_data['notifyToolroom']:
                    pass

                redirect_url = '/production_and_mold_history/production_report/%s' % (jobNo)
                # redirect to a new URL:
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))


    # if a GET (or any other method) we'll create a blank form
    else:
        form = phlForm()

        context = RequestContext(request, {
            'form': form,
            'active_job': active_job,
            'list_many': True
        })
        return render(request, 'phl/forms/phlForm.html', context)


@login_required
def view_specific_phl_form_sp(request, jobNo):

    active_job = startUpShot.objects.filter(jobNumber=jobNo).select_related('item')
    mattec_prod = MattecProd.objects.filter(jobNumber=jobNo)
    sta = 0 # preset machine number
    if mattec_prod[0]:
        machInfo = EquipmentInfo.objects.filter(part_identifier=mattec_prod[0].machNo, is_active=True)
        if machInfo:
            sta = machInfo[0].id

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = phlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                args = (
                    is_user.DeviceToken, # Device Token
                    sta, # STA Name
                    datetime.datetime.utcnow(), #.strftime('%Y-%m-%d %H:%M:%S'), # UTC Time Now
                    form.cleaned_data['descEvent'], # Event Description
                    jobNo.strip(), # Job Number
                    0, # Copy MHL
                    0, # Copy EHL
                    0 # Is Mold PM
                )

                try:
                    result = call_phl_insert_sp(args)
                except Exception as e:
                    raise Http404(str(e))

                redirect_url = '/production_and_mold_history/production_report/%s' % (jobNo)
                # redirect to a new URL:
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))


    # if a GET (or any other method) we'll create a blank form
    else:
        form = phlForm()

        context = RequestContext(request, {
            'form': form,
            'active_job': active_job,
            'list_many': True
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

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            if is_user:
                # process the data in form.cleaned_data as required
                newForm = MoldHistory(
                    Date_Performed=form.cleaned_data['Date_Performed'],
                    inspectorName= is_user.EmpLMName,
                    moldNumber=moldNo,
                    descEvent=form.cleaned_data['descEvent'],
                    pm=form.cleaned_data['pm'],
                    repair=form.cleaned_data['repair'],
                    hours_worked=form.cleaned_data['hours_worked'],
                )
                newForm.save()

                redirect_url = '/production_and_mold_history/mold_report/%s' % (moldNo)
                # redirect to a new URL:
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = mhlForm()

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
            item_type = form.cleaned_data['item_type']
            item_id = form.cleaned_data['id_Number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            date_from, date_to = createDateRange(date_from, date_to)
            my_dict = {}

            n = 1
            if item_type == 'Job Number':
                my_dict[str(n)] = {}
                my_dict[str(n)]['sus'] = startUpShot.objects.filter(jobNumber=item_id)
                my_dict[str(n)]['phl'] = ProductionHistory.objects.filter(jobNumber=item_id, \
                                                                          dateCreated__range=(date_from, date_to)).values('dateCreated','jobNumber','inspectorName__EmpLMName','descEvent').order_by('-dateCreated')
                context_dict = {'my_dict': my_dict,
                                'list_many': True}
                template = loader.get_template('phl/reports/phl.html')
                context = RequestContext(request, context_dict)

            else:
                # mold list
                active_list = startUpShot.objects.filter(moldNumber__mold_number=item_id).order_by('-dateCreated')
                my_dict = {'sus':[],'phl':[]}
                for eachJob in active_list:
                    my_dict['sus'].append(eachJob)
                    for each_entry in ProductionHistory.objects.filter(jobNumber=eachJob.jobNumber, \
                                                                              dateCreated__range=(date_from, date_to)).values('dateCreated','jobNumber','inspectorName__EmpLMName','descEvent').order_by('-dateCreated'):
                        my_dict['phl'].append(each_entry)
                    # my_dict[str(n)]['phl'] = ProductionHistory.objects.filter(jobNumber=eachJob.jobNumber, \
                    #                                                           dateCreated__range=(date_from, date_to)).values('dateCreated','jobNumber','inspectorName__EmpLMName','descEvent').order_by('-dateCreated')
                    # n += 1

                context_dict = {'my_dict': my_dict,
                                'list_many': True}
                template = loader.get_template('phl/reports/phl_by_mold.html')
                context = RequestContext(request, context_dict)
            # Return new page
            return HttpResponse(template.render(context))


    # if a GET (or any other method) we'll create a blank form
    else:
        form = phlLookup()
        activeInMattec = MattecProd.objects.all().order_by('machNo')
        return render(request, 'phl/forms/phlLookup.html', {'form': form, 'activeInMattec': activeInMattec})


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
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            # Format date range
            date_from, date_to = createDateRange(date_from, date_to)
            # Get information from DB
            mold_info = Mold.objects.get(mold_number=mold_Number)
            MHL = MoldHistory.objects.filter(moldNumber=mold_Number,
                                             dateCreated__range=(date_from, date_to)).order_by('-Date_Performed')
            # Format dictionaries
            context_dict = {'mold_info': mold_info, 'MHL': MHL}
            template = loader.get_template('phl/reports/mhl.html')
            context = RequestContext(request, context_dict)
            # Return new page
            return HttpResponse(template.render(context))
            # redirect_url = '/production_and_mold_history/mold_report/%s' % (mold_Number)
            # redirect to a new URL:
            # return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = moldLookup()
        activeInMattec = MattecProd.objects.all().order_by('machNo')
        return render(request, 'phl/forms/moldReportLookup.html', {'form': form, 'activeInMattec': activeInMattec})


@login_required
def view_phl_report(request, jobNo):
    n = 1
    my_dict={}
    my_dict[str(n)] = {}
    my_dict[str(n)]['sus'] = startUpShot.objects.filter(jobNumber=jobNo).order_by('-dateCreated')
    my_dict[str(n)]['phl'] = ProductionHistory.objects.filter(jobNumber=jobNo).values('dateCreated','jobNumber','inspectorName__EmpLMName','descEvent').order_by('-dateCreated')
    context_dict = {'my_dict': my_dict,
                    'list_many': True}
    template = loader.get_template('phl/reports/phl.html')
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))


@login_required
def view_mold_report(request, moldNo):
    try:
        mold_info = Mold.objects.get(mold_number=moldNo)
    except ObjectDoesNotExist:
        raise Http404("The mold has not been created in the system yet.")

    MHL = MoldHistory.objects.filter(moldNumber=moldNo).order_by('-Date_Performed')


    context_dict = {'mold_info': mold_info, 'MHL': MHL}
    # context_dict = {'my_dict':my_dict}
    template = loader.get_template('phl/reports/mhl.html')
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))


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

# def view_mold_report(request,moldNo):
def getShift():
    currentHour = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    currentHour = datetime.datetime.time(currentHour).hour

    if (currentHour >= 7) and (currentHour < 15):
        shift = 1
    elif (currentHour >= 15) and (currentHour < 23):
        shift = 2
    else:
        shift = 3

    return shift

def get_user_info(man_num):
    try:
        this_user = Employees.objects.get(EmpNum=man_num)
    except Employees.DoesNotExist:
        this_user = None
    return this_user
    