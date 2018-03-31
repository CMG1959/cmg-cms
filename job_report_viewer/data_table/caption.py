from job_report_viewer.settings import *
from inspection.models import (passFailTest, numericTest,
    textRecord, RangeRecord)

class Caption(object):

    @classmethod
    def get_numeric(cls, primitive_id):
        inspection_instance = numericTest.objects.get(id=primitive_id)
        return inspection_instance.testName

    @classmethod
    def get_pass_fail(cls, primitive_id):
        inspection_instance = passFailTest.objects.get(id=primitive_id)
        return inspection_instance.testName

    @classmethod
    def get_range(cls, primitive_id):
        inspection_instance = RangeRecord.objects.get(id=primitive_id)
        return inspection_instance.testName

    @classmethod
    def get_text(cls, primitive_id):
        inspection_instance = textRecord.objects.get(id=primitive_id)
        return inspection_instance.testName

    @classmethod
    def get_cover(cls, primitive_id):
        pass

    @classmethod
    def get_statistics(cls, primitive_id):
        pass


    @classmethod
    def get(cls, table_type, primitive_id):
        if table_type == NUMERIC:
            return cls.get_numeric(primitive_id)
        elif table_type == PASS_FAIL:
            return cls.get_pass_fail(primitive_id)
        elif table_type == RANGE:
            return cls.get_range(primitive_id)
        elif table_type == TEXT:
            return cls.get_text(primitive_id)
        elif table_type == COVER:
            return COVER
        elif table_type == PHL:
            return PHL
        elif table_type == STATISTICS:
            return 'N-A'
        else:
            return 'N-A'