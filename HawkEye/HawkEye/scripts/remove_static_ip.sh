#!/bin/bash
echo "$(sed '/#AUTOGEN_START/,/#AUTOGEN_END/d' /etc/dhcpcd.conf)" > /etc/dhcpcd.conf
