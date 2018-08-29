"""Define the application views and routes."""
__author__ = 'IBM'

# (C) Copyright IBM Corp. 2018
# The source code for this program is not published or
# otherwise divested of its trade secrets, irrespective of
# what has been deposited with the US Copyright Office.

import os
import json
from datetime import datetime
from flask import send_from_directory
from flask import render_template
from app import app
from grdlib.GrdConnection import GrdConnection
from grdlib.GRDApi import GRDApi
from step1 import renderStep1
from step2 import renderStep2
from step3 import renderStep3


@app.route('/')
@app.route('/index')
def index():    
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
    return render_template(
        "index.html",
        current_time=datetime.utcnow(),
        logins=result)

@app.route('/favicon.ico')
def favicon():
    """Define IBM Security icon for browser tab."""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')

        
@app.route('/step1')
def step1():
    return renderStep1()

@app.route('/step2')
def step2():
    return renderStep2()

@app.route('/step3')
def step3():
    return renderStep3()

