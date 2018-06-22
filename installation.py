import tarfile
import io
import os
import subprocess
import sys
import jinja2
 
def show2():
    print 'start show2'
    save = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    proc = subprocess.Popen(['./cso-setup.sh'])
    proc.wait()
    sys.stdout = save

#show2()

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
        #print key,val
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
