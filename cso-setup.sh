#!/bin/bash
# CSO 3.3.1 INSTALLATION
# Command example ./cso-setup.sh

HOME_DIR=/root/
DATA_PATH=$HOME_DIR/data/cso-data.txt
echo "" > $DATA_PATH

echo ""
echo " **************************************************"
echo "          CSO SERVER DEPLOYMENT PROCESS"
echo " **************************************************"
echo ""
read -p "Enter CSO Host Server Name: " temphostname
hostname=${temphostname:-$hostname}
read -p "Enter CSO Host Server IP Address (x.x.x.x/x): " tempcsoip
csoip=${tempcsoip:-$csoip}
read -p "Enter DNS Server IP Address (x.x.x.x): " tempdns
dns=${tempdns:-$dns}
read -p "Enter NTP Server IP Address (x.x.x.x): " tempntp
ntp=${tempntp:-$ntp}
read -p "Enter Gateway IP Address (x.x.x.x): " tempgw
gw=${tempgw:-$gw}
read -s -p "Enter CSO Host Server Password: " temppassword
password=${temppassword:-$password}
echo ""
read -p "Enter CSP Central Infravm IP Address (x.x.x.x/x): " tempcentralinfravmip
centralinfravmip=${tempcentralinfravmip:-$centralinfravmip}
read -p "Enter CSP Central Msvm IP Address (x.x.x.x/x): " tempcentralmsvmip
centralmsvmip=${tempcentralmsvmip:-$centralmsvmip}
read -p "Enter CSP Central k8mastervm IP Address (x.x.x.x/x): " tempcentralk8mastervmip
centralk8mastervmip=${tempcentralk8mastervmip:-$centralk8mastervmip}
read -p "Enter CSP Regional Infravm IP Address (x.x.x.x/x): " tempregionalinfravmip
regionalinfravmip=${tempregionalinfravmip:-$regionalinfravmip}
read -p "Enter CSP Regional Msvm IP Address (x.x.x.x/x): " tempregionalmsvmip
regionalmsvmip=${tempregionalmsvmip:-$regionalmsvmip}
read -p "Enter CSP Regional k8mastervm IP Address (x.x.x.x/x): " tempregionalk8mastervmip
regionalk8mastervmip=${tempregionalk8mastervmip:-$regionalk8mastervmip}
read -p "Enter CSP Installervm IP Address (x.x.x.x/x): " tempinstallervmip
installervmip=${tempinstallervmip:-$installervmip}
read -p "Enter CSP Regional Sblb IP Address (x.x.x.x/x): " tempregionalsblbip
regionalsblbip=${tempregionalsblbip:-$regionalsblbip}
read -p "Enter CSP Contrailanalytics IP Address (x.x.x.x/x): " tempcontrailanalyticsip
contrailanalyticsip=${tempcontrailanalyticsip:-$contrailanalyticsip}
read -p "Enter CSP Vrrvm IP Address (x.x.x.x/x): " tempvrrvmip
vrrvmip=${tempvrrvmip:-$vrrvmip}
echo ""

echo "hostname:$hostname" >> $DATA_PATH
echo "csoip:$csoip" >> $DATA_PATH
echo "dns:$dns" >> $DATA_PATH
echo "ntp:$ntp" >> $DATA_PATH
echo "gw:$gw" >> $DATA_PATH
echo "password:$password" >> $DATA_PATH
echo "centralinfravmip:$centralinfravmip" >> $DATA_PATH
echo "centralmsvmip:$centralmsvmip" >> $DATA_PATH
echo "centralk8mastervmip:$centralk8mastervmip" >> $DATA_PATH
echo "regionalinfravmip:$regionalinfravmip" >> $DATA_PATH
echo "regionalmsvmip:$regionalmsvmip" >> $DATA_PATH
echo "regionalk8mastervmip:$regionalk8mastervmip" >> $DATA_PATH
echo "installervmip:$installervmip" >> $DATA_PATH
echo "regionalsblbip:$regionalsblbip" >> $DATA_PATH
echo "contrailanalyticsip:$contrailanalyticsip" >> $DATA_PATH
echo "vrrvmip:$vrrvmip" >> $DATA_PATH

while true; do
  echo ""
  echo ""
  echo " ********************************************"
  echo "           CSO HOST DETAILS"
  echo " ********************************************"
  echo ""
  echo " * CSO HOST NAME     : $hostname"
  echo ""
  echo " * CSO HOST IP       : $csoip"
  echo ""
  echo " * PASSWORD          : ************"
  echo ""
  echo " * DNS SERVER        : $dns"
  echo ""
  echo " * NTP SERVER        : $ntp"
  echo ""
  echo " * GATEWAY           : $gw"
  echo ""
  echo ""
  echo " ********************************************"
  echo "           CSO VM DETAILS"
  echo " ********************************************"
  echo ""
  echo " * CENTRAL INFRAVM IP     : $centralinfravmip"
  echo ""
  echo " * CENTRAL MSVM IP        : $centralmsvmip"
  echo ""
  echo " * CENTRAL K8MASTERVM IP  : $centralk8mastervmip"
  echo ""
  echo " * REGIONAL INFRAVM IP    : $regionalinfravmip"
  echo ""
  echo " * REGIONAL MSVM IP       : $regionalmsvmip"
  echo ""
  echo " * REGIONAL K8MASTERVM IP : $regionalk8mastervmip"
  echo ""
  echo " * INSTALLER VM IP        : $installervmip"
  echo ""
  echo " * REGIONAL SBLB IP       : $regionalsblbip"
  echo ""
  echo " * CONTRAIL ANALYTICS IP  : $contrailanalyticsip"
  echo ""
  echo " * VRR VM IP              : $vrrvmip"
  echo ""
  echo " ********************************************"

  read -p ' Confirm above details (Y?N) ? ' choice
  case $choice in
        [Yy]* ) break;;
        [Nn]* )
          echo ""
          echo ""
          echo "Enter new values, or press enter to accept default values"
          echo "********************************************************"
          echo "TARGET MACHINE DETAILS: "
          read -p " Enter CSO Hostname ($hostname): " temp
          hostname=${temp:-$hostname}
          read -p " Enter CSO IP ($csoip): " temp
          csoip=${temp:-$csoip}
          read -p " Enter PASSWORD ($password): " temp
          password=${temp:-$password}
          read -p " Enter DNS SERVER ($dns): " temp
          dns=${temp:-$dns}
          read -p " Enter GATEWAY ($gw): " temp
          gw=${temp:-$gw}
          echo ""
          read -p " Enter CENTRAL INFRAVM IP ($centralinfravmip): " temp
          centralinfravmip=${temp:-$centralinfravmip}
          read -p " Enter CENTRAL MSVM IP ($centralmsvmip): " temp
          centralmsvmip=${temp:-$centralmsvmip}
          read -p " Enter CENTRAL K8MASTERVM IP ($centralk8mastervmip): " temp
          centralk8mastervmip=${temp:-$centralk8mastervmip}
          read -p " Enter REGIONAL INFRAVM IP ($regionalinfravmip): " temp
          regionalinfravmip=${temp:-$regionalinfravmip}
          read -p " Enter REGIONAL MSVM IP ($regionalmsvmip): " temp
          regionalmsvmip=${temp:-$regionalmsvmip}
          read -p " Enter REGIONAL K8MASTERVM IP ($regionalk8mastervmip): " temp
          regionalk8mastervmip=${temp:-$regionalk8mastervmip}
          read -p " Enter INSTALLER VM IP ($installervmip): " temp
          installervmip=${temp:-$installervmip}
          read -p " Enter CONTRAIL ANALYTICS IP ($contrailanalyticsip): " temp
          contrailanalyticsip=${temp:-$contrailanalyticsip}
          clear
          ;;
        * ) echo "Please answer y or n";;
    esac
done

while true; do
echo ""
echo " ********************************************"
echo ""
read -p ' PROCEED WITH THE CSO SETUP?? (Y/n) ' choice
  case $choice in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer y or n";;
    esac
done

echo ""
echo ""
echo "##############################################################"
echo "                     CSO INSTALLATION BEGINS"
echo "##############################################################"
echo ""
echo ""

