# cake-acl-auditor
Cake ARO/ACO ACL Auditor

Gets a list of all ACOs, then checks to see whether or not the ARO (user or group) is allowed access.
A list of allowed, and denied ACOs are returned.

For CakePHP 3 applications.

# Example Usage
    ./check_acls.py -c Groups.1

# Parameters:
-c aro to check, such as Groups.1

# Performs:
* bin/cake acl_extras aco_sync
* bin/cake acl view aco
* bin/cake acl check <target aro> <target aco>

# Authors:
* sysop.host
* notorious_turtle
