from inspection.models import (passFailByPart, numericTestByPart,
    textRecordByPart, RangeRecordByPart)

PASS_FAIL = 'Pass-Fail'
NUMERIC = 'Numeric'
TEXT = 'Text'
RANGE = 'Range'
COVER = 'Cover'
STATISTICS = 'Statistics'


class Node(object):

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

class Branch(object):

    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

class TreeBuilder(object):

    def __init__(self, item_number_id):
        self.item_number_id = item_number_id
        self.branch_pass_fail = Branch(PASS_FAIL)
        self.branch_numeric = Branch(NUMERIC)
        self.branch_text = Branch(TEXT)
        self.branch_range = Branch(RANGE)
        self.build_tree(item_number_id)

    def get_pass_fail_inspections(self, item_number_id):
        for inspection in passFailByPart.objects.filter(item_Number_id=item_number_id).order_by('testName__testName'):
            new_node = Node(inspection.id, inspection.testName.testName, PASS_FAIL)
            self.branch_pass_fail.add_node(new_node)

    def get_numeric_inspections(self, item_number_id):
        for inspection in numericTestByPart.objects.filter(item_Number_id=item_number_id).order_by('testName__testName'):
            new_node = Node(inspection.id, inspection.testName.testName, NUMERIC)
            self.branch_numeric.add_node(new_node)

    def get_text_inspections(self, item_number_id):
        for inspection in textRecordByPart.objects.filter(item_Number_id=item_number_id).order_by('testName__testName'):
            new_node = Node(inspection.id, inspection.testName.testName, TEXT)
            self.branch_text.add_node(new_node)

    def get_range_inspections(self, item_number_id):
        for inspection in RangeRecordByPart.objects.filter(item_Number_id=item_number_id).order_by('testName__testName'):
            new_node = Node(inspection.id, inspection.testName.testName, RANGE)
            self.branch_range.add_node(new_node)

    def build_tree(self, item_number_id):
        self.get_pass_fail_inspections(item_number_id)
        self.get_numeric_inspections(item_number_id)
        self.get_text_inspections(item_number_id)
        self.get_range_inspections(item_number_id)
