
import os
import json
from datetime import datetime
from flask import render_template
from grdlib.GrdConnection import GrdConnection
from grdlib.GRDApi import GRDApi

def getSQLEntitlements():
    """Define logic and view for app root."""
    grd_connection = GrdConnection()
    grd_api = GRDApi(grd_connection)
    result = json.loads(json.dumps(
        grd_api.create_online_report(
            'Typed SQL Server Srv Account of sys/server/security admin', 'NOW -21 DAY', 'NOW',
            fetchSize=10000, sortColumn='MemberName', sortType='ASC')))

    
    return result

def renderStep2():
    result = getSQLEntitlements()
    return render_template(
        "step2.html",
        entitlements=result,
        title="Enhanced Entitlement Reports",
        subtitle="Typed SQL Server Srv Account of sys/server/security admin"
    )

