INSPECTION_RESULT = 'inspectionResult'

INSPECTION_NUMERIC = ['numericTestName__testName__testName', INSPECTION_RESULT ]

INSPECTION_PASS_FAIL = ['passFailTestName__testName', INSPECTION_RESULT]

INSPECTION_RANGE = ['rangeTestName__testName', INSPECTION_RESULT ]

INSPECTION_TEXT = ['textTestName__testName']

INSPECTION_PHL = [('Inspector Name', 'inspectorName'),
              ('Date', 'dateCreated'),
              ('Event', 'descEvent')]

INSPECTION_SELECT_RELATED = ['machineOperator', 'inspectorName']
PREFETCH_PASS_FAIL = ['defectType']

TEST_NAME = 'Test Name'