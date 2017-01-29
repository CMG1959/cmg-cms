from django.db import connection

def get_inspection_type(inspection_type_str):
    inspection_type_str = inspection_type_str.rstrip('VF')
    if inspection_type_str in ['Pass/Fail', 'Pass-Fail']:
        return 1
    elif inspection_type_str == 'Range':
        return 2
    elif inspection_type_str == 'Integer':
        return 3
    elif inspection_type_str == 'Numeric':
        return 4
    elif inspection_type_str == 'Text':
        return 5
    else:
        return -1


def get_qms_insp_def(job_id=498, inspection_type=1, inspection_id=11, man_num=7406):

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM [CMG_Mfg].[dbo].[GetQMSInspDef] (%s, %s , %s, %s)", [job_id, inspection_type,
                                                                                       inspection_id ,man_num] )

    columns = [col[0] for col in cursor.description]

    return dict(zip(columns, cursor.fetchone()))


