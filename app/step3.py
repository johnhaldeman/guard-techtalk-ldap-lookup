import os
import json
from datetime import datetime
from flask import render_template
from grdlib.GrdConnection import GrdConnection
from grdlib.GRDApi import GRDApi
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from config import getConfig

conf = getConfig()

def getSQLEntitlements():
    """Define logic and view for app root."""
    grd_connection = GrdConnection()
    grd_api = GRDApi(grd_connection)
    result = json.loads(json.dumps(
        grd_api.create_online_report(
            'Typed SQL Server Srv Account of sys/server/security admin', 'NOW -21 DAY', 'NOW',
            fetchSize=10000, sortColumn='MemberName', sortType='ASC')))

    return result

def connect():
    server = Server(conf["hostname"], port=389, get_info=ALL)
    conn = Connection(server, user=conf["user"], password=conf["password"], authentication=NTLM)
    conn.bind()
    return conn

def getGroupMembers(conn, group):
    filter = '(memberof=CN=' + group + conf["group_postfix"]
    conn.search(conf["base_dn"], filter, search_scope = SUBTREE, attributes=['cn', 'sAMAccountName'])

    entryList = list()
    for entry in conn.entries:
        newEntry = {}
        newEntry['id'] = str(entry.sAMAccountName)
        newEntry['name'] = str(entry.cn)
        entryList.append(newEntry)
        
    return entryList

def renderStep3():
    guardResult = getSQLEntitlements()
    conn = connect()

    for result in guardResult:
        if result['Type'] == 'WINDOWS_GROUP':
            groupName = result['MemberName'].split("\\",1)[1].strip()
            result['members'] = getGroupMembers(conn, groupName)
        else:
            result['members'] = list()
    
    return render_template(
        "step3.html",
        entitlements=guardResult,
        title="Enhanced Entitlement Reports",
        subtitle="Typed SQL Server Srv Account of sys/server/security admin"
    )









