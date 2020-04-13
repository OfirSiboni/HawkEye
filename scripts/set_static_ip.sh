#!/bin/bash

echo "$(sed '/#AUTOGEN_START/,/#AUTOGEN_END/d' /etc/dhcpcd.conf)" > /etc/dhcpcd.conf
echo "#AUTOGEN_START" >> /etc/dhcpcd.conf
echo "interface eth0" >> /etc/dhcpcd.conf
echo "static ip_address=$1/24" >> /etc/dhcpcd.conf
echo "#AUTOGEN_END" >> /etc/dhcpcd.conf
