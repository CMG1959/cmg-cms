import pyodbc
import json
import os
from django.db import connection
#
# default_db = json.load(open(os.path.join('..','CIMC', 'config.json')))['default_database']
#
# # Connection example: Windows, without a DSN, using the Windows SQL Server driver
# cnxn_string = 'DRIVER={%s};SERVER=%s;PORT=1433;DATABASE=CMG_Mfg;UID=%s;PWD=%s' % (default_db['OPTIONS']['driver'],
#                                                                                   default_db['HOST'],
#                                                                                   default_db['USER'],
#                                                                                   default_db['PASSWORD'])
# cnxn = pyodbc.connect(cnxn_string)
#
#
# # Opening a cursor
# cursor = cnxn.cursor()
#
# cursor.execute(
#     """
#     SELECT * FROM [CMG_Mfg].[dbo].[GetQMSInspDef] (?, ? , ?, ?)
#     """, 498, 1 ,11 ,7406)
#
# row = cursor.fetchone()
#
# print row
#
# cnxn.close()

cursor = connection.cursor()

cursor.execute("SELECT * FROM [CMG_Mfg].[dbo].[GetQMSInspDef] (?, ? , ?, ?)", [498, 1 ,11 ,7406] )

row = cursor.fetchone()

print row