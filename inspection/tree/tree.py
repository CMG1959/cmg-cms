import re

class Node(object):
    def __init__(self, id, name, children, depth):
        self.id = id
        self.name = name
        self.children = children or []
        self.depth = depth

class InspectionTree(object):
    workstation_type = 'workstation_type'
    re_workstation_type = '(?P<workstation_type>[a-zA-Z]+)'
    re_workstation_id = '(?P<workstation_id>\d+)'

    @classmethod
    def get_workstation_types(cls, active_stations):
        re_expr = re.compile(cls.re_workstation_type+cls.re_workstation_id)

        matches = filter(None, map(lambda x: re_expr.match(x), active_stations))
        workstation_types = set([m.group(cls.workstation_type) for m in matches])

        return list(workstation_types)



if __name__=='__main__':
    mattec = [['IMM01', '353-900001', ['Numeric Inspection', 'Other Inspection']],
              ['IMM02', '353-900003',
               ['Numeric Inspection', 'Other Inspection']],
              ['ISBM30', '353-600001',
               ['Numeric Inspection', 'Other Inspection', 'One More']]]

    active_stations = [x[0] for x in mattec]
    print InspectionTree.get_workstation_types(active_stations)