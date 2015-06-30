from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render
from part.models import Part
from molds.models import Mold, PartIdentifier
from equipment.models import EquipmentInfo
from employee.models import employee
from .models import startUpShot, MattecProd
from .forms import startupShotLookup, startupShotForm

def index(request):
    # template = loader.get_template('startupshot/startUpShotSearch.html')
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


def viewActive(request):
    activeInMattec = MattecProd.objects.all()
    template = loader.get_template('startupshot/viewActive.html')
    context = RequestContext(request, {
        'activeInMattec': activeInMattec,
    })
    return HttpResponse(template.render(context))


def detailPart(request, part_number):
    currentPart = Part.objects.get(item_Number=part_number)
    return HttpResponse("Part Detail: You're looking %s: %s" % (currentPart.item_Number,currentPart.item_Description))


def viewCreatedStartUpShot(request, part_number):
    item_id = Part.objects.get(item_Number=part_number)
    different_shots = startUpShot.objects.filter(item_id=item_id.id)
    template = loader.get_template('startupshot/view.html')
    context = RequestContext(request, {
        'item' : item_id,
        'different_shot_list': different_shots,
        })
    return HttpResponse(template.render(context))


def createNewStartUpShot(request, jobNo):
    MattecInfo = MattecProd.objects.get(jobNumber=jobNo)

    # print Part.objects.get(item_Number=MattecInfo.itemNo)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = startupShotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print form.cleaned_data['inspectorName'].pk
            # head, cavID = str(form.cleaned_data.get('headCavID')).replace(" ", "").split('-')

            newForm = startUpShot(item=Part.objects.get(item_Number=MattecInfo.itemNo), \
                                  jobNumber=jobNo,\
                                 moldNumber=Mold.objects.get(mold_number=MattecInfo.moldNumber),\
                                 # headCavID=PartIdentifier.objects.get(mold_number__mold_number=MattecInfo.moldNumber,
                                 #                                      head_code=head, cavity_id=cavID), \
                                 inspectorName=employee.objects.get(pk=form.cleaned_data['inspectorName'].pk),\
                                 shotWeight=form.cleaned_data['shotWeight'],\
                                 activeCavities=MattecInfo.activeCavities, \
                                  cycleTime=MattecInfo.cycleTime, \
                                  machNo=EquipmentInfo.objects.get(part_identifier=MattecInfo.machNo))

            newForm.save()
            # process the data in form.cleaned_data as required
            redirect_url = '/startupshot/%s/viewCreated' % (MattecInfo.itemNo)
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_url)
    # if a GET (or any other method) we'll create a blank form
    else:
        if startUpShot.objects.filter(jobNumber=jobNo).exists():
            redirect_url = '/startupshot/%s/viewCreated' % (MattecInfo.itemNo)
            return HttpResponseRedirect(redirect_url)

        else:
            form = startupShotForm()

    return render(request, 'startupshot/createStartupShot.html', {'form': form, 'MattecDict': MattecInfo})
