from django.db import connection

def get_qms_insp_def(job_id=498, inspection_type=1, inspection_id=11, man_num=7406):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM [CMG_Mfg].[dbo].[GetQMSInspDef] (%s, %s , %s, %s)", [job_id, inspection_type,
                                                                                       inspection_id ,man_num] )
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))



