# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


@login_required
class Index(TemplateView):
    template_name= "home/index.html"