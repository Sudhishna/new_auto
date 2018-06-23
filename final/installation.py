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
 
def show2():
    print 'start show2'
    save = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    proc = subprocess.Popen(['./cso-setup.sh'])
    proc.wait()
    sys.stdout = save

#show2()

print "Extracting file from the CSO tar file"
def untar(fname):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
        print "Extracted in Current Directory"
    else:
        print "Not a tar.gz file: '%s '" % sys.argv[0]
 
untar("/root/Contrail_Service_Orchestration_3.3.1.tar.gz")

data_file = "/root/data/cso-data.txt"
with open(data_file) as f:
    lines = f.readlines()

dict = {}
for line in lines:
    if line.strip() != "":
        key,val = line.strip().split(":")
        dict.update({key:val})

def load_template_config(dict,template_file):

    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_file)

    '''
    RENDER CONFIG BASED ON VARIABLES AND TEMPLATE
    '''
    print "Render the Configuration basd on auto-generated variables and the template"
    outputText = template.render(dict)
    return outputText

installerip = dict['csoip'].split("/")[0]
dict.update({'installerip':installerip})
print dict

template_file = "/root/template/provision-vm.j2"
provision_config = load_template_config(dict,template_file)

with open('/root/Contrail_Service_Orchestration_3.3.1/confs/provision_vm.conf','w') as f:
    f.write(provision_config)

installervmip = dict['installervmip'].split("/")[0]
dict.update({'installerip':installervmip})
print dict

template_file = "/root/template/provision-vm.j2"
provision_config = load_template_config(dict,template_file)

with open('/root/Contrail_Service_Orchestration_3.3.1/confs/installervm.conf','w') as f:
    f.write(provision_config)

def show3():
    print 'start show3'
    save = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    os.chdir('/root/Contrail_Service_Orchestration_3.3.1/')
    proc = subprocess.Popen(['./provision_vm.sh'])
    proc.wait()
    sys.stdout = save
    os.chdir('/root/')

show3()
time.sleep(10)

call(["python", "test.py"])

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('192.168.10.40', username='root', password='passw0rd')

print "Copying CSO tar file to installervm: "
source= '/root/Contrail_Service_Orchestration_3.3.1.tar.gz'
destination ='/root/Contrail_Service_Orchestration_3.3.1.tar.gz'
sftp = client.open_sftp()
sftp.put(source,destination)
sftp.close()
print "Success"
time.sleep(10)

print "Extracting files from the tar file: "
cmd = "tar xvzf /root/Contrail_Service_Orchestration_3.3.1.tar.gz"
stdin, stdout, stderr = client.exec_command(cmd)
print (stdout.read())
print "Success"
time.sleep(5)

print "Copying provision_vm.conf file to installervm: ",
source= '/root/Contrail_Service_Orchestration_3.3.1/confs/installervm.conf'
destination ='/root/Contrail_Service_Orchestration_3.3.1/confs/provision_vm.conf'
sftp = client.open_sftp()
sftp.put(source,destination)
sftp.close()
print "Success"
time.sleep(5)

channel = client.invoke_shell()
channel_data = str()
host = str()
full_data = str()

print "Running ./setup_assist.sh script: ",

complete = 0
step1 = 0
step2 = 0
step3 = 0
setup_assist_complete = 0
while True:
    if channel.recv_ready():
        channel_data = channel.recv(9999)
        full_data += channel_data
        print channel_data
    else:
        continue


    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    channel_data = ansi_escape.sub('', channel_data)

    if channel_data.endswith('installervm:~# '):
        if step1 == 0:
            channel.send('cd /root/Contrail_Service_Orchestration_3.3.1/\n')
            time.sleep(2)
            step1 += 1

    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
        if step2 == 0:
            channel.send('./setup_assist.sh\n')
            time.sleep(2)
            step2 += 1

    if re.search('Press any key to continue:$',channel_data):
        if step3 < 2:
            channel.send('\n')
            time.sleep(1)
            step3 += 1

    if re.search('The installer machine IP: \[\w*.*?\]:$',channel_data):
        channel.send(installervmip + '\n')
        time.sleep(1)
    if re.search('The deployment environment that you want to setup. \(production/trial\) \[\w*.*?\]:$',channel_data):
        channel.send('trial\n')
        time.sleep(1)
    if re.search('Is CSO behind NAT \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('n\n')
        time.sleep(1)
    if re.search('Timezone for the servers in topology \[\w*.*?\]:$',channel_data):
        channel.send('America/Los_Angeles\n')
        time.sleep(1)
    if re.search('List of ntp servers \(comma seperated\) \[\w*.*?\]:$',channel_data):
        channel.send(installerip + '\n')
        time.sleep(1)
    if re.search('Do you need a HA deployment \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('n\n')
        time.sleep(1)
    if re.search('Provide the regional region name\(s\) \(For centralized deployment,if more than one region, provide comma separated list of region names\) \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)
    if re.search('CSO certificate validity \(in days\) \[\w*.*?\]:$',channel_data):
        channel.send('999\n')
        time.sleep(1)
    if re.search('Do you want to enable TLS mode of authentication between device to FMPM services\?\. \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('y\n')
        time.sleep(1)
    if re.search('Do you want separate VMs for kubernetes master\? \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('y\n')
        time.sleep(1)
    if re.search('Provide Email Address for cspadmin user \[\w*.*?\]:$',channel_data):
        channel.send('juniperse@juniper.net\n')
        time.sleep(1)
    if re.search('DNS name of CSO Customer Portal \[\w*.*?\]:$',channel_data):
        channel.send('centralmsvm.example.net\n')
        time.sleep(1)
    if re.search('DNS name of CSO Admin Portal \(can be same as Customer Portal\) \[\w*.*?\]:$',channel_data):
        channel.send('centralmsvm.example.net\n')
        time.sleep(1)


    if re.search('Do you have an external keystone \(centralized mode use case only\) \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('n\n')
        time.sleep(1)
    if re.search('Kubernetes overlay network cidr used by the microservices \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)
    if re.search('Kubernetes Services overlay network range \(cidr\) used by the microservices \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)
    if re.search('Kubernetes Service APIServer IP which is in above cidr range \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)
    if re.search('Kubernetes Cluster DNS IP used by skydns which should be in Kubernetes Services overlay network range \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)

    if re.search('Number of VRR instances \[\w*.*?\]:$',channel_data):
        channel.send('1\n')
        time.sleep(1)
    if re.search('Do you have VRR behind NAT \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('n\n')
        time.sleep(1)
    if re.search('Do all your VRR instances use the same username and password \[\w*.*?\]:$',channel_data):
        channel.send('y\n')
        time.sleep(1)
    if re.search('Enter the username for VRR \[\w*.*?\]:$',channel_data):
        channel.send('root\n')
        time.sleep(1)
    if re.search('Enter the username for VRR of instance 1 \[\w*.*?\]:$',channel_data):
        channel.send('root\n')
        time.sleep(1)
    if re.search('Enter the password for VRR:$',channel_data):
        channel.send('passw0rd\n')
        time.sleep(1)
    if re.search('Confirm Password:$',channel_data):
        channel.send('passw0rd\n')
        time.sleep(1)
    if re.search('VRR Public IP Address of instance 1 \[\w*.*?\]:$',channel_data):
        channel.send(dict['vrrvmip'].split("/")[0] + '\n')
        time.sleep(1)
    if re.search('Please provide redundancy group \(0/1\) of instance 1 \[\w*.*?\]:$',channel_data):
        channel.send('0\n')
        time.sleep(1)
    if re.search('Kubernetes overlay network cidr used by the microservices \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)
    if re.search('Kubernetes Services overlay network range \(cidr\) used by the microservices \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)
    if re.search('Kubernetes Service APIServer IP which is in above cidr range \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)
    if re.search('Kubernetes Cluster DNS IP used by skydns which should be in Kubernetes Services overlay network range \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)


    if re.search('Enter the subnet where all CSO VMs reside \(network cidr\)\) \[\w*.*?\]:$',channel_data):
        channel.send('192.168.10.0/24\n')
        time.sleep(1)
    if re.search('Enter the tunnel interface unit range which can be used by cso \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)
    if re.search('Enter the primary interface for all VMs \[\w*.*?\]:$',channel_data):
        channel.send('\n')
        time.sleep(1)


    if re.search('central:Number of replicas of each microservice \[\w*.*?\]:$',channel_data):
        channel.send('1\n')
        time.sleep(1)
    if re.search('regional:Number of replicas of each microservice \[\w*.*?\]:$',channel_data):
        channel.send('1\n')
        time.sleep(1)
    if re.search('Done!',channel_data) and setup_assist_complete == 0:
        content = re.findall('PLEASE STORE ALL INFRA PASSWORDS GENERATED BELOW\w*.*?Done!',full_data,re.DOTALL)[0]
        setup_assist_complete = 1
        with open('/root/passwords.txt','w') as f:
            f.write(content)
        break


print "Running services infra/micro script: ",

call(["python", "vers.py"])

