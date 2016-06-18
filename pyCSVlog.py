#script for Loging CSV data from Serial

import serial
import time
import os
import sys
import pickle
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
port = 'COM4'
baud = '9600'
endline = b'\n'
delimiter = ','

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

allowedchars = [ ord(b'0'),ord(b'1')]

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
        print(rv)
        return(rv)
            
try:
    #put actual code here

    #csv format
    keys = ['value']

    ##SETTINGS##
    #log file
    filesize = 5000
    #http://stackoverflow.com/questions/647769/why-cant-pythons-raw-string-literals-end-with-a-single-backslash
    logfiledir = r"C:\Users\Reegan\Documents\GitHub\Python-Data-Logging\Log"
    logfilename = 'log'
    logfiletype = '.csv'
    logfilenumber = 0
    logsessionnumber = 0
    lograte = 0.1
    #display
    displayrate = 1.0
    #pickle
    picklerate = 0.25
    picklefile = r"data.pkl"

    #variables for timing
    logtimer = 0
    pickletimer = 0
    displaytimer = 0

    #keeping track of file number
    filesizecount = 0

    if not os.path.exists(logfiledir):
        os.makedirs(logfiledir)

    #scan log directory to determine number
    #http://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python#8933290
    while os.path.isdir(os.path.join(logfiledir , str(logsessionnumber))):
        logsessionnumber += 1

    #update log file directory using number
    logfiledir = os.path.join(logfiledir, str(logsessionnumber))
    os.mkdir(logfiledir)                

                 

    def csv2dict(line,keys):
        #split line 
        d = line.split(delimiter)
        #zip into dictionary
        data = dict(zip(keys,d))
        return data

    #displaying csv
        
    try:
        while 1:
            s = openserialport()
            #make log file
            logfile = os.path.join(logfiledir,logfilename + str(logfilenumber) + logfiletype)
            f = open(logfile,'w')

            #open pickle file
            fp = open(picklefile,"wb")
        
            while filesizecount <= filesize:
                now = time.time()
            
                readlineCR(s)
                line = '1,2,3'
                data = csv2dict(line,keys)
            
                #display data
                if (now - displaytimer) >= displayrate:
                    #print(data)
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

                #pickle data
                if (now - pickletimer) >= picklerate:
                    try:
                        fp = open(picklefile,"wb")
                        pickle.dump(data,fp)
                        pickletimer = now
                    except EOFError:
                        print('open file open in another process')
                    fp.close()

                
    except KeyboardInterrupt:
        print('closing')
    
    f.close()
    fp.close()
    s.close()

##################################
#this runs when the process closes
finally:
    os.unlink(pidfile)
##################################
