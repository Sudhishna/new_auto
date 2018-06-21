import paramiko
import tarfile
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('192.168.10.40', username='root', password='passw0rd')

print "Copying CSO tar file to installervm: ",
source= '/root/Contrail_Service_Orchestration_3.3.1.tar.gz' 
destination ='/root/Contrail_Service_Orchestration_3.3.1.tar.gz'
sftp = client.open_sftp()
sftp.put(source,destination)
sftp.close()
print "Success"
time.sleep(5)

print "Extracting files from the tar file: ",
cmd = "tar xvfz /root/Contrail_Service_Orchestration_3.3.1.tar.gz"
stdin, stdout, stderr = client.exec_command(cmd)
print "Success"
time.sleep(5)

print "Copying provision_vm.conf file to installervm: ",
source= '/root/Contrail_Service_Orchestration_3.3.1/confs/installervm.conf'
destination ='/root/Contrail_Service_Orchestration_3.3.1/confs/provision_vm.conf'
sftp = client.open_sftp()
sftp.put(source,destination)
sftp.close()
print "Success"

channel = client.invoke_shell()
channel_data = str()
host = str()
srcfile = str()

print "Running ./setup_assist.sh script: ",
#file = "/root/Contrail_Service_Orchestration_3.3.1.tar.gz"
#cmd = "cd /root/Contrail_Service_Orchestration_3.3.1/"
#stdin, stdout, stderr = client.exec_command(cmd)
#cmd = "./setup_assist.sh"
#stdin, stdout, stderr = client.exec_command(cmd)
#print "Success"

#while True:
#    if channel.recv_ready():
#        channel_data += channel.recv(9999)
#        print channel_data
#    else:
#        continue
#
#    if channel_data.endswith('installervm:~# '):
#        channel.send('cd /root/Contrail_Service_Orchestration_3.3.1/\n')
#    if channel_data.endswith('installervm:~/Contrail_Service_Orchestration_3.3.1# '):
#        channel.send('./setup_assist.sh\n')

#    print channel_data.endswith('The installer machine IP: []:')
#    #if channel_data.endswith('The installer machine IP: []:'):
#    #    channel.send('192.168.10.40\n')


