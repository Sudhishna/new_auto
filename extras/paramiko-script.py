import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.10.40', username='root', password='passw0rd')
chan = ssh.invoke_shell()
channel_data = str()
host = str()
srcfile = str()

buff = ''
while not buff.endswith('installervm:~# '):
    resp = chan.recv(9999)
    buff += resp
chan.send('cd /root/Contrail_Service_Orchestration_3.3.1/\n')

while not buff.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
    resp = chan.recv(9999)
    buff += resp
chan.send('./setup_assist.sh\n')

while not buff.endswith('Press any key to continue:'):
    resp = chan.recv(9999)
    buff += resp
chan.send('\n')

while not buff.endswith('The installer machine IP: []:'):
    resp = chan.recv(9999)
    buff += resp
chan.send('Sudhishna')

#while True:
#    if channel.recv_ready():
#        channel_data += channel.recv(9999)
#        print channel_data
#    else:
#        continue

#    print channel_data.endswith('installervm:~# ')
#    #if channel_data.endswith('installervm:~# '):
#    #    channel.send('./Contrail-Install.sh\n')
#
#    #if channel_data.endswith('Enter Contrail Host IP Address (x.x.x.x): '):
#    #    channel.send('192.168.10.10\n')
##
#    #if channel_data.endswith('Enter Contrail Host Password: '):
#    #    channel.send('Contrail123\n')
#    #    print channel_data.endswith("Enter Contrail Host Password: ")

