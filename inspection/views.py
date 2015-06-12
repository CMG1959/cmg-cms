
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render
from django.db.models import Q
from startupshot.models import  CIMC_Part, CIMC_Production
# from .forms import startupShotLookup, startupShotForm

# def index(request):
#     # template = loader.get_template('startupshot/index.html')
#     # return HttpResponse(template.render())
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = startupShotLookup(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             part_number = form.cleaned_data['part_Number']
#             redirect_url = '/startupshot/%s/viewCreated' % (part_number)
#             # redirect to a new URL:
#             return HttpResponseRedirect(redirect_url)
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = startupShotLookup()
#
#     return render(request, 'startupshot/index.html', {'form': form})


# def detailPart(request, part_number):
#     currentPart = CIMC_Part.objects.get(item_Number=part_number)
#     return HttpResponse("Part Detail: You're looking %s: %s" % (currentPart.item_Number,currentPart.item_Description))


def index(request):
    # item_id = CIMC_Part.objects.get(item_Number = part_number)
    # different_shots = CIMC_Production.objects.filter(item_id = item_id.id)
    active_parts = CIMC_Production.objects.filter(inProduction = True).select_related('item')

    template = loader.get_template('inspection/index.html')
    context = RequestContext(request, {
        'active_parts' : active_parts,
        })
    return HttpResponse(template.render(context))

def detailJob(request, jobNumber):
    active_job = CIMC_Production.objects.filter(jobNumber = jobNumber).select_related('item')

    template = loader.get_template('inspection/detailJob.html')
    context = RequestContext(request, {
        'active_job' : active_job,
        })
    return HttpResponse(template.render(context))

#
# def createNewStartUpShot(request):
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = startupShotForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             part_number = form.cleaned_data['item']
#             form.save()
#             # process the data in form.cleaned_data as required
#             redirect_url = '/startupshot/%s/viewCreated' % (part_number)
#             # redirect to a new URL:
#             return HttpResponseRedirect(redirect_url)
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = startupShotForm()
#
#     return render(request, 'startupshot/createStartupShot.html', {'form': form})