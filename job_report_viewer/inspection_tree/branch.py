from inspection.models import (passFailByPart, numericTestByPart,
    textRecordByPart, RangeRecordByPart)
from collections import OrderedDict
from job_report_viewer.settings import NUMERIC, PASS_FAIL, PHL, RANGE, TEXT, COVER, STATISTICS



class Node(object):

    def __init__(self, primitive_id, job_number_id, name, type, url):
        self.id = None
        self.text = name
        self.type = type
        self.data = {'url': "{0}?job_number_id={1}&primitive_id={2}&type={3}".format(url,
                                                                                    job_number_id,
                                                                                    primitive_id,
                                                                                    type)}
        self.children = []

    def to_jstree(self):
        return {'id': self.id,
                'text': self.text,
                'type': self.type,
                'data': self.data,
                'children': self.children }



class Branch(object):

    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def to_jstree(self):
        js_tree = {}
        js_tree.update({'text': self.name, 'children' : []})
        for node in self.nodes:
            js_tree['children'].append(node.to_jstree())
        return js_tree

class TreeBuilder(object):

    def __init__(self, item_number_id, job_number_id, cover_page_url, data_table_url, plots_url):
        self.job_number_id = job_number_id
        self.item_number_id = item_number_id
        self.url_cover_page = cover_page_url
        self.url_data_table = data_table_url
        self.url_plots = plots_url
        self.branch_cover_page = Branch(COVER)
        self.branch_pass_fail = Branch(PASS_FAIL)
        self.branch_numeric = Branch(NUMERIC)
        self.branch_text = Branch(TEXT)
        self.branch_range = Branch(RANGE)
        self.build_tree(item_number_id, job_number_id)

    def get_cover_page(self, item_number_id, job_number_id):
        new_node = Node(item_number_id, job_number_id, 'Cover', COVER, self.url_cover_page)
        self.branch_cover_page.add_node(new_node)

    def get_pass_fail_inspections(self, item_number_id, job_number_id):
        for inspection in passFailByPart.objects.filter(item_Number_id=item_number_id).order_by('testName__testName'):
            new_node = Node(inspection.testName_id, self.job_number_id, inspection.testName.testName, PASS_FAIL, self.url_data_table)
            self.branch_pass_fail.add_node(new_node)

    def get_numeric_inspections(self, item_number_id, job_number_id):
        for inspection in numericTestByPart.objects.filter(item_Number_id=item_number_id).order_by('testName__testName'):
            new_node = Node(inspection.id, self.job_number_id, inspection.testName.testName, NUMERIC, self.url_data_table)
            self.branch_numeric.add_node(new_node)

    def get_text_inspections(self, item_number_id, job_number_id):
        for inspection in textRecordByPart.objects.filter(item_Number_id=item_number_id).order_by('testName__testName'):
            new_node = Node(inspection.testName_id, self.job_number_id, inspection.testName.testName, TEXT, self.url_data_table)
            self.branch_text.add_node(new_node)

    def get_range_inspections(self, item_number_id, job_number_id):
        for inspection in RangeRecordByPart.objects.filter(item_Number_id=item_number_id).order_by('testName__testName'):
            new_node = Node(inspection.testName_id, self.job_number_id, inspection.testName.testName, RANGE, self.url_data_table)
            self.branch_range.add_node(new_node)

    def build_tree(self, item_number_id, job_number_id):
        self.get_cover_page(item_number_id, job_number_id)
        self.get_pass_fail_inspections(item_number_id, job_number_id)
        self.get_numeric_inspections(item_number_id, job_number_id)
        self.get_text_inspections(item_number_id, job_number_id)
        self.get_range_inspections(item_number_id, job_number_id)

    def get_json(self):
        jstree = []
        jstree.append(self.branch_cover_page.nodes[0].to_jstree())
        for each_branch in [self.branch_pass_fail, self.branch_numeric, self.branch_range, self.branch_text]:
            jstree.append(each_branch.to_jstree())
        return jstree