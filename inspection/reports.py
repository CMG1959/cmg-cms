__author__ = 'mike'

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, \
    Spacer, PageBreak, Image, KeepTogether, LongTable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

from cStringIO import StringIO
import textwrap
from collections import OrderedDict
import datetime
from django.utils import timezone
from models import passFailByPart, passFailTest, passFailInspection, \
    passFailTestCriteria, numericTestByPart, \
    numericInspection, textRecord, textRecordByPart, textInspection, \
    numericTest, RangeRecordByPart, RangeInspection
from startupshot.models import startUpShot
from production_and_mold_history.models import ProductionHistory
import numpy as np
from django.http import HttpResponse
import pytz as tz

from django.db.models import Min, Max
from job_report_viewer.inspection_summary.summary import InspectionSummary
from job_report_viewer.inspection_summary.numeric_summary import \
    NumericInspectionSummary


class JobReport:
    '''
    A class for generating both html and inspection reports
    '''

    def __init__(self, job_number, date_from=None, date_to=None):
        self.job_number = job_number
        self.job_number_id = startUpShot.objects.get(
            jobNumber=self.job_number).id
        self.date_from = date_from
        self.date_to = date_to
        self.inspection_date_range = {}
        self.summary_tables = OrderedDict()
        self.extended_tables = OrderedDict()
        self.inspection_summarized = []
        self.numeric_inspection_summarized = []
        self.__get_job_ids()
        self.date_range = self.__create_date_range()
        self.item_number = self.__get_item_number()
        self.__build_report()

    def __get_item_number(self):
        item = startUpShot.objects.get(jobNumber=self.job_number).item
        self.item_number_id = item.id
        return item.item_Number

    def _get_inspection_summary(self):
        inspections = InspectionSummary.get_data(self.job_number_id)
        table_data = InspectionSummary.get_table(inspections)
        wrapped_data = map(self._wrap_text, table_data['data'])

        self.inspection_summarized.append(table_data['table_headers'])
        self.inspection_summarized.extend(wrapped_data)


    def _get_numeric_summary(self):
        inspections = NumericInspectionSummary.get_numeric(self.job_number_id)
        table_data = NumericInspectionSummary.get_table(inspections)
        wrapped_data = map(self._wrap_text, table_data['data'])

        self.numeric_inspection_summarized.append(table_data['table_headers'])
        self.numeric_inspection_summarized.extend(wrapped_data)

    def _wrap_text(self, row):
        row[0] = textwrap.fill(row[0], 30)#.replace('\n', '<br />\n')
        return row

    def __get_job_ids(self):
        self.start_up_shot_ids = [each_id.id for each_id in
                                  startUpShot.objects.filter(
                                      jobNumber=self.job_number)]

    def __get_startup_shot(self):
        self.startup_shot = startUpShot.objects.get(jobNumber=self.job_number)
        self.startup_shot_report = [
            ['Inspector', 'Machine Operator', 'Mold Number', 'Active Cavities',
             'Shot Weight', 'Cycle Time'],
            [self.startup_shot.inspectorName, self.startup_shot.machineOperator,
             self.startup_shot.moldNumber,
             self.startup_shot.activeCavities, self.startup_shot.shotWeight,
             self.startup_shot.cycleTime]]

    def __get_job_info(self):
        self.job_info = [
            ['Job Number', 'Item Number', 'Item Description', 'Mold Number',
             'Mold Description',
             'Date Started', 'Date Ended'],
            [self.job_number, self.item_number,
             self.startup_shot.item.item_Description,
             self.startup_shot.moldNumber,
             self.startup_shot.moldNumber.mold_description,
             self.report_date_start.date(), self.report_date_end.date()]]
        self.job_info = map(list, zip(*self.job_info))

    def __get_date_range(self):
        my_inspection = []
        for inspection_primitive in [textInspection, passFailInspection,
                                     numericInspection]:
            qset = inspection_primitive.objects.filter(
                jobID__in=self.start_up_shot_ids). \
                aggregate(min_date=Min('dateCreated'),
                          max_date=Max('dateCreated'))
            my_inspection.append(qset['min_date'])
            my_inspection.append(qset['max_date'])

        if my_inspection:
            self.report_date_end = max(my_inspection)
            self.report_date_start = min(my_inspection)
        else:
            self.report_date_end = 'No Inspections'
            self.report_date_start = self.report_date_end

    def __make_local_str(self, date_time_obj):
        loc_time = timezone.localtime(date_time_obj)
        str_time = (loc_time).strftime('%Y-%m-%d %I:%M %p')
        return str_time

    def __create_date_range(self):
        if self.date_from is None:
            self.date_from = datetime.datetime.strptime('1900-01-01',
                                                        '%Y-%m-%d')
            self.date_from = timezone.make_aware(self.date_from,
                                                 timezone.get_current_timezone())

        if self.date_to is None:
            self.date_to = datetime.datetime.combine(datetime.date.today(),
                                                     datetime.time.max)
            self.date_to = timezone.make_aware(self.date_to,
                                               timezone.get_current_timezone())

        return self.date_from, self.date_to

    def __my_first_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        # canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-108, self.Title)
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "%s" % self.pageinfo)
        canvas.drawString(self.PAGE_WIDTH / 2 - 0.25 * inch, 0.75 * inch,
                          "Page %d" % doc.page)
        canvas.drawString(self.PAGE_WIDTH - 2 * inch, 0.75 * inch,
                          "%s" % self.dateinfo)
        #     canvas.showPage()
        canvas.restoreState()

    def __my_later_pages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "%s" % self.pageinfo)
        canvas.drawString(self.PAGE_WIDTH / 2 - 0.25 * inch, 0.75 * inch,
                          "Page %d" % doc.page)
        canvas.drawString(self.PAGE_WIDTH - 2 * inch, 0.75 * inch,
                          "%s" % self.dateinfo)
        canvas.restoreState()

    def __build_report(self):
        self.__get_startup_shot()
        self._get_inspection_summary()
        self._get_numeric_summary()
        self.__get_date_range()
        self.__get_job_info()

        self.PAGE_HEIGHT = defaultPageSize[1]
        self.PAGE_WIDTH = defaultPageSize[0]
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        self.styles.add(
            ParagraphStyle(name='titlePage', alignment=TA_CENTER, fontSize=16))
        self.Title = "Job Report"
        self.pageinfo = "QSR-752-538/Job"
        self.dateinfo = "Rev A Dated 11/17/15"

    def get_report(self):

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename="Job Report %s .pdf"' % str(
            self.job_number)
        tmp = StringIO()

        doc = SimpleDocTemplate(tmp)
        my_spacer = Spacer(1, 1 * inch)
        caption_spacer = Spacer(1, 0.25 * inch)

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
        t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
                               ('BOX', (0, 0), (-1, -1), 1, colors.black)
                               ]))
        Story.append(t)
        Story.append(PageBreak())

        ptext = 'Startup Shot'
        Story.append(Paragraph(ptext, self.styles['Center']))
        Story.append(caption_spacer)
        t = Table(self.startup_shot_report)
        t.setStyle(TableStyle([('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),
                               ]))
        Story.append(t)
        Story.append(my_spacer)

        ptext = 'Summary of Inspections'
        Story.append(Paragraph(ptext, self.styles['Center']))
        Story.append(caption_spacer)
        t = Table(self.inspection_summarized)
        t.setStyle(TableStyle([('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),
                               ]))
        Story.append(t)
        Story.append(my_spacer)

        if self.numeric_inspection_summarized:
            ptext = 'Summary of Numeric Inspections'
            Story.append(Paragraph(ptext, self.styles['Center']))
            Story.append(caption_spacer)
            t = Table(self.numeric_inspection_summarized)
            t.setStyle(TableStyle([('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),
                                   ]))
            Story.append(t)
            Story.append(my_spacer)

        #
        # ptext = 'Production History Log'
        # Story.append(Paragraph(ptext, self.styles['Center']))
        # Story.append(caption_spacer)
        #
        # commentParagraphStyle = ParagraphStyle("Comment", fontName="Helvetica", fontSize = 10, alignment=TA_LEFT)
        # phl_list = []
        # for row in self.phl:
        #     row_list = []
        #     for each_cell in row:
        #         row_list.append(Paragraph(each_cell,commentParagraphStyle))
        #     # row_list[-1] = textwrap.fill(row_list[-1],30).replace('\n','<br />\n')
        #     phl_list.append(row_list)
        #
        # # phl_text = [Paragraph(each_item, style) for row in self.phl for each_item in row]
        # t = LongTable(phl_list)
        # t.setStyle(TableStyle([('LINEABOVE',(0,1),(-1,1),1,colors.black),
        #         ]))
        # Story.append(t)
        # Story.append(my_spacer)

        doc.build(Story, onFirstPage=self.__my_first_page,
                  onLaterPages=self.__my_later_pages)
        # Get the data out and close the buffer cleanly
        pdf = tmp.getvalue()
        tmp.close()
        response.write(pdf)
        return response
