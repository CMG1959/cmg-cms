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


class Summary(object):
    def __init__(self, name, inspection_type):
        self.name = name
        self.inspection_type = inspection_type
        self.number_passed = 0
        self.number_failed = 0
        self.total = 0

    def add_aggregation(self, inspection_result, count):
        if inspection_result:
            self.number_passed = count
        elif not inspection_result:
            self.number_failed = count
        else:
            pass

        self.total = self.number_failed + self.number_passed

    def get_report(self):
        return {report_name: getattr(self, name) for report_name, name in REPORT}


class InspectionSummary(object):

    @classmethod
    def response(self, queryset, inspection_col_name, inspection_type):
        queryset_dict = {}
        for each_query in queryset:
            inspection_name = each_query.get(inspection_col_name)

            if inspection_name not in queryset_dict:
                queryset_dict[inspection_name] = \
                    Summary(inspection_name, inspection_type)

            queryset_dict[inspection_name].add_aggregation(
                each_query.get(INSPECTION_RESULT),
                each_query.get('count_of')
            )
        return [v.get_report() for k,v in queryset_dict.iteritems()]

    @classmethod
    def get_numeric(cls, job_id):
        inspections = numericInspection.objects.\
            filter(jobID=job_id).\
            values(*INSPECTION_NUMERIC).\
            annotate(count_of=Count(INSPECTION_RESULT))
        return cls.response(inspections, INSPECTION_NUMERIC[0], NUMERIC)

    @classmethod
    def get_pass_fail(cls, job_id):
        inspections = passFailInspection.objects.\
            filter(jobID = job_id).\
            values(*INSPECTION_PASS_FAIL).\
            annotate(count_of=Count(INSPECTION_RESULT))
        return cls.response(inspections, INSPECTION_PASS_FAIL[0], PASS_FAIL)

    @classmethod
    def get_range(cls, job_id):
        inspections = RangeInspection.objects.\
            filter(jobID=job_id).\
            values(*INSPECTION_RANGE).\
            annotate(count_of=Count(INSPECTION_RESULT))
        return cls.response(inspections, INSPECTION_RANGE[0], RANGE)

    @classmethod
    def get_text(cls, job_id):
        inspections = textInspection.objects.\
            filter(jobID=job_id).\
            values(*INSPECTION_TEXT).\
            annotate(count_of=Count(INSPECTION_RESULT))

        [each_inspection.update({'inspectionResult': True})
            for each_inspection in inspections]

        return cls.response(inspections, INSPECTION_TEXT[0], TEXT)

    @classmethod
    def get_data(cls, job_id):
        inspections = []
        for anon_func, func_type in [(cls.get_numeric, NUMERIC ),
                                      (cls.get_pass_fail, PASS_FAIL),
                                      (cls.get_range, RANGE),
                                      (cls.get_text, TEXT)]:
            inspections.extend(anon_func(job_id))
        return inspections

    @classmethod
    def get_table(cls, inspections):
        header = [name for name, attr_ref in REPORT]
        body = [[each_inspection[name] for name in header] for each_inspection in inspections]
        return {'data': body, 'table_headers': header}