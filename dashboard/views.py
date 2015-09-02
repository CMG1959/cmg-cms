from django.shortcuts import render
from models import errorLog
import datetime
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import RequestContext, loader
from django.shortcuts import render
# Create your views here.

def view_errorLog(request):
    dt_yesterday = datetime.date.today()-datetime.timedelta(days=1)
    production_errors = errorLog.objects.filter(dateCreated__gte=dt_yesterday).order_by('-dateCreated')
    template = loader.get_template('dashboard/errorLog.html')
    context = RequestContext(request, {
        'prodErrors':production_errors
    })
    return HttpResponse(template.render(context))
