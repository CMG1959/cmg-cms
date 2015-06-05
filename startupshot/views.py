from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import CIMC_Part, CIMC_Production


def index(request):
    latest_startupshot = CIMC_Production.objects.last()
    return HttpResponse("The last startup shot created is: Part:%s Job: %s" % \
                        (latest_startupshot.item, latest_startupshot.jobNumber))

def detailPart(request, part_number):
    currentPart = CIMC_Part.objects.get(item_Number=part_number)
    return HttpResponse("Part Detail: You're looking %s: %s" % (currentPart.item_Number,currentPart.item_Description))


def viewCreatedStartUpShot(request, part_number):
    item_id = CIMC_Part.objects.get(item_Number = part_number)
    different_shots = CIMC_Production.objects.filter(item_id = item_id.id)
    template = loader.get_template('startupshot/view.html')
    context = RequestContext(request, {
        'item' : item_id,
        'different_shot_list': different_shots,
        })
    return HttpResponse(template.render(context))

def createNewStartUpShot(request, part_number):
    return HttpResponse("You're creating a new startup shot for %s." % part_number)