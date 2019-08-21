# -*-  coding: utf-8 -*-
# Author: Burak Karaduman <burakkaradumann@gmail.com>
# Usage: python serviceCheck.py

import re
import os
import subprocess

# Make it colorful
green = "\x1b[1;32;40m"
red = "\x1b[1;31;40m"
bold='\x1b[01m'
resetColor = "\x1b[0m"

# You can add any services to in below list.
exactServices = ['hostcontext', 'hostservices']

# Check, Is host console?
def isConsole():
    checkConsole = subprocess.check_output("/opt/qradar/bin/myver -c", shell=True).strip("\n")
    if  checkConsole == "true":
        return True
    else:
        return False

if isConsole():
    exactServices.append("tomcat")


def componentProcess():
    # You can add services below list what do you want to check.
    

    processList = subprocess.check_output("grep COMPONENT /opt/qradar/conf/nva.hostcontext.conf | awk -F '=' '{print $2}'", shell=True).split(",")
    processList += exactServices        

    cleanList = []
    for process in processList:
        if not "tunnel" in process:
            if "." in process:
                cleanList.append(process.strip("\n").split(".")[0])
            else:
                cleanList.append(process.strip("\n"))
    cleanList = sorted(cleanList, key=len)          
    return cleanList


def checkStatus(serviceName, longest):
    status = subprocess.check_output("systemctl status {} | cut -f 1".format(serviceName.strip("\n")), shell=True)
    if "Active: active" in status:
        icon = "[+]"
        color = green
        date = re.search('since\s(.*?)\\n',status).group(1)
        pid = re.search('Main\sPID:\s(\d+)\s',status).group(1)
        activeLine = re.search('Active:\s(\S+)',status).group(1)
    else:
        icon = "[-]"
        color = red
        activeLine = re.search('Active:\s(\S+)',status).group(1)
        try:
            date = re.search('since\s(.*?)\\n',status).group(1)
        except:
            date = "null"
        try:
            pid = re.search('Main\sPID:\s(\d+)\s',status).group(1)
        except:
            pid = "null"

    print(color + icon +  " " +serviceName.ljust(longest," ") + "   {}".format(pid.ljust(10," ")) + "   " +activeLine + " " +date + resetColor)

os.system("clear")
print("\n"+"\x1b[4;30;42m"+"##############################################################################################################"+"\x1b[0m"+"\n\n\n")

first = 0
for service in componentProcess():
    longest = len(max(componentProcess(), key=len))
    if first == 0:
        print(bold + " "*4 + "SERVICE NAME".ljust(longest, " ") + "   PROCESS ID" + "   STATUS\n" + resetColor)
        first += 1 
    longest = len(max(componentProcess(), key=len))
    checkStatus(service, longest)
print("\nAction: systemctl status | start | stop | enable | disable <service_name>")
print("\n"+"\x1b[4;30;42m"+"##############################################################################################################"+"\x1b[0m"+"\n\n\n")
