import paramiko
import tarfile
import time
import re

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('192.168.10.40', username='root', password='passw0rd')

channel = client.invoke_shell()
channel_data = str()
full_data = str()

print "Running ./setup_assist.sh script: ",

step1 = 0
central_infra_services = 0
regional_infra_services = 0
central_micro_services = 0
regional_micro_services = 0
load_services_data = 0
deployment_duration = 0
while True:
    if channel.recv_ready():
        channel_data = channel.recv(9999)
        full_data += channel_data
        print channel_data
    else:
        continue

    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    channel_data = ansi_escape.sub('', channel_data)

    deployment_duration = full_data.count("Deployment duration")
    if channel_data.endswith('installervm:~# '):
        if step1 == 0:
            channel.send('cd /root/Contrail_Service_Orchestration_3.3.1/\n')
            step1 += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 0 and deployment_duration == 0:
            channel.send('DEPLOYMENT_ENV=central ./deploy_infra_services.sh\n')
            central_infra_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 0 and deployment_duration==1:
            channel.send('DEPLOYMENT_ENV=regional ./deploy_infra_services.sh\n')
            regional_infra_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 0 and deployment_duration ==2:
            channel.send('DEPLOYMENT_ENV=central ./deploy_micro_services.sh\n')
            central_micro_services += 1
 
    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 1 and regional_micro_services == 0 and deployment_duration == 3:
            channel.send('DEPLOYMENT_ENV=regional ./deploy_micro_services.sh\n')
            regional_micro_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 1 and regional_micro_services == 1 and load_services_data ==0 and deployment_duration == 4:
            channel.send('./load_services_data.sh\n')
            load_services_data += 1

    if load_services_data == 1:
        print load_services_data
        break
