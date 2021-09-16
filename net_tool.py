import paramiko

def Connect_SSH(IP, user, passwd):
    try:
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connection.connect(IP, username=user, password=passwd)
        connection.close()
        return True
    except:
        return False
