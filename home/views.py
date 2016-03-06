# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect



@login_required
def index_redirect(request):
    return HttpResponseRedirect('/QMS')



@login_required
def index(request):
    return render_to_response('home/index.html', context_instance=RequestContext(request))
