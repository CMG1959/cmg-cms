from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from part.models import Part
from molds.models import Mold
from equipment.models import EquipmentInfo
from employee.models import Employees
from inspection.models import numericTestByPart
from .models import startUpShot, MattecProd, startUpShotWeightLinkage
from .forms import startupShotLookup, startupShotForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    # return HttpResponse(template.render())
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = startupShotLookup(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return HttpResponseRedirect(reverse('start_up_shot_part_entries',
                                                args=[form.
                                                cleaned_data['part_Number']]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = startupShotLookup()

    return render(request, 'startupshot/start_up_shot_search.html', {'form': form})


@login_required
def viewActive(request):
    activeInMattec = MattecProd.objects.all().order_by('machNo')
    template = loader.get_template('startupshot/view_active.html')
    context = RequestContext(request, {
        'activeInMattec': activeInMattec,
    })
    return HttpResponse(template.render(context))


@login_required
def detailPart(request, part_number):
    currentPart = Part.objects.get(item_Number=part_number)
    return HttpResponse("Part Detail: You're looking %s: %s" % (currentPart.item_Number, currentPart.item_Description))


@login_required
def viewCreatedStartUpShot(request, part_number):

    try:
        item_id = Part.objects.get(item_Number=part_number)
    except ObjectDoesNotExist:
        raise Http404("Part number does not exist")

    different_shots = startUpShot.objects.filter(item_id=item_id.id)
    template = loader.get_template('startupshot/view.html')
    context = RequestContext(request, {
        'item': item_id,
        'different_shot_list': different_shots,
        'list_many': True
    })
    return HttpResponse(template.render(context))


@login_required
def create_new_start_up_shot(request):
    job_number = request.GET.get('job_number', -1)
    machine_number = request.GET.get('machine_number',-1)

    part_in_mattec = MattecProd.objects.get(jobNumber=job_number,
                                        machNo=machine_number)
    part = Part.objects.get(item_Number=part_in_mattec.itemNo)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = startupShotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            is_user = get_user_info(request.user.webappemployee.EmpNum)

            if is_user:

                newForm = startUpShot(item=part_info, \
                                      jobNumber=job_number, \
                                      moldNumber=Mold.objects.get(mold_number=part_in_mattec.moldNumber), \
                                      inspectorName=is_user,\
                                      machineOperator=Employees.objects.get(pk=form.cleaned_data['machineOperator'].pk), \
                                      shotWeight=form.cleaned_data['shotWeight'], \
                                      activeCavities=part_in_mattec.activeCavities, \
                                      cycleTime=part_in_mattec.cycleTime, \
                                      machNo=EquipmentInfo.objects.get(part_identifier=part_in_mattec.machNo))
                newForm.save()
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('start_up_shot_part_entries',
                                                args=[part_in_mattec.itemNo.strip()]))
        # if a GET (or any other method) we'll create a blank form
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))
    else:
        if startUpShot.objects.filter(jobNumber=job_number).exists():
            HttpResponseRedirect(reverse('start_up_shot_part_entries',
                                         args=[part_in_mattec.itemNo.strip()]))
        else:
            form = startupShotForm()
            form.fields["machineOperator"].queryset = Employees.objects.filter(StatusActive=True, IsOpStaff=True).order_by('EmpShift').order_by('EmpLName')

            shotWeightName = startUpShotWeightLinkage.objects.all()[0] #

            rangeInfo = numericTestByPart.objects.filter(testName__testName=shotWeightName.susName.testName, item_Number__item_Number=part_in_mattec.itemNo)

            if rangeInfo.exists():
                    min_val=rangeInfo[0].rangeMin
                    max_val=rangeInfo[0].rangeMax
            else:
                    min_val=0
                    max_val=999999.999

            return render(request, 'startupshot/create_startup_shot.html',
                          {'form': form, 'MattecDict': part_in_mattec,
                            'part_info': part_info,
                            'num_id':'#id_shotWeight',
                            'min_val':min_val,
                            'max_val':max_val
                           })

def get_user_info(man_num):
    try:
        this_user = Employees.objects.get(EmpNum=man_num)
    except Employees.DoesNotExist:
        this_user = None
    return this_user
