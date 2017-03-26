from collections import namedtuple, OrderedDict
from django.db import connection
import pytz
#
# def query_to_named_tuple(query):
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#     pass

QUERY_ACTIVE_JOB_ERRORS_COUNT_BY_TEST = """
SELECT
	COUNT(vISC.Test_Name) AS 'Error_Count',
	vISC.Test_Name
  FROM [cmg_qms].[dbo].[startupshot_mattecprod] as mp
  JOIN [cmg_qms].[dbo].[vInspectionSummaryCache] as vISC
  ON mp.jobNumber = vISC.Job_Number
  WHERE vISC.Inspection_Result != 'Pass'
  AND
  vISC.DATE_CREATED >= DATEADD(DAY, -{0}, GETDATE())
  GROUP BY vISC.Test_Name
  ORDER BY Error_Count DESC
"""

QUERY_ACTIVE_JOB_ERRORS_COUNT_BY_MACHINE = """
SELECT
	COUNT(mp.machNo) AS 'Error_Count',
	 mp.machNo AS 'Mach_Alias'
  FROM [cmg_qms].[dbo].[startupshot_mattecprod] as mp
  JOIN [cmg_qms].[dbo].[vInspectionSummaryCache] as vISC
  ON mp.jobNumber = vISC.Job_Number
  WHERE vISC.Inspection_Result != 'Pass'
    AND
  vISC.DATE_CREATED >= DATEADD(DAY, -{0}, GETDATE())
  GROUP BY mp.machNo
  ORDER BY Error_Count DESC
  """


QUERY_ACTIVE_JOB_ERRORS = """
    SELECT vISC.[Inspection_Type]
      ,vISC.[Date_Created]
      ,vISC.[Job_Number]
      ,vISC.[Item_Number]
      ,vISC.[Item_Description]
      ,vISC.[Test_Name]
      ,vISC.[EmpLName]
      ,vISC.[EmpFName]
      ,vISC.[Inspection_Result]
      ,vISC.[Shift]
      ,vISC.[Report_Text]
      ,VISC.[HeadCav]
	 , mp.machNo as 'Workstation'
  FROM [cmg_qms].[dbo].[startupshot_mattecprod] as mp
  JOIN [cmg_qms].[dbo].[vInspectionSummaryCache] as vISC
  ON mp.jobNumber = vISC.Job_Number
  WHERE vISC.Inspection_Result != 'Pass'
    AND
  vISC.DATE_CREATED >= DATEADD(DAY, -{0}, GETDATE())
  ORDER BY Date_Created DESC
"""


def parse_date_time(date_time):
    if date_time is None:
        return ''
    date_time = date_time.replace(tzinfo=pytz.utc)
    date_time = date_time.astimezone(pytz.timezone('America/New_York'))
    date_time = date_time.strftime('%Y-%m-%d %I:%M %p')
    return date_time


def fetch_errors(query, n_days):
    query = query.format(abs(n_days))
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns,row)) for row in cursor.fetchall()
        ]


def vh_get_active_error_count_by_test(n_days):
    data = fetch_errors(QUERY_ACTIVE_JOB_ERRORS_COUNT_BY_TEST, n_days)
    return prepare_bar_chart(data, 'Test_Name', 'Error_Count', 'Error Pareto By Test')

def vh_get_active_error_count_by_machine(n_days):
    data = fetch_errors(QUERY_ACTIVE_JOB_ERRORS_COUNT_BY_MACHINE, n_days)
    return prepare_bar_chart(data, 'Mach_Alias', 'Error_Count', 'Error Pareto By Machine')

def vh_get_active_error_verbose(n_days):
    error_list = fetch_errors(QUERY_ACTIVE_JOB_ERRORS, n_days)
    for idx, each_error in enumerate(error_list):
        error_list[idx].update({'Date_Created': parse_date_time(each_error.get('Date_Created'))})
    return error_list


def prepare_bar_chart(aggregate_dict_list, x_id, y_id, name):
    x = []
    y = []
    for each_item in aggregate_dict_list:
        x.append(each_item.get(x_id))
        y.append(each_item.get(y_id))
    return {"data": [{"x": x, "y": y, "type": "bar"}],
            "layout": {"autosize": True,
                       "title": name,
                       "yaxis": {"title": "Count"}}
            }