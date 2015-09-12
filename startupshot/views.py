from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from part.models import Part
from molds.models import Mold
from equipment.models import EquipmentInfo
from employee.models import Employees
from inspection.models import rangeTestByPart
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
            # process the data in form.cleaned_data as required
            part_number = form.cleaned_data['part_Number']
            redirect_url = '/startupshot/%s/viewCreated' % (part_number)
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = startupShotLookup()

    return render(request, 'startupshot/startUpShotSearch.html', {'form': form})


@login_required
def viewActive(request):
    activeInMattec = MattecProd.objects.all().order_by('machNo')
    template = loader.get_template('startupshot/viewActive.html')
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
    })
    return HttpResponse(template.render(context))


@login_required
def createNewStartUpShot(request, jobNo):
    MattecInfo = MattecProd.objects.get(jobNumber=jobNo)
    PartInfo = Part.objects.get(item_Number=MattecInfo.itemNo)

    shotWeightName = startUpShotWeightLinkage.objects.all()[0]

    rangeInfo = rangeTestByPart.objects.filter(testName__testName=shotWeightName.testName,item_Number__item_Number=MattecInfo.itemNo.trim())

    if rangeInfo.exists():
            min_val=rangeInfo.rangeMin
            max_val=rangeInfo.rangeMax
    else:
            min_val=0
            max_val=999999.999


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = startupShotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print form.cleaned_data['inspectorName'].pk
            # head, cavID = str(form.cleaned_data.get('headCavID')).replace(" ", "").split('-')

            newForm = startUpShot(item=Part.objects.get(item_Number=MattecInfo.itemNo), \
                                  jobNumber=jobNo, \
                                  moldNumber=Mold.objects.get(mold_number=MattecInfo.moldNumber), \
                                  inspectorName=Employees.objects.get(pk=form.cleaned_data['inspectorName'].pk), \
                                  machineOperator=Employees.objects.get(pk=form.cleaned_data['machineOperator'].pk), \
                                  shotWeight=form.cleaned_data['shotWeight'], \
                                  activeCavities=MattecInfo.activeCavities, \
                                  cycleTime=MattecInfo.cycleTime, \
                                  machNo=EquipmentInfo.objects.filter(part_identifier=MattecInfo.machNo)[0])


            newForm.save()
            # process the data in form.cleaned_data as required
            redirect_url = '/startupshot/%s/viewCreated' % (MattecInfo.itemNo.strip())
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)
    # if a GET (or any other method) we'll create a blank form
    else:
        if startUpShot.objects.filter(jobNumber=jobNo).exists():
            redirect_url = '/startupshot/%s/viewCreated' % (MattecInfo.itemNo.strip())
            return HttpResponseRedirect(redirect_url)

        else:
            form = startupShotForm()
            form.fields["machineOperator"].queryset = Employees.objects.filter(EmpJob__JobNum=9)
            form.fields["inspectorName"].queryset = Employees.objects.filter(EmpJob__JobNum=6)

    return render(request, 'startupshot/createStartupShot.html',
                  {'form': form, 'MattecDict': MattecInfo,
                    'PartInfo': PartInfo,
                    'num_id':'#id_shotWeight',
                    'min_val':min_val,
                    'max_val':max_val
                   })
