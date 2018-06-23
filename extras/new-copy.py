import tarfile
import io
import os
import subprocess
import sys
import jinja2
import paramiko
import time
import re
from subprocess import call
 
print "Running services infra/micro script: ",

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('192.168.10.40', username='root', password='passw0rd')

channel = client.invoke_shell()
channel_data = str()
host = str()
srcfile = str()

step1 = 0
central_infra_services = 0
regional_infra_services = 0
central_micro_services = 0
regional_micro_services = 0
load_services_data = 0
while True:
    if channel.recv_ready():
        channel_data = channel.recv(9999)
        print channel_data
    else:
        continue

    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    channel_data = ansi_escape.sub('', channel_data)

    if channel_data.endswith('installervm:~# '):
        if step1 == 0:
            print "changed directory"
            channel.send('cd /root/Contrail_Service_Orchestration_3.3.1/\n')
            step1 += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 0:
            channel.send('DEPLOYMENT_ENV=central ./deploy_infra_services.sh\n')
            print "central infra"
            central_infra_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 0:
            channel.send('DEPLOYMENT_ENV=regional ./deploy_infra_services.sh\n')
            print "regional infra"
            regional_infra_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 0:
            channel.send('DEPLOYMENT_ENV=central ./deploy_micro_services.sh\n')
            central_micro_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 1 and regional_micro_services == 0:
            channel.send('DEPLOYMENT_ENV=regional ./deploy_micro_services.sh\n')
            regional_micro_services += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if central_infra_services == 1 and regional_infra_services == 1 and central_micro_services == 1 and regional_micro_services == 1 and load_services_data ==0:
            channel.send('./load_services_data.sh\n')
            load_services_data += 1
            #break

    if load_services_data == 1:
        break
