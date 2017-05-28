# mpower.py: provides interface to ubiquity mpower pro.
import paramiko
import sys

hostname = port = cmd = None
    
def exec_single_ssh_cmd(cmd):
    """
    Executes single ssh command then close the connection.
    """
    client = None
    result = None

    user = "ubnt"
    password =  "ubnt"
    tcpport = 22
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, tcpport, user, password)
        stdin, stdout, stderr = client.exec_command(cmd)
        result = stdout.read()
    finally:
        if client: client.close()

    return result
    
def enable(port):
    result = exec_single_ssh_cmd("echo 1 > /dev/output" + str(port))

def disable(port):
    result = exec_single_ssh_cmd("echo 0 > /dev/output" + str(port))

def status(port):
    status = exec_single_ssh_cmd("cat /dev/output" + str(port))
    return int(status)

def toggle(port):
    if(status(port) == 1):
        disable(port)
    else:
        enable(port)

def usage():
    print("Usage: ./mpower.py <hostname> <port> <cmd>")
    print("Allowed commands: on, off, toggle, status")

if __name__ == '__main__':
    if len(sys.argv) is not 4:
        usage()
        exit()
    
    hostname = sys.argv[1]
    port = sys.argv[2]
    cmd = sys.argv[3]

    if(cmd == "on"):
        enable(port)
    elif(cmd == "off"):
        disable(port)
    elif(cmd == "toggle"):
        toggle(port)
    elif(cmd == "status"):
        print(status(port))
    else:
        print("Unknown cmd.")
