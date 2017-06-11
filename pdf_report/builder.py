from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, \
    Spacer, PageBreak, Image, KeepTogether, LongTable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

from cStringIO import StringIO

BASE_FONT = "Times-Roman"
BASE_FONT_BOLD = 'Times-Bold'
BASE_FONT_SIZE = 9
IMAGE_ALIGN_CENTER = "CENTER"
PAGE_WIDTH = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]
PAGE_NUMBER_STR = "Page %d"


DOCUMENT_TITLE = "Job Report"
DOCUMENT_NUMBER = "QSR-752-538/Job"
DOCUMENT_DATE = "Rev A Dated 11/17/15"

STYLE_TITLE_PAGE_KEY = 'title_page'
STYLE_CENTER_TABLE_KEY = 'center_table'

class PDFReport(object):
    def __init__(self, document_title=None, document_number=None, document_date=None):
        self.document_title = document_title or DOCUMENT_TITLE
        self.document_number = document_number or DOCUMENT_NUMBER
        self.document_date = document_date or DOCUMENT_DATE
        self.styles = None
        self.story = []


    def _my_first_page(self, canvas, doc, date):
        canvas.saveState()
        canvas.setFont(BASE_FONT_BOLD, 16)
        canvas.setFont(BASE_FONT, 9)
        canvas.drawString(inch, 0.75 * inch, "%s" % self.document_number)
        canvas.drawString(PAGE_WIDTH / 2 - 0.25 * inch, 0.75 * inch,
                          PAGE_NUMBER_STR % doc.page)
        canvas.drawString(PAGE_WIDTH - 2 * inch, 0.75 * inch,
                          "%s" % date)
        canvas.restoreState()

    def _my_later_pages(self, canvas, doc, date):
        canvas.saveState()
        canvas.setFont(BASE_FONT, 9)
        canvas.drawString(inch, 0.75 * inch, "%s" % self.document_number)
        canvas.drawString(PAGE_WIDTH / 2 - 0.25 * inch, 0.75 * inch,
                          PAGE_NUMBER_STR % doc.page)
        canvas.drawString(PAGE_WIDTH - 2 * inch, 0.75 * inch,
                          "%s" % date)
        canvas.restoreState()

    def _document_styles(self, styles):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name=STYLE_TITLE_PAGE_KEY,
                                  alignment=TA_CENTER))
        styles.add(
            ParagraphStyle(name=STYLE_CENTER_TABLE_KEY,
                           alignment=TA_CENTER, fontSize=16))

    def _report_meta(self):
        pass

    def _add_image(self, image_path, image_align, story=None):
        story = story or self.story

        image = Image(image_path)
        image.hAlign = IMAGE_ALIGN_CENTER

        story.append(image)

    def _add_cover_page(self, cover_page_text, style, caption_spacer, story):
        story = story or self.story

        if caption_spacer:
            story.append(caption_spacer)

        story.append(Paragraph(cover_page_text, style))

        if caption_spacer:
            story.append(caption_spacer)


    def _add_table(self, table_style, table_data, style, story=None,
                   table_title=None, spacer=None):
        story = story or self.story

        if table_title:
            story.append(Paragraph(table_title, style))
            story.append(Spacer(1, 0.25 * inch))

        t = Table(table_data)
        t.setStyle(TableStyle(table_style))

        story.append(t)

        if spacer:
            story.append(spacer)

    def build_document(self, story=None):
        story = story or self.story
        tmp_file = StringIO()

        document = SimpleDocTemplate(tmp_file)
        document.build(story,
                       onFirstPage=self._my_first_page,
                       onLaterPages=self._my_later_pages)
        stringified_object = tmp_file.getvalue()
        tmp_file.close()
        return stringified_object
