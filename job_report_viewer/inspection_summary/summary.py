from settings import *
from inspection.models import passFailInspection, numericInspection, textInspection, RangeInspection
from production_and_mold_history.models  import ProductionHistory
from startupshot.models import startUpShot
from job_report_viewer.settings import *
import tzlocal
import pytz
import datetime
from django.db.models import Count, StdDev, Avg
from decimal import Decimal

INSPECTION_RESULT = 'inspectionResult'

class InspectionSummary(object):

    @classmethod
    def response(cls, queryset, settings_list):
        db_cols = settings_list[0]
        print queryset
        formatted_list = queryset
        return formatted_list

    @classmethod
    def get_headers(cls, settings_list):
        return [x[0] for x in settings_list]

    @classmethod
    def agg_count(cls, queryset):
        pass

    @classmethod
    def get_numeric(cls, job_id):
        inspections = numericInspection.objects.\
            filter(jobID=job_id).\
            values(*INSPECTION_NUMERIC).\
            annotate(count_of=Count(INSPECTION_RESULT))
        return cls.response(inspections, INSPECTION_NUMERIC)

    @classmethod
    def get_pass_fail(cls, job_id):
        inspections = passFailInspection.objects.\
            filter(jobID = job_id).\
            values(*INSPECTION_PASS_FAIL).\
            annotate(count_of=Count(INSPECTION_RESULT))
        return cls.response(inspections, INSPECTION_PASS_FAIL)

    @classmethod
    def get_range(cls, job_id):
        inspections = RangeInspection.objects.\
            filter(jobID=job_id).\
            values(*INSPECTION_RANGE)
        return cls.response(inspections, INSPECTION_RANGE)

    @classmethod
    def get_text(cls, job_id):
        inspections = textInspection.objects.\
            filter(jobID=job_id).\
            values(*INSPECTION_TEXT)
        return cls.response(inspections, INSPECTION_TEXT)

    @classmethod
    def get_phl(cls, job_id, header):
        startup_shot = startUpShot.objects.get(id=job_id)
        inspections = ProductionHistory.objects.filter(jobNumber=startup_shot.jobNumber).select_related('inspectorName')
        return cls.response(inspections, header )

    @classmethod
    def get_data(cls, job_id):
        inspections = {}
        for anon_func, func_type in [(cls.get_numeric, NUMERIC ),
                                      (cls.get_pass_fail, PASS_FAIL),
                                      (cls.get_range, RANGE),
                                      (cls.get_text, TEXT)]:
            inspections.update({func_type: anon_func(job_id)})
        return inspections