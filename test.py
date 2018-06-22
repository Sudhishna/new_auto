import paramiko
import tarfile
import time
import re

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
srcfile = str()

print "Running ./setup_assist.sh script: ",

complete = 0
step1 = 0
step2 = 0
step3 = 0
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
        if step2 == 0:
            channel.send('./setup_assist.sh\n')
            step2 += 1

    if re.search('Press any key to continue:$',channel_data):
        if step3 < 2:
            channel.send('\n')
            step3 += 1

    if re.search('The installer machine IP: \[\w*.*?\]:$',channel_data):
        channel.send('192.168.10.40\n')
    if re.search('The deployment environment that you want to setup. \(production/trial\) \[\w*.*?\]:$',channel_data):
        channel.send('trial\n')
    if re.search('Is CSO behind NAT \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('n\n')
    if re.search('Timezone for the servers in topology \[\w*.*?\]:$',channel_data):
        channel.send('America/Los_Angeles\n')
    if re.search('List of ntp servers \(comma seperated\) \[\w*.*?\]:$',channel_data):
        channel.send('192.168.10.10\n')
    if re.search('Do you need a HA deployment \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('n\n')
    if re.search('Provide the regional region name\(s\) \(For centralized deployment,if more than one region, provide comma separated list of region names\) \[\w*.*?\]:$',channel_data):
        channel.send('\n')
    if re.search('CSO certificate validity \(in days\) \[\w*.*?\]:$',channel_data):
        channel.send('999\n')
    if re.search('Do you want to enable TLS mode of authentication between device to FMPM services\?\. \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('y\n')
    if re.search('Do you want separate VMs for kubernetes master\? \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('y\n')
    if re.search('Provide Email Address for cspadmin user \[\w*.*?\]:$',channel_data):
        channel.send('juniperse@juniper.net\n')
    if re.search('DNS name of CSO Customer Portal \[\w*.*?\]:$',channel_data):
        channel.send('centralmsvm.example.net\n')
    if re.search('DNS name of CSO Admin Portal \(can be same as Customer Portal\) \[\w*.*?\]:$',channel_data):
        channel.send('centralmsvm.example.net\n')


    if re.search('Do you have an external keystone \(centralized mode use case only\) \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('n\n')
    if re.search('Kubernetes overlay network cidr used by the microservices \[\w*.*?\]:$',channel_data):
        channel.send('\n')
    if re.search('Kubernetes Services overlay network range \(cidr\) used by the microservices \[\w*.*?\]:$',channel_data):
        channel.send('\n')
    if re.search('Kubernetes Service APIServer IP which is in above cidr range \[\w*.*?\]:$',channel_data):
        channel.send('\n')
    if re.search('Kubernetes Cluster DNS IP used by skydns which should be in Kubernetes Services overlay network range \[\w*.*?\]:$',channel_data):
        channel.send('\n')
  
    if re.search('Number of VRR instances \[\w*.*?\]:$',channel_data):
        channel.send('1\n')
    if re.search('Do you have VRR behind NAT \(y/n\) \[\w*.*?\]:$',channel_data):
        channel.send('n\n')
    if re.search('Do all your VRR instances use the same username and password \[\w*.*?\]:$',channel_data):
        channel.send('y\n')
    if re.search('Enter the username for VRR \[\w*.*?\]:$',channel_data):
        channel.send('root\n')
    if re.search('Enter the username for VRR of instance 1 \[\w*.*?\]:$',channel_data):
        channel.send('root\n')
    if re.search('Enter the password for VRR:$',channel_data):
        channel.send('passw0rd\n')
    if re.search('Confirm Password:$',channel_data):
        channel.send('passw0rd\n')
    if re.search('VRR Public IP Address of instance 1 \[\w*.*?\]:$',channel_data):
        channel.send('192.168.10.49\n')
    if re.search('Please provide redundancy group \(0/1\) of instance 1 \[\w*.*?\]:$',channel_data):
        channel.send('0\n')
    if re.search('Kubernetes overlay network cidr used by the microservices \[\w*.*?\]:$',channel_data):
        channel.send('\n')
    if re.search('Kubernetes Services overlay network range \(cidr\) used by the microservices \[\w*.*?\]:$',channel_data):
        channel.send('\n')
    if re.search('Kubernetes Service APIServer IP which is in above cidr range \[\w*.*?\]:$',channel_data):
        channel.send('\n')
    if re.search('Kubernetes Cluster DNS IP used by skydns which should be in Kubernetes Services overlay network range \[\w*.*?\]:$',channel_data):
        channel.send('\n')


    if re.search('Enter the subnet where all CSO VMs reside \(network cidr\)\) \[\w*.*?\]:$',channel_data):
        channel.send('192.168.10.0/24\n')
    if re.search('Enter the tunnel interface unit range which can be used by cso \[\w*.*?\]:$',channel_data):
        channel.send('\n')
    if re.search('Enter the primary interface for all VMs \[\w*.*?\]:$',channel_data):
        channel.send('\n')


    if re.search('central:Number of replicas of each microservice \[\w*.*?\]:$',channel_data):
        channel.send('1\n')
    if re.search('regional:Number of replicas of each microservice \[\w*.*?\]:$',channel_data):
        channel.send('1\n')
    time.sleep(1)

    #if re.search('\w*.*',channel_data):
    #    print "########## yes completed #################################"
    #    complete = 1

    if re.search('Done!',channel_data):
        #if complete == 1:
        print "######################### done 111111 ##########################"
        content = re.findall('PLEASE STORE ALL INFRA PASSWORDS GENERATED BELOW\w*.*?Done!',channel_data,re.DOTALL)[0]

        print "###########################"
        print content
        with open('/root/passwords.txt','w') as f:
            f.write(content)
        print "###########################"
        break


 
