import paramiko
import tarfile
import time
import re

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('192.168.10.40', username='root', password='passw0rd')

channel = client.invoke_shell()
channel_data = str()

print "Running ./setup_assist.sh script: ",

step1 = 0
central_infra_services = 0
regional_infra_services = 0
central_micro_services = 0
regional_micro_services = 0
while True:
    if channel.recv_ready():
        channel_data += channel.recv(100)
        print channel_data
    else:
        continue

    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    channel_data = ansi_escape.sub('', channel_data)

    if channel_data.endswith('installervm:~# '):
        if step1 == 0:
            channel.send('cd /root/Contrail_Service_Orchestration_3.3.1/\n')
            step1 += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 0:
            #channel.send('DEPLOYMENT_ENV=central ./deploy_infra_services.sh\n')
            central_infra_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 0:
            #channel.send('DEPLOYMENT_ENV=regional ./deploy_infra_services.sh\n')
            regional_infra_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 0:
            #channel.send('DEPLOYMENT_ENV=central ./deploy_micro_services.sh\n')
            central_micro_services += 1
 
    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 1 and regional_micro_services == 0:
            #channel.send('DEPLOYMENT_ENV=regional ./deploy_micro_services.sh\n')
            regional_micro_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 1 and regional_micro_services == 1:
            channel.send('./load_services_data.sh\n')
            break

