# Importing necessary modules and packages
import os
import re
import string
import array
import java.lang
import time as systime
from jarray import array as jarray_c
from java.util import Hashtable
from javax.management import MBeanServerConnection
from javax.management import ObjectName
from java.lang import String
from java.lang import Object

# Connect to the WebLogic Server using WLST
connect()

# Switch to the domain runtime MBean tree
domainRuntime()

# Get a list of ServerRuntimes (all running servers in the domain)
cd('ServerRuntimes')
servers = domainRuntimeService.getServerRuntimes()

# List to store names of stopped servers
stoppedServers = []

# Loop through each server and perform actions
for server in servers:
    try:
        # Check the OverallHealthState of the server and display its status
        cd('/ServerRuntimes/' + server.getName())
        CS = get('OverallHealthState').getState()
        if CS == 0:
            print server.getName(), "= Health_Ok"
        elif CS == 1:
            print server.getName(), "= HEALTH_WARN :"
        elif CS == 2:
            print server.getName(), "= HEALTH_CRITICAL :"
        elif CS == 3:
            print server.getName(), "= HEALTH_FAILED :"
        elif CS == 4:
            print server.getName(), "= HEALTH_OVERLOADED :"
        else:
            print server.getName() + ': ' + get('State') + ': UNKNOWN HEALTH STATE (' + currentState + ')'
        
        # Store the server name in a variable for later use
        ms = server.getName()
        
        # Check if the server is the AdminServer, if not, initiate shutdown and startup sequence
        if ms != "AdminServer":
            print ms, " Shutdown Initiated"
            # Delay before shutting down the server (10 seconds in this case)
            systime.sleep(10)
            # Shut down the server
            shutdown(server.getName(), 'Server', force="false")
            print ms, " Shutdown Completed"
            print ms, " Startup Initiated"
            # Start up the server
            start(ms, 'Server')
            # Delay after starting the server (10 seconds in this case)
            systime.sleep(10)
            print server.getName(), " Startup Completed"
        else:
            print "AdminServer - no action performed"
        
        # Check the OverallHealthState of the server again after the shutdown and startup
        CS = get('OverallHealthState').getState()
        if CS == 0:
            print server.getName(), "= HEALTH_OK"
        elif CS == 1:
            print server.getName(), "= HEALTH_WARN :"
        elif CS == 2:
            print server.getName(), "= HEALTH_CRITICAL :"
        elif CS == 3:
            print server.getName(), "= HEALTH_FAILED :"
        elif CS == 4:
            print server.getName(), "= HEALTH_OVERLOADED :"
        else:
            print server.getName() + ': ' + get('State') + ': UNKNOWN HEALTH STATE (' + currentState + ')'
    except WLSTException, e:
        # If there is an exception, the server is not running, add its name to the stoppedServers list
        print server.getName() + " is not running."
        stoppedServers.append(server.getName())

# Disconnect from the WebLogic Server
disconnect()

# Exit WLST
exit()
