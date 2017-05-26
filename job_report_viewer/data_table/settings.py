HEADER_NUMERIC = [('Machine Operator', 'machineOperator'),
                  ('Inspector', 'inspectorName'),
                   ('Date', 'dateCreated' ),
                    ('Cavity', 'headCavID'),
                     ('Measurement', 'inspectorName'),
                      ('Result', 'inspectionResult'),
                  ('Value', 'numVal_1')]

HEADER_PASS_FAIL = [('Machine Operator','machineOperator'),
                    ('Inspector', 'inspectorName'),
                    ('Date', 'dateCreated'),
                    ('Inspection Result', 'inspectionResult'),
                    ('Cavity', 'headCavID'),
                    ('Defects', 'defectType')]

HEADER_RANGE = [('Machine Operator','machineOperator'),
                ('Inspector', 'inspectorName' ),
                ('Date', 'dateCreated'),
                ('Inspection Result', 'inspectionResult' ),
                ('Cavity', 'headCavID'),
                ('Low', 'numVal_1'),
                ('High' 'numVal_2')]

HEADER_TEXT = [('Machine Operator','machineOperator'),
               ('Inspector', 'inspectorName'),
               ('Date', 'dateCreated'),
               ('Result', 'inspectionResult')]

INSPECTION_SELECT_RELATED = ['machineOperator', 'inspectorName']
PREFETCH_PASS_FAIL = ['defectType']