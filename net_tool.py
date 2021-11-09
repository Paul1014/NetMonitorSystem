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

def cisco_get_interface(IP, community):
    traffic_dict = {}
    interface_oid = '1.3.6.1.2.1.2.2.1.2'
    interface_status_oid = '1.3.6.1.2.1.2.2.1.8'
    interface_speed_oid = '1.3.6.1.2.1.2.2.1.5'
    in_byte_oid = '1.3.6.1.2.1.2.2.1.10'
    out_byte_oid = '1.3.6.1.2.1.2.2.1.16'
    in_packet_oid = '1.3.6.1.2.1.2.2.1.11'
    out_packet_oid = '1.3.6.1.2.1.2.2.1.17'
    
    errorIndication, errorStatus, errorIndex, \
    varBindTable = cmdgen.CommandGenerator().bulkCmd(  
                cmdgen.CommunityData(community),  
                cmdgen.UdpTransportTarget((IP, 161)),  
                0, 
                25,
                interface_oid,
                interface_status_oid,
                interface_speed_oid, 
                in_byte_oid,
                out_byte_oid,
                in_packet_oid,
                out_packet_oid
            )

    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print("%s at %s\n" % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                ))
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    if interface_oid in str(name):
                        interface_name = str(val)
                        traffic_dict[interface_name] = {}

                    elif interface_status_oid in str(name):
                        traffic_dict[interface_name]["interface_status"]=str(val)

                    elif interface_speed_oid in str(name):
                        traffic_dict[interface_name]["interface_speed"]=str(val)

                    elif in_byte_oid in str(name):
                        traffic_dict[interface_name]["in_byte"]=str(val)

                    elif out_byte_oid in str(name):
                        traffic_dict[interface_name]["out_byte"]=str(val)

                    elif in_packet_oid in str(name):
                        traffic_dict[interface_name]["in_packet"]=str(val)
                        
                    elif out_packet_oid in str(name):
                        traffic_dict[interface_name]["out_packet"]=str(val)

            return traffic_dict