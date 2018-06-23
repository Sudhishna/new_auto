#!/bin/bash
# OPENSTACK 10 WITH CONTRAIL 4.1 INSTALLATION USING SERVER-MANAGER
# Comannd example ./Contrail-Install.sh
# Authors: Sudhishna Sendhilvelan <ssendhil@juniper.net>, Lakshmi Rajan <lrajan@juniper.net>
# Date written 2018 March 9

echo ""
echo " ********************************************"
echo "           CONTRAIL SETUP DETAILS"
echo " ********************************************"
echo ""

read -p "Enter Contrail Host IP Address (x.x.x.x): " tempip
ip=${tempip:-$ip}
read -s -p "Enter Contrail Host Password: " temppassword
password=${temppassword:-$password}
echo ""
read -p "Enter Management Interface Name: " tempiface
miface=${tempiface:-$miface}
read -p "Enter File Server Ip: " tfs
file_server=${tfs:-$file_server}

echo ""
echo ""
echo "##############################################################"
echo "                     CONTRAIL SETUP BEGINS"
echo "##############################################################"
echo ""
echo ""
