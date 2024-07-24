from django.db import connection

def call_phl_insert_sp(var):
    cursor = connection.cursor()
    stmt = '''\
        DECLARE @ret int
        EXEC @ret = dbo.PHL_Insert {}
        SELECT @ret
    '''.format(','.join(['%s']*len(var)))
    result = cursor.execute(stmt, params=var).fetchone()[0]
    cursor.close()
    return result


def fn_generic(cursor):
    msg = cursor.fetchone()[0]
    cursor.execute('FETCH ALL IN "%s"' % msg)
    thing = create_dict_from_cursor(cursor)
    cursor.close()
    return thing

def create_dict_from_cursor(cursor, DEBUG=False):
    rows = cursor.fetchall()
    # DEBUG settings (used to) affect what gets returned.
    if DEBUG:
        desc = [item[0] for item in cursor.cursor.description]
    else:
        desc = [item[0] for item in cursor.description]
    return [dict(zip(desc, item)) for item in rows]

