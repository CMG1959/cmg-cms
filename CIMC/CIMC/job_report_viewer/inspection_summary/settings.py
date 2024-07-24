INSPECTION_RESULT = 'inspectionResult'

INSPECTION_NUMERIC = ['numeric_test_name_id__testName', INSPECTION_RESULT ]

INSPECTION_PASS_FAIL = ['passFailTestName__testName', INSPECTION_RESULT]

INSPECTION_RANGE = ['rangeTestName__testName', INSPECTION_RESULT ]

INSPECTION_TEXT = ['textTestName__testName']

INSPECTION_PHL = [('Inspector Name', 'inspectorName'),
              ('Date', 'dateCreated'),
              ('Event', 'descEvent')]

INSPECTION_SELECT_RELATED = ['machineOperator', 'inspectorName']
PREFETCH_PASS_FAIL = ['defectType']

TEST_NAME = 'Test Name'


REPORT = [('Name', 'name'),
          ('Inspection Type', 'inspection_type'),
          ('Number Passed', 'number_passed'),
          ('Number Failed', 'number_failed'),
          ('Total', 'total')]

SUMMARY_NUMERIC_ID = 'numVal_1'
SUMMARY_NUMERIC = ['numeric_test_name_id__testName']

SUMMARY_NUMERIC_REPORT = [('Test Name', SUMMARY_NUMERIC[0]),
                          ('Min', 'min'),
                          ('Mean', 'mean'),
                          ('StdDev', 'std'),
                          ('Max', 'max')]