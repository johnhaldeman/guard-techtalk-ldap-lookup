
import os
import json
from datetime import datetime
from flask import render_template
from grdlib.GrdConnection import GrdConnection
from grdlib.GRDApi import GRDApi

def getFailedLogins():
    """Define logic and view for app root."""
    grd_connection = GrdConnection()
    grd_api = GRDApi(grd_connection)
    result = json.loads(json.dumps(
        grd_api.create_online_report(
            'Guardium Logins', 'NOW -7 DAY', 'NOW',
            fetchSize=25, sortColumn='Login Date And Time', sortType='DESC')))

    ''' More GuardAPI functions exist; for more details,
        search "GuardAPI Reference" within Knowledge Center or visit
            https://www.ibm.com/support/knowledgecenter/en/SSMPHH_10.1.0
            /com.ibm.guardium.doc.reference/cli_api/guardapi_reference.html

        For example,
            grd_api.list_staps()
            grd_api.create_online_report(
                'SQL Errors', 'NOW -10 HOUR', 'NOW +3 HOUR')))
            grd_api.create_online_report(
                'Managed Units', "NOW -30 DAY", "NOW")
    '''

    for row in result:
        row['login_datetime'] = datetime.strptime(
            row['Login Date And Time'], '%Y-%m-%d %H:%M:%S')
        if int(row['Login Succeeded']) == 1:
            row['failed'] = False
        else:
            row['failed'] = True
    return result

def renderStep1():
    result = getFailedLogins()
    return render_template(
        "step1.html",
        current_time=datetime.utcnow(),
        logins=result)

