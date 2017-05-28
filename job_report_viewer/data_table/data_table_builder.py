from settings import *
from inspection.models import passFailInspection, numericInspection, textInspection, RangeInspection
from production_and_mold_history.models  import ProductionHistory
from startupshot.models import startUpShot
from job_report_viewer.settings import *
import tzlocal
import pytz
import datetime
from django.db.models import ManyToManyField
from decimal import Decimal

class DataTableBuilder(object):
    local_tz = tzlocal.get_localzone()
    time_str = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def format_time(cls, datetime_obj):
        new_date_time_obj = datetime_obj.replace(tzinfo=pytz.utc).astimezone(DataTableBuilder.local_tz)
        return new_date_time_obj.strftime(DataTableBuilder.time_str)

    @classmethod
    def response(cls, queryset, settings_list):
        db_cols = [x[1] for x in settings_list]
        formatted_queryset = list(queryset)
        formatted_list = cls.format_queryset(formatted_queryset, db_cols)
        return {'data': formatted_list,
                'table_headers': cls.get_headers(settings_list)}

    @classmethod
    def get_headers(cls, settings_list):
        return [x[0] for x in settings_list]

    @classmethod
    def format_queryset(cls, queryset_list, db_cols):
        new_queryset_list = []
        for row in queryset_list:
            new_list = []
            for each_key in db_cols:
                val = getattr(row,each_key)
                if isinstance(val, datetime.datetime):
                    val = cls.format_time(val)
                elif isinstance(val, bool):
                    val = 'Pass' if val else 'Fail'
                elif isinstance(val, (float, int, Decimal)):
                    pass
                elif isinstance(val, (basestring)):
                    pass
                elif isinstance(row._meta.get_field(each_key), ManyToManyField):
                    items = [each_val.__unicode__() for each_val in val.all()]
                    if not items:
                        items = ['None']
                    items = ','.join(items)
                    val = items
                else:
                    val = val.__unicode__()
                new_list.append(val)
            new_queryset_list.append(new_list)
        return new_queryset_list

    @classmethod
    def get_numeric(cls, test_name_id, job_id, header):
        inspections = numericInspection.objects.filter(numericTestName_id=test_name_id,
                                                        jobID=job_id). \
            select_related(*INSPECTION_SELECT_RELATED)
        return cls.response(inspections, header)

    @classmethod
    def get_pass_fail(cls, test_name_id, job_id, header):
        inspections = passFailInspection.objects.filter(passFailTestName_id=test_name_id,
                                                        jobID = job_id).\
            select_related(*INSPECTION_SELECT_RELATED).\
            prefetch_related(*PREFETCH_PASS_FAIL)
        return cls.response(inspections, header)

    @classmethod
    def get_range(cls, test_name_id, job_id, header):
        inspections = RangeInspection.objects.filter(rangeTestName_id=test_name_id,
                                                       jobID=job_id). \
            select_related(*INSPECTION_SELECT_RELATED)
        return cls.response(inspections, header)

    @classmethod
    def get_text(cls, test_name_id, job_id, header):
        inspections = textInspection.objects.filter(textTestName_id=test_name_id,
                                                       jobID=job_id). \
            select_related(*INSPECTION_SELECT_RELATED)
        return cls.response(inspections, header)

    @classmethod
    def get_phl(cls, job_id, header):
        startup_shot = startUpShot.objects.get(id=job_id)
        inspections = ProductionHistory.objects.filter(jobNumber=startup_shot.jobNumber).select_related('inspectorName')
        return cls.response(inspections, header )

    @classmethod
    def get_data(cls, test_name_id, job_id, get_type):
        if get_type == NUMERIC:
            return cls.get_numeric(test_name_id, job_id, HEADER_NUMERIC)
        elif get_type == PASS_FAIL:
            return cls.get_pass_fail(test_name_id, job_id, HEADER_PASS_FAIL)
        elif get_type == RANGE:
            return cls.get_range(test_name_id, job_id, HEADER_RANGE)
        elif get_type == TEXT:
            return cls.get_text(test_name_id, job_id, HEADER_TEXT)
        elif get_type == PHL:
            return cls.get_phl(job_id, HEADER_PHL)
        else:
            pass