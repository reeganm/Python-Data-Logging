#!/usr/bin/env python3

#script for Loging CSV data from Serial

import serial
import time
import os
import sys
import os
import json

################################################
#code that stops this process from running twice
pid = str(os.getpid()) #get process id
pidfile = 'pyCSVlog.pid'

if 0:#os.path.isfile(pidfile):
    print("%s already exists, exiting",pidfile)
    sys.exit()
open(pidfile, 'w').write(pid) #create lock file
################################################

#serial settings
port = '/dev/ttyACM0'
baud = '9600'
endline = b'\n'
delimiter = ','

#################################################
## Function Declarationss ##

def openserialport():
    status = 0
    while status == 0:
        if os.path.isfile('serialsettings.json'): #look for settings file
            #load settings file
            print('settings file found');
            with open("serialsettings.json") as infile:
                serialsettings = json.load(infile)
            try:
                s = serial.Serial(serialsettings['port'], baudrate=baud, timeout=5.0)
                status = 1
                print('settings applied')
                print('port opened')
            except:
                print('failed to apply saved settings')
                os.remove('serialsettings.json')
                time.sleep(1)
        else: #there is no settings file
            time.sleep(1)
            #try opening serial port defined in this file
            try:
                s = serial.Serial(port, baudrate=baud, timeout=3.0)
                print('serial port opened')
                status = 1
                #update settings file
                serialsettings = { 'port':port }
                with open("serialsettings.json", "w") as outfile:
                    json.dump(serialsettings, outfile, indent=4)
                    print('settings saved')
            except serial.serialutil.SerialException:
                print('cant connect to serial port')
                time.sleep(30) #wait for serial to be connected
    return(s)

allowedchars = [ ord(b'0'),ord(b'1'),ord(b'2'),ord(b'3'),ord(b'4'),ord(b'5'),ord(b'6'),ord(b'7'),ord(b'8'),ord(b'9'),ord(b','),ord(b'-'),ord('.')]

def readlineCR(serial_p):
        rv = ""
        state = 0
        while state == 0:
            val = serial_p.read(1)
            if (val != b'\x00') & (val != b''): #no time out
                val = ord(val) #convert ascii to a number
                if val == ord('\n'):
                    state = 1 #eol detected
                else:
                    if val in allowedchars: #check for valid characters
                        rv = rv + chr(val)
                    else: #invalid character
                        rv = ""
                        print('invalid character')
                        state = 0 #invalid character detected
        return(rv)

def csv2dict(line,keys):
    #split line 
    d = line.split(delimiter)
    #zip into dictionary
    data = dict(zip(keys,d))
    return data


#################################################
## Settings ##

#csv format
keys = ['v','w','x','y','z']

#log file
filesize = 5000
#http://stackoverflow.com/questions/647769/why-cant-pythons-raw-string-literals-end-with-a-single-backslash
logfiledir = r"/home/pi/Log"
logfilename = 'log'
logfiletype = '.csv'
logfilenumber = 0
logsessionnumber = 0
lograte = 5

#display
displayrate = 1.0

#variables for timing
logtimer = 0
displaytimer = 0

#keeping track of file number
filesizecount = 0

#####################################
##### put actual code that runs here
try:
    
    if not os.path.exists(logfiledir):
        os.makedirs(logfiledir)

    #scan log directory to determine number
    #http://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python#8933290
    while os.path.isdir(os.path.join(logfiledir , str(logsessionnumber))):
        logsessionnumber += 1

    #update log file directory using number
    logfiledir = os.path.join(logfiledir, str(logsessionnumber))
    os.mkdir(logfiledir)                

    try:
        while 1:
            #open serial port
            s = openserialport()
            
            #make log file
            logfile = os.path.join(logfiledir,logfilename + str(logfilenumber) + logfiletype)
            f = open(logfile,'w')

            while filesizecount <= filesize:
                now = time.time()
            
                line = readlineCR(s)
                data = csv2dict(line,keys)
            
                #display data
                if (now - displaytimer) >= displayrate:
                    print(data)
                    displaytimer = now
                
                #log data in csv
                if (now - logtimer) >= lograte:
                    f.write(line)
                    filesizecount += 1
                    logtimer = now
                if filesizecount == filesize:
                    f.close()
                    logfilenumber += 1
                    #make new log file
                    logfile = os.path.join(logfiledir,logfilename + str(logfilenumber) + logfiletype)
                    f = open(logfile,'a')
                    filesizecount = 0

    except KeyboardInterrupt:
        print('closing')
    
    f.close()
    s.close()

##################################
#this runs when the process closes
finally:
    os.unlink(pidfile)
##################################
