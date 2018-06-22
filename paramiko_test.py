import paramiko
import re
import time
def sudo_ssh(hostname, usernameIn, passIn, cmd) :

    # Create an SSH client
    client = paramiko.SSHClient()

    # Make sure that we add the remote server's SSH key automatically
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the client
    client.connect(hostname, username=usernameIn, password=passIn)

    # Create a raw shell
    channel = client.invoke_shell()


    # Send the sudo command
    for command in cmd:
        print("CMD= " + command + "\n")
        time.sleep(1)

        # wait until channel is ready
        #while not channel.recv_ready() :
        if channel.recv_ready():
            #print("NOT READY " + str(channel.recv_ready()) + "\n \n")
            #time.sleep(1)

            # Send the command
            channel.send(command)
            channel.send("\n")

        # Wait a bit, if necessary
        time.sleep(1)

        # Flush the receive buffer
        receive_buffer = channel.recv(4096)

        # If promted send the sudo pass
        if re.search(b".*\[sudo\].*", receive_buffer): 
            time.sleep(1)
            print(" TYPING SUDO PASSWORD .... \n")
            channel.send( "sudoPass" + "\n" )
            receive_buffer = channel.recv(4096)

        # Print the receive buffer, if necessary
        print(receive_buffer)

    print("Executed all of the commands. Now will exit \n")
    client.close()




com =[]
com.append("sudo ls")
com.append("ls Contrail_Service_Orchestration_3.3.1")
com.append("sleep 5")
com.append("ls")
com.append("pwd")
com.append("cd /opt/")
sudo_ssh('192.168.10.40', 'root', 'passw0rd', com)
