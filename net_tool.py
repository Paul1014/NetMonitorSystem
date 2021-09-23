import paramiko
from pysnmp.entity.rfc3413.oneliner import cmdgen


def Connect_SSH(IP, user, passwd):
    try:
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connection.connect(IP, username=user, password=passwd)
        connection.close()
        return True
    except:
        return False


def cisco_snmp(IP, community):
    hostname_oid = "1.3.6.1.2.1.1.5.0"
    sysuptime_oid = "1.3.6.1.2.1.1.3.0"
    freemem_oid = "1.3.6.1.4.1.9.2.1.8.0"
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((IP, 161)),
        hostname_oid,
        sysuptime_oid,
        freemem_oid
    )
    snmp_info = {}
    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'
                )
            )
        else:
            for name, val in varBinds:
                name = str(name)
                if name == hostname_oid:
                    name = "Hostname"
                elif name == sysuptime_oid:
                    name = "Uptime"
                    val = str(val)
                    val = int(val)
                    hours = int(val/3600)
                    val = hours
                    
                elif name == freemem_oid:
                    name = "freeMem"
                    val = str(val)
                    val = int(val)
                    val = int(val/1000000)
                snmp_info[name] = str(val)

            return snmp_info

def linux_snmp(IP, community):
    hostname_oid = "1.3.6.1.2.1.1.5.0"
    sysuptime_oid = "1.3.6.1.2.1.1.3.0"
    freemem_oid = "1.3.6.1.4.1.9.2.1.8.0"
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((IP, 161)),
        hostname_oid,
        sysuptime_oid,
        freemem_oid
    )
    snmp_info = {}
    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
        return 0
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'
                )
            )
            return 0
        else:
            for name, val in varBinds:
                name = str(name)
                if name == hostname_oid:
                    name = "Hostname"
                elif name == sysuptime_oid:
                    name = "Uptime"
                elif name == freemem_oid:
                    name = "freeMem"
                snmp_info[name] = str(val)

            return snmp_info
