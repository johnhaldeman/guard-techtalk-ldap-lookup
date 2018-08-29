
from password import getPassword

def getConfig():
    return {
        "hostname": "172.16.100.152",
        "user": "IILAB\\test",
        "password": getPassword(),
        "group_postfix": ",CN=Users,DC=iilab,DC=io)",
        "base_dn": "DC=iilab,DC=io"
    }


