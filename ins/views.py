from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.
from startupshot.models import MattecProd


@login_required
def view_index(request):
    activeInMattec = MattecProd.objects.order_by('machNo').all()

    template = loader.get_template('ins/index.html')
    context = RequestContext(request, {
        'active_parts': activeInMattec,
    })
    return HttpResponse(template.render(context))


def view_job(request):
    job_number = request.GET.get('job_number','-1')
    return True