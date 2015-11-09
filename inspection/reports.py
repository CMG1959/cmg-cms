__author__ = 'mike'

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

from cStringIO import StringIO

from collections import OrderedDict
import datetime
from django.utils import timezone
from models import passFailByPart, passFailTest, passFailInspection, passFailTestCriteria, rangeTestByPart, \
    rangeInspection, textRecord, textRecordByPart, textInspection, rangeTest
from startupshot.models import startUpShot
from production_and_mold_history.models import ProductionHistory
import numpy as np
from django.http import HttpResponse


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
        self.text_summarized = [['Inspection Name', 'Pass', 'Fail', 'Total', 'Pass Percent']]
        self.range_summarized = [['Inspection Name', 'Count', 'Min', 'Max', 'Average', 'Std Dev']]
        self.date_range = self.__create_date_range()
        self.item_number = self.__get_item_number()
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

    def __get_job_info(self):
        self.job_info = [['Job Number','Item Number','Item Description','Mold Number','Mold Description',
                          'Date Started','Date Ended'],
                         [self.job_number,self.item_number,self.startup_shot.item.item_Description,
                          self.startup_shot.moldNumber,self.startup_shot.moldNumber.mold_description,
                          self.report_date_end, self.report_date_start]]
        self.job_info =  map(list, zip(*self.job_info))


        # <th>Item #</th>
        # <th>Description</th>
        # <th>TMM Part Weight (g)</th>
        # <th>TMM Cycle (s)</th>
        #
        #     <td>{{ active_job.0.item.item_Number }}</td>
        #     <td>{{ active_job.0.item.item_Description }}</td>
        #     <td>{{ active_job.0.item.exp_part_weight }}</td>
        #     <td>{{ active_job.0.item.exp_cycle_time }}</td>

    def __get_phl(self):
        self.phl = [['Date','Name','Description']]
        phl_info = ProductionHistory.objects.filter(jobNumber__jobNumber=self.job_number)
        for row in phl_info:
            self.phl.append([row.dateCreated, row.inspectorName, row.descEvent])


    def __get_range_inspections(self):
        self.range_inspections = OrderedDict()
        self.range_inspection_summary = OrderedDict()
        for each_inspection in self.required_inspections['range_inspections']:

            self.range_inspections.update({each_inspection.testName.testName:
                rangeInspection.objects.filter(
                    rangeTestName__testName=each_inspection.testName,
                    jobID__jobNumber=self.job_number,
                    dateCreated__range=self.date_range)})

            range_report = [['Date', 'Machine Operator', 'Inspector', 'Is Full Shot', 'Cavity', 'Numeric Value',
                             'Inspection Result']]
            for row in self.range_inspections[each_inspection.testName.testName]:
                range_report.append(
                    [row.dateCreated, row.machineOperator, row.inspectorName, row.isFullShot, row.headCavID, row.numVal,
                     row.inspectionResult])
            self.extended_tables.update({each_inspection.testName.testName: range_report})


            rangeList = []
            for eachShot in self.range_inspections[each_inspection.testName.testName]:
                if ((eachShot.isFullShot) and (not each_inspection.testName.calcAvg)):
                    rangeList.append(eachShot.numVal / self.startup_shot.activeCavities)
                else:
                    rangeList.append(float(eachShot.numVal))

            result_dict, result_list = self.__calc_range_stats(rangeList)

            range_id = [each_inspection.testName.testName]
            range_id.extend(result_list)
            self.range_summarized.append(range_id)
            self.range_inspection_summary.update({each_inspection.testName.testName: result_dict})

    def __get_pass_fail_inspections(self):
        self.pass_fail_inspections = OrderedDict()
        self.pass_fail_inspection_summary = OrderedDict()
        print self.required_inspections['pf_inspections']
        for each_inspection in self.required_inspections['pf_inspections']:

            self.pass_fail_inspections.update({each_inspection.testName.testName:
                passFailInspection.objects.filter(
                    passFailTestName__testName=each_inspection.testName.testName,
                    jobID__jobNumber=self.job_number,
                    dateCreated__range=self.date_range)})

            pass_fail_report = [['Date', 'Machine Operator', 'Inspector', 'Cavity', 'Inspection Result', 'Defect']]

            if self.pass_fail_inspections[each_inspection.testName.testName]:
                for row in self.pass_fail_inspections[each_inspection.testName.testName]:
                    if len(row.defectType.all())> 1:
                        pass_fail_report.append(
                            [row.dateCreated, row.machineOperator, row.inspectorName, row.headCavID, row.inspectionResult,
                              "\n".join([r.passFail for r in row.defectType.all()])])
                    else:
                        pass_fail_report.append(
                            [row.dateCreated, row.machineOperator, row.inspectorName, row.headCavID, row.inspectionResult,
                              " ".join([r.passFail for r in row.defectType.all()])])

                result_dict, result_list = self.__create_pf_stats(self.pass_fail_inspections[
                                                                          each_inspection.testName.testName])
                self.pass_fail_inspection_summary.update({each_inspection.testName.testName: result_dict})
            else:
                pass_fail_report.append(['None']*len(pass_fail_report[0]))
                result_list = ['None']*(len(self.pf_summarized[0])-1)

            self.extended_tables.update({each_inspection.testName.testName: pass_fail_report})

            pf_id = [each_inspection.testName.testName]
            pf_id.extend(result_list)
            self.pf_summarized.append(pf_id)


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
            print self.text_inspections[each_inspection.testName]

            for row in self.text_inspections[each_inspection.testName]['text_dict']:
                text_inspection.append(
                    [row.dateCreated, row.machineOperator, row.inspectorName, row.isFullShot, row.headCavID, row.inspectionResult])

            self.extended_tables.update({each_inspection.testName: text_inspection})

            if self.text_inspections[each_inspection.testName]['text_dict']:
                result_dict, result_list = self.__create_pf_stats(self.text_inspections[
                                                                   each_inspection.testName]['text_dict'])
            else:
                result_list = ['None']*(len(self.text_summarized[0])-1)

            text_id = [each_inspection.testName]
            text_id.extend(result_list)
            self.text_summarized.append(text_id)



    def __get_date_range(self):

        my_inspection = list(textInspection.objects.filter(jobID__jobNumber=self.job_number,dateCreated__range=self.date_range).values_list('dateCreated',flat=True))
        my_inspection.extend(list(passFailInspection.objects.filter(jobID__jobNumber=self.job_number,dateCreated__range=self.date_range).values_list('dateCreated',flat=True)))
        my_inspection.extend(list(rangeInspection.objects.filter(jobID__jobNumber=self.job_number,dateCreated__range=self.date_range).values_list('dateCreated',flat=True)))

        if my_inspection:
            self.report_date_end = max(my_inspection)
            self.report_date_start = min(my_inspection)
        else:
            self.report_date_end = 'No Inspections'
            self.report_date_start = self.report_date_end


    def __create_pf_stats(self, qSet):
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

        return result_dict, result_list



    def __calc_range_stats(self, range_list):
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

        return result_dict, [result_dict['range_count'],result_dict['range_min'],result_dict['range_max'],result_dict['range_avg'],result_dict['range_stddev'],]


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
        # canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-108, self.Title)
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
        self.__get_startup_shot()
        self.__get_required_inspections()
        self.__get_pass_fail_inspections()
        self.__get_range_inspections()
        self.__get_text_inspections()
        self.__get_date_range()
        self.__get_job_info()
        self.__get_phl()


        self.PAGE_HEIGHT=defaultPageSize[1]
        self.PAGE_WIDTH=defaultPageSize[0]
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(name='titlePage',alignment=TA_CENTER,fontSize=16))
        self.Title = "Job Report"
        self.pageinfo = "QSR-123-456"

    def get_report(self):

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Job Report %s .pdf"' % str(self.job_number)
        tmp = StringIO()

        doc = SimpleDocTemplate(tmp)
        my_spacer = Spacer(1,1*inch)
        caption_spacer = Spacer(1,0.25*inch)

        Story = []
        # Story = [my_spacer]

        style = self.styles["Normal"]
        im = Image('C:\CIMC_static\images\CMGlogo-white-small.jpeg')
        im.hAlign = 'CENTER'
        Story.append(im)

        Story.append(caption_spacer)
        ptext = 'Job Report'
        Story.append(Paragraph(ptext, self.styles['titlePage']))
        Story.append(caption_spacer)

        #### Do first page stuff
        t = Table(self.job_info)
        t.setStyle(TableStyle([('INNERGRID',(0,0),(-1,-1),1,colors.black),
                               ('BOX',(0,0),(-1,-1),1,colors.black)
                ]))
        Story.append(t)
        Story.append(PageBreak())


        ptext = 'Startup Shot'
        Story.append(Paragraph(ptext, self.styles['Center']))
        Story.append(caption_spacer)
        t = Table(self.startup_shot_report)
        t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
                ]))
        Story.append(t)
        Story.append(my_spacer)

        ptext = 'Summary of Range Tests'
        Story.append(Paragraph(ptext, self.styles['Center']))
        Story.append(caption_spacer)
        t = Table(self.range_summarized)
        t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
                ]))
        Story.append(t)
        Story.append(my_spacer)


        ptext = 'Summary of Pass Fail Tests'
        Story.append(Paragraph(ptext, self.styles['Center']))
        Story.append(caption_spacer)
        t = Table(self.pf_summarized)
        t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
                ]))
        Story.append(t)
        Story.append(my_spacer)


        ptext = 'Summary of other tests'
        Story.append(Paragraph(ptext, self.styles['Center']))
        Story.append(caption_spacer)
        t = Table(self.text_summarized)
        t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
                ]))
        Story.append(t)
        Story.append(my_spacer)


        ptext = 'Production History Log'
        Story.append(Paragraph(ptext, self.styles['Center']))
        Story.append(caption_spacer)
        t = Table(self.phl)
        t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
                ]))
        Story.append(t)
        Story.append(my_spacer)

        doc.build(Story, onFirstPage=self.__my_first_page, onLaterPages=self.__my_later_pages)
        # Get the data out and close the buffer cleanly
        pdf = tmp.getvalue()
        tmp.close()
        response.write(pdf)
        return response