from settings import *
from inspection.models import passFailInspection, numericInspection, textInspection, RangeInspection
from production_and_mold_history.models  import ProductionHistory
from startupshot.models import startUpShot
from job_report_viewer.settings import *
import tzlocal
import pytz
import datetime
from django.db.models import StdDev, Avg, Min, Max
from decimal import Decimal

class NumericInspectionSummary(object):

    @classmethod
    def get_numeric(cls, job_id):
        inspections = numericInspection.objects.\
            filter(jobID=job_id).\
            values(*SUMMARY_NUMERIC).\
            annotate(min=Min(SUMMARY_NUMERIC_ID),
                     max=Max(SUMMARY_NUMERIC_ID),
                     std=StdDev(SUMMARY_NUMERIC_ID),
                     mean=Avg(SUMMARY_NUMERIC_ID))
        return inspections

    @classmethod
    def get_data(cls, job_id):
        inspections = cls.get_numeric(job_id)
        return inspections

    @classmethod
    def get_table(cls, inspections):
        header = [name for name, attr_ref in SUMMARY_NUMERIC_REPORT]
        body = []
        for each_inspection in inspections:
            row = []
            for name in [attr_ref for name, attr_ref in SUMMARY_NUMERIC_REPORT]:
                cell = each_inspection[name]
                if isinstance(cell, (float, Decimal, int)):
                    cell = '%1.3f' % (cell)
                row.append(cell)
            body.append(row)

        return {'data': body, 'table_headers': header}

