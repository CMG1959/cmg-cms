# Create your views here.
import collections
import datetime
import json
import re
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, StdDev
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.urlresolvers import reverse

from dashboard.models import errorLog
from employee.models import Employees, EmployeeAtWorkstation
from equipment.models import EquipmentInfo
from inspection.models import *
from molds.models import Mold, PartIdentifier
from part.models import Part
from production_and_mold_history.models import ProductionHistory
from startupshot.models import startUpShot, MattecProd
from job_report_viewer.inspection_tree.branch import TreeBuilder
from inspection_coverpage.cover import CoverPageBuilder
from django.http import JsonResponse
from data_table.data_table_builder import DataTableBuilder
from inspection_summary.summary import InspectionSummary
from data_table.caption import Caption

class JobReportBase(TemplateView):
    template_name = 'job_report_viewer/job_report_base.html'

    def get_context_data(self, **kwargs):
        job_number = self.request.GET.get('job_number')
        context = super(JobReportBase, self).get_context_data(**kwargs)
        context['job_number'] = job_number
        return context

def cover_page(request):
    template_name = 'job_report_viewer/cover_page.html'

    job_number_id = request.GET.get('job_number_id')
    start_up_shot = startUpShot.objects.get(id=job_number_id)
    cover_page_data = CoverPageBuilder(start_up_shot.item_id, start_up_shot)

    html_context = render_to_string(template_name, {'cover_page': cover_page_data})
    js_context = None

    return JsonResponse({'html': html_context, 'js': js_context})

class CoverPage(TemplateView):
    template_name = 'job_report_viewer/data_table_base.html'

    def get_context_data(self, **kwargs):
        job_number_id = self.request.GET.get('job_number_id')
        start_up_shot = startUpShot.objects.get(id=job_number_id)
        context = super(CoverPage, self).get_context_data(**kwargs)
        context['cover_page'] = CoverPageBuilder(start_up_shot.item_id, start_up_shot)
        return context

def data_table_view(request):
    template_name = 'job_report_viewer/data_table_base.html'

    # http: // cmg - vis01 / JobReportViewer / DataTable?job_number_id = 1167 & primitive_id = 10 & type = Pass - Fail
    job_number_id = request.GET.get('job_number_id')
    primitive_id = request.GET.get('primitive_id')
    primitive_type = request.GET.get('type')

    data_table_builder = DataTableBuilder.get_data(primitive_id, job_number_id, primitive_type)

    html_context = render_to_string(template_name, {'table_headers': data_table_builder['table_headers'],
                                                    'caption': Caption.get(primitive_type, primitive_id)})

    return JsonResponse({'html': html_context, 'data': data_table_builder['data']})

def data_table_summary_view(request):
    template_name = 'job_report_viewer/data_table_base.html'

    job_number_id = request.GET.get('job_number_id')
    primitive_id = request.GET.get('primitive_id')
    primitive_type = request.GET.get('type')

    summary = InspectionSummary.get_data(job_number_id)
    summary_builder = InspectionSummary.get_table(summary)

    html_context = render_to_string(template_name, {'table_headers': summary_builder['table_headers'],
                                                    'caption': 'Inspection Summary'})

    return JsonResponse({'html': html_context, 'data': summary_builder['data']})


def plots(request):
    pass


def get_tree(request):
    job_number = request.GET.get('job_number')
    start_up_shot = startUpShot.objects.get(jobNumber=job_number)

    url_cover_page = reverse('cover_page')
    url_data_table = reverse('data_table')
    url_plots = reverse('plots')
    url_summary = reverse('data_table_summary')

    tree = TreeBuilder(start_up_shot.item_id, start_up_shot.id, url_cover_page,
                       url_data_table, url_plots, url_summary)
    return JsonResponse(tree.get_json(), safe=False)