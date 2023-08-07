import sys
import os
from java.lang import System
import sys
import os
from java.lang import System
#Python Script to manage Servers in weblogic server.
#This script takes input from command line and executes it.
#It can be used to check status,stop,start of applications in weblogic server using weblogic wlst tool.

import getopt
#========================
#Usage Section
#========================
def usage():

    print "Usage:"
    print "java weblogic.WLST manageServers.py -n ServerName -c [stop:start:restart:status:stopall:startall:statusall]\n"
    sys.exit(2)
#========================
#Connect To Domain
#========================

def connectToDomain():
    try:      
        connect()
        print 'Successfully connected to the domain\n'


    except:
        print 'The domain is unreacheable. Please try again\n'
        exit()

#==============================================
#Checking Server Status
#==============================================
def _serverstatus(ServerName):
    try:
        cd('domainRuntime:/ServerLifeCycleRuntimes/'+ServerName);
        serverState = cmo.getState()
        if serverState == "RUNNING":
            print 'Server ' + ServerName + ' is :\033[1;32m' + serverState + '\033[0m';
        elif serverState == "STARTING":
            print 'Server ' + ServerName + ' is :\033[1;33m' + serverState + '\033[0m';
        elif serverState == "UNKNOWN":
            print 'Server ' + ServerName + ' is :\033[1;34m' + serverState + '\033[0m';
        else:
            print 'Server ' + ServerName + ' is :\033[1;31m' + serverState + '\033[0m';
        return serverState
    except:
        print 'Not able to get the' + serverState +'server status. Please try again\n';
        print 'Please check logged in user has full access to complete the requested operation on ' +ServerName+ '\n';
        exit()

#==============================================
#Start Server Block
#==============================================

def _startServer(ServerName):

    try:
        cd('domainRuntime:/ServerLifeCycleRuntimes/'+ServerName);
        cmo.start();
        state=_serverstatus(ServerName);
        while (state!='RUNNING'):
            state=_serverstatus(ServerName);
            java.lang.Thread.sleep(5000);
    except:
        print 'Error in getting current status of ' +ServerName+ '\n';
        print 'Please check logged in user has full access to complete the start operation on ' +ServerName+ '\n';
        exit()
#==============================================
#Stop Server Block
#==============================================

def _stopServer(ServerName):

    try:
        cd('domainRuntime:/ServerLifeCycleRuntimes/'+ServerName);
        cmo.shutdown(ServerName, 'Server', force="true");
        state=_serverstatus(ServerName);
        while (state!='SHUTDOWN'):
            state=_serverstatus(ServerName);
            java.lang.Thread.sleep(5000);
    except:
        print 'Error in getting current status of ' +ServerName+ '\n';
        print 'Please check logged in user has full access to complete the stop operation on ' +ServerName+ '\n';
        exit()

#===============================
#Input Values Validation Section
#===============================

if __name__=='__main__' or __name__== 'main':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:c:", ["ServerName=", "command="])

    except getopt.GetoptError, err:
        print str(err)
        usage()
    ServerName = ''
    command = ''

    for opt, arg in opts:
        if opt == "-n":
            ServerName = arg
        elif opt == "-c":
            command = arg

    if ServerName == "":
        print "Missing \"-n ServerName\" parameter.\n"
        usage()
    elif command == "":
        print "Missing \"-c command\" parameter.\n"
        usage()
#========================
#Main Control Block For Operations
#========================

def lifecycleMain():
    try:
        if command =='status' :
            _serverstatus(ServerName);
        elif command =='stop':
            state=_serverstatus(ServerName);
            if state!='SHUTDOWN' :
                print 'Trying To Shutdown Server:' + ServerName + '...';
                _stopServer(ServerName);
        elif command =='start':
            state=_serverstatus(ServerName);
            if state!='RUNNING' :
                print 'Trying To Start Server:' + ServerName + '...';
                _startServer(ServerName);
        elif command =='restart':
            state=_serverstatus(ServerName);
            if state!='SHUTDOWN' :
                print 'Trying To Shutdown Server:' + ServerName + '...';
                _stopServer(ServerName);
            state=_serverstatus(ServerName);
            if state!='RUNNING' :
                print 'Trying To Start Server:' + ServerName + '...';
                _startServer(ServerName);
        elif command == "stopall":
            try:
                cd('/Servers')
                allServers=ls('/Servers', returnMap='true')
                for p_server in allServers:
                    if p_server == 'AdminServer':
                        continue
                    else:
                        _stopServer(p_server);
            except Exception, e:
                print "Error Occured"
        elif command == "startall":
            try:
                cd('/Servers')
                allServers=ls('/Servers', returnMap='true')
                for p_server in allServers:
                    if p_server == 'AdminServer':
                        continue
                    else:
                        _startServer(p_server);
            except Exception, e:
                print "Error Occured"
        elif command == "restartall":
            try:
                cd('/Servers')
                allServers=ls('/Servers', returnMap='true')
                for p_server in allServers:
                    if p_server == 'AdminServer':
                        continue
                    else:
                        _stopServer(p_server);
                        _startServer(p_server);
            except Exception, e:
                print "Error Occured"                
        elif command == "statusall":
            try:
                cd('/Servers')
                allServers=ls('/Servers', returnMap='true')
                for p_server in allServers:
                    _serverstatus(p_server);
            except Exception, e:
                print "Error Occured"
        else:
           print 'Not able to understand the command supplied.'
           usage();
    except:
        print 'Error during lifecycle operation of ' +ServerName+ '\n'
        exit();
#========================
#Execute Block
#========================

connectToDomain();
lifecycleMain();
disconnect();
exit();
