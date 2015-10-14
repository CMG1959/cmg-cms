__author__ = 'mike'
from startupshot.models import startUpShot
from collections import OrderedDict
import datetime
from django.utils import timezone
from models import passFailByPart, passFailTest, passFailInspection, passFailTestCriteria, rangeTestByPart, \
    rangeInspection, textRecord, textRecordByPart, textInspection, rangeTest
from startupshot.models import startUpShot
import numpy as np


class JobReport:
    '''
    A class for generating both html and inspection reports
    '''

    def __init__(self, job_number, date_from=None, date_to=None):
        self.job_number = job_number
        self.date_from = date_from
        self.date_to = date_to
        self.inspection_date_range = {}
        self.date_range = self.__create_date_range()
        self.item_number = self.__get_item_number()
        self.__get_startup_shot()
        self.__get_required_inspections()
        self.__get_pass_fail_inspections()
        self.__get_range_inspections()
        self.__get_text_inspections()

    def __get_item_number(self):
        return startUpShot.objects.get(jobNumber=self.job_number).item.item_Number

    def __get_required_inspections(self):
        self.required_inspections = OrderedDict({
            'pf_inspections': passFailByPart.objects.filter(item_Number__item_Number=self.item_number),
            'range_inspections': rangeTestByPart.objects.filter(item_Number__item_Number=self.item_number),
            'text_inspections': textRecordByPart.objects.filter(item_Number__item_Number=self.item_number)
        })

    def __get_startup_shot(self):
        self.startup_shot = startUpShot.objects.get(jobNumber=self.job_number)

    def __get_range_inspections(self):
        self.range_inspections = OrderedDict()
        self.range_inspection_summary = OrderedDict()
        for each_inspection in self.required_inspections['range_inspections']:
            self.range_inspections.update({each_inspection.test_name.test_name:
                rangeInspection.objects.filter(
                    rangeTestName__testName=each_inspection.testName,
                    jobID__jobNumber=self.job_number,
                    dateCreated__range=self.date_range)})
            self.range_inspection_summary.update({each_inspection.test_name.test_name:
                                                      self.__calc_range_stats(
                                                          self.range_inspections[each_inspection.test_name.test_name])})

    def __get_pass_fail_inspections(self):
        self.pass_fail_inspections = OrderedDict()
        self.pass_fail_inspection_summary = OrderedDict()
        for each_inspection in self.required_inspections['pf_inspections']:
            self.pass_fail_inspections.update({each_inspection.test_name.test_name:
                passFailInspection.objects.filter(
                    passFailTestName__testName=each_inspection.testName.testName,
                    jobID__jobNumber=self.job_number,
                    dateCreated__range=self.date_range)})
            self.pass_fail_inspection_summary.update({each_inspection.test_name.test_name:
                                                          self.__create_pf_stats(self.pass_fail_inspections[
                                                                                     each_inspection.test_name.test_name])})

    def __get_text_inspections(self):
        self.text_inspections = OrderedDict()
        for each_inspection in self.required_inspections['text_inspections']:
            self.text_inspections.update({each_inspection.testName: {
                'testName': each_inspection.testName,
                'textDict': textInspection.objects.filter( \
                    textTestName__testName=each_inspection.testName,
                    jobID__jobNumber=self.job_number,
                    dateCreated__range=self.date_range)}})

    def __create_pf_stats(qSet):
        result_dict = {}
        if qSet:
            result_dict = {
                'numPass': qSet.filter(inspectionResult=1).count(),
                'numFail': qSet.filter(inspectionResult=0).count()}
            result_dict['totalInspections'] = result_dict['numPass'] + result_dict['numFail']
            if result_dict['totalInspections'] > 0:
                result_dict['passPerc'] = 100 * result_dict['numPass'] / result_dict['totalInspections']
            else:
                result_dict['passPerc'] = 0

        return result_dict

    def __calc_range_stats(range_list):
        if range_list:
            resultDict = {
                'range_list__count': '%i' % (len(range_list)),
                'range_list__min': '%1.3f' % (np.amin(range_list)),
                'range_list__max': '%1.3f' % (np.amax(range_list)),
                'range_list__avg': '%1.3f' % (np.mean(range_list)),
                'range_list__stddev': '%1.3f' % (np.std(range_list))
            }
        else:
            resultDict = {
                'range_list__count': '%i' % (0),
                'range_list__min': '%1.3f' % (0),
                'range_list__max': '%1.3f' % (0),
                'range_list__avg': '%1.3f' % (0),
                'range_list__stddev': '%1.3f' % (0)
            }
        return resultDict

    def __create_date_range(self):
        if self.date_from is None:
            self.date_from = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
            self.date_from = timezone.make_aware(self.date_from, timezone.get_current_timezone())

        if self.date_to is None:
            self.date_to = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            self.date_to = timezone.make_aware(self.date_to, timezone.get_current_timezone())

        return self.date_from, self.date_to
