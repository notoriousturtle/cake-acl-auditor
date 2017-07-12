#!/usr/bin/python

"""
Cake ARO/ACO ACL Auditor

Gets a list of all ACOs, then checks to see whether or not the ARO (user or group) is allowed access.
A list of allowed, and denied ACOs are returned.

Parameters:
    -c aro to check, such as Groups.1

Performs:
    * bin/cake acl_extras aco_sync
    * bin/cake acl view aco
    * bin/cake acl check <target aro> <target aco>

Authors:
    * sysop.host
    * notorious_turtle
"""

import re
import os
import subprocess
import sys
import getopt

def usage():
    print("Usage: "+sys.argv[0]+" -c <aro-to-check>")
    print("       -c, aro (e.g. Groups.1)")

if __name__ == '__main__':
    aro = ""

    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'c:', ['aro=', 
                                                         ])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in options:
        if opt in ("-c", "--aro"):
            aro = arg

    if aro == "":
        usage()
        sys.exit(2)

    print("* Performing ACO sync")
    sync = subprocess.Popen("bin/cake acl_extras aco_sync", stdout=subprocess.PIPE, shell=True)
    (output, err) = sync.communicate()

    print("* Fetching ACO list")
    aco = subprocess.Popen("bin/cake acl view aco", stdout=subprocess.PIPE, shell=True)
    (output, err) = aco.communicate()

    output = re.sub(r"\[\d+\]", "", output) #remove [n] from lines
    output = output.split("\n",9)[9] #remove first 9 lines of output
    links = output.split("\n")[0:-2] #remove first 9 lines of output
    links = [e[3:] for e in links]
    links = [e.replace("  ","\t") for e in links]
    links = [e.replace("  ","\t") for e in links]

    print("* Checking ACOs:")
    url = parent = child = subChild = subChild2 = ""
    allowed = []
    denied = []
    for link in links:
        parentPattern = re.compile("^([A-Za-z]+)+$")
        if parentPattern.match(link):
            parent = link.strip()
            url =  "{}".format(parent)

        childPattern = re.compile("^(\t[A-Za-z]+)+$")
        if childPattern.match(link):
            child = link.strip("\t").strip()
            url = "{}{}{}".format(parent, "/", child)

        subChildPattern = re.compile("^(\t\t[A-Za-z]+)+$")
        if subChildPattern.match(link):
            subChild = link.strip("\t\t").strip()
            url = "{}{}{}{}{}".format(parent, "/", child, "/", subChild)

        subChild2Pattern = re.compile("^(\t\t\t[A-Za-z]+)+$")
        if subChild2Pattern.match(link):
            subChild2 = link.strip("\t\t\t").strip()
            url = "{}{}{}{}{}{}{}".format(parent, "/", child, "/", subChild, "/", subChild2)

        print("\t"+url)
        check = subprocess.Popen("bin/cake acl check "+aro+" "+url, stdout=subprocess.PIPE, shell=True)
        (output, err) = check.communicate()

        #print(output)
        if "not allowed" in output:
            denied.append(url)
        else:
            allowed.append(url)

    print("\n----- Checked for ARO: "+aro)
    sys.stdout.write("\n  Allowed: \n\t")
    print('\n\t'.join(allowed))

    sys.stdout.write("\n  Denied: \n\t")
    print('\n\t'.join(denied))
