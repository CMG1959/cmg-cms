__author__ = 'mike'

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

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
        self.summary_tables = OrderedDict()
        self.extended_tables = OrderedDict()
        self.pf_summarized = [['Inspection Name', 'Pass', 'Fail', 'Total', 'Pass Percent']]
        self.range_summarized = [['Inspection Name', 'Count', 'Min', 'Max', 'Average', 'Std Dev']]
        self.date_range = self.__create_date_range()
        self.item_number = self.__get_item_number()
        self.__get_startup_shot()
        self.__get_required_inspections()
        self.__get_pass_fail_inspections()
        self.__get_range_inspections()
        self.__get_text_inspections()
        self.__get_date_range()



        self.PAGE_HEIGHT=defaultPageSize[1]
        self.PAGE_WIDTH=defaultPageSize[0]
        self.styles = getSampleStyleSheet()
        self.Title = "Job Report"
        self.pageinfo = "QSR-123-456"
        self.__build_report()

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
        self.startup_shot_report = [
            ['Inspector', 'Machine Operator', 'Mold Number', 'Active Cavities', 'Shot Weight', 'Cycle Time'],
            [self.startup_shot.inspectorName, self.startup_shot.machineOperator, self.startup_shot.moldNumber,
             self.startup_shot.activeCavities, self.startup_shot.shotWeight, self.startup_shot.cycleTime]]

    def __get_range_inspections(self):
        self.range_inspections = OrderedDict()
        self.range_inspection_summary = OrderedDict()
        for each_inspection in self.required_inspections['range_inspections']:

            self.range_inspections.update({each_inspection.test_name.test_name:
                rangeInspection.objects.filter(
                    rangeTestName__testName=each_inspection.testName,
                    jobID__jobNumber=self.job_number,
                    dateCreated__range=self.date_range)})

            range_report = [['Date', 'Machine Operator', 'Inspector', 'Is Full Shot', 'Cavity', 'Numeric Value',
                             'Inspection Result']]
            for row in self.range_inspections[each_inspection.test_name.test_name]:
                range_report.append(
                    [row.dateCreated, row.machineOperator, row.inspectorName, row.isFullShot, row.headCavID, row.numVal,
                     row.inspectionResult])
            self.extended_tables.update({each_inspection.test_name.test_name: range_report})

            result_dict, result_list = self.__calc_range_stats(
                self.range_inspections[each_inspection.test_name.test_name])

            self.range_summarized.append(result_list)
            self.range_inspection_summary.update({each_inspection.test_name.test_name: result_dict})

    def __get_pass_fail_inspections(self):
        self.pass_fail_inspections = OrderedDict()
        self.pass_fail_inspection_summary = OrderedDict()
        for each_inspection in self.required_inspections['pf_inspections']:
            self.pass_fail_inspections.update({each_inspection.test_name.test_name:
                passFailInspection.objects.filter(
                    passFailTestName__testName=each_inspection.testName.testName,
                    jobID__jobNumber=self.job_number,
                    dateCreated__range=self.date_range)})

            pass_fail_report = [['Date', 'Machine Operator', 'Inspector', 'Cavity', 'Inspection Result', 'Defect']]
            for row in self.pass_fail_inspections[each_inspection.test_name.test_name]:
                pass_fail_report.append(
                    [row.dateCreated, row.machineOperator, row.inspectorName, row.headCavID, row.inspectionResult,
                     row.defectType])
            self.extended_tables.update({each_inspection.test_name.test_name: pass_fail_report})

            result_dict, result_list = self.__create_pf_stats(self.pass_fail_inspections[
                                                                  each_inspection.test_name.test_name])
            self.pf_summarized.append(result_list)
            self.pass_fail_inspection_summary.update({each_inspection.test_name.test_name: result_dict})

    def __get_text_inspections(self):
        self.text_inspections = OrderedDict()
        for each_inspection in self.required_inspections['text_inspections']:
            self.text_inspections.update({each_inspection.testName: {
                'test_name': each_inspection.testName,
                'text_dict': textInspection.objects.filter( \
                    textTestName__testName=each_inspection.testName,
                    jobID__jobNumber=self.job_number,
                    dateCreated__range=self.date_range)}})

            text_inspection = [['Date', 'Machine Operator', 'Inspector', 'Full Shot?', 'Cav ID', 'Inspection Result']]
            for row in self.text_inspections[each_inspection.test_name]:
                text_inspection.append(
                    [row.dateCreated, row.machineOperator, row.inspectorName, row.headCavID, row.inspectionResult,
                     row.defectType])

            self.extended_tables.update({each_inspection.test_name: text_inspection})

    def __get_date_range(self):

        my_inspections = textInspection.objects.filter(jobID__jobNumber=self.job_number,dateCreated__range=self.date_range).values_list('dateCreated')
        my_inspections.append(passFailInspection.objects.filter(jobID__jobNumber=self.job_number,dateCreated__range=self.date_range).values_list('dateCreated'))
        my_inspections.append(rangeInspection.objects.filter(jobID__jobNumber=self.job_number,dateCreated__range=self.date_range).values_list('dateCreated'))
        self.report_date_end = max(my_inspections)
        self.report_date_start = min(my_inspections)


    def __create_pf_stats(qSet):
        result_dict = {}
        if qSet:
            result_dict = OrderedDict({
                'num_pass': qSet.filter(inspectionResult=1).count(),
                'num_fail': qSet.filter(inspectionResult=0).count()})
            result_dict.update({'total_inspections': result_dict['num_pass'] + result_dict['num_fail']})
            if result_dict['total_inspections'] > 0:
                result_dict.update({'pass_perc': 100 * result_dict['num_pass'] / result_dict['total_inspections']})
            else:
                result_dict.update({'pass_perc': 0})

        result_list = []
        for k, v in result_dict.iteritems():
            result_list.append(v)

        return result_dict

    def __calc_range_stats(range_list):
        if range_list:
            result_dict = OrderedDict({
                'range_count': '%i' % (len(range_list)),
                'range_min': '%1.3f' % (np.amin(range_list)),
                'range_max': '%1.3f' % (np.amax(range_list)),
                'range_avg': '%1.3f' % (np.mean(range_list)),
                'range_stddev': '%1.3f' % (np.std(range_list))
            })
        else:
            result_dict = OrderedDict({
                'range_count': '%i' % (0),
                'range_min': '%1.3f' % (0),
                'range_max': '%1.3f' % (0),
                'range_avg': '%1.3f' % (0),
                'range_stddev': '%1.3f' % (0)
            })

        result_list = []
        for k, v in result_dict.iteritems():
            result_list.append(v)

        return result_dict, result_list


    def __create_date_range(self):
        if self.date_from is None:
            self.date_from = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
            self.date_from = timezone.make_aware(self.date_from, timezone.get_current_timezone())

        if self.date_to is None:
            self.date_to = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            self.date_to = timezone.make_aware(self.date_to, timezone.get_current_timezone())

        return self.date_from, self.date_to

    def __my_first_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold',16)
        canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-108, self.Title)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch,"%s" % self.pageinfo)
    #     canvas.showPage()
        canvas.restoreState()



    def __my_later_pages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch,"%s: Page %d" % (self.pageinfo, doc.page))
        canvas.restoreState()


    def __build_report(self):
        doc = SimpleDocTemplate("phello.pdf")
        Story = [Spacer(1,2*inch)]
        style = self.styles["Normal"]

        #### Do first page stuff
        sus_info = [['date','name'],['Today!','Mike']]
        t = Table(sus_info)
        t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
                ]))

        Story.append(t)
        Story.append(Spacer(1,0.2*inch))
        part_info = [['part number','part name'],['123-456789','Some part']]
        t = Table(part_info)
        t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
                ]))

        Story.append(t)
        Story.append(PageBreak())

        my_header = ['col1','col2','col3']
        my_data = [my_header]
        for x in range(3):
            new_list = []
            for y in range(3):
                new_list.append(str(y))
            my_data.append(new_list)

        table_names = ['Startup shot','shot weight','visual inspections']
        table_data = [my_data, my_data, my_data]

        for n in range(len(table_names)):
            p = Paragraph(table_names[n],style)
            Story.append(p)
            Story.append(Spacer(1,0.2*inch))
            t = Table(table_data[n])
            t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
                ]))
            Story.append(t)

        doc.build(Story, onFirstPage=self.__my_first_page(), onLaterPages=self.__my_later_pages())

