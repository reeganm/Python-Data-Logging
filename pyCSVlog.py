#!/usr/bin/env python3
#script for Loging CSV data from Serial

import serial
import time
import os
import pickle

#csv format
keys = ['x','y','z']

##SETTINGS##
#serial
port = '/dev/ttyUSB0'
baud = '115200'
endline = b'\n'
delimiter = ','
#log file
filesize = 5000
#http://stackoverflow.com/questions/647769/why-cant-pythons-raw-string-literals-end-with-a-single-backslash
logfiledir = r"/home/pi/Python-Data-Logging/Log"
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

def readlineCR(port):
    rv = b""
    while True:
        ch = port.read()
        rv += ch
        if ch==endline:
            rv = rv.decode("utf-8")
            return rv

def csv2dict(line,keys):
    line = line[0:len(line)-2] #remove endline
    #split line 
    d = line.split(delimiter)
    #zip into dictionary
    data = dict(zip(keys,d))
    return data

#displaying csv
        
try:
    while 1:
        s = serial.Serial(port, baudrate=baud, timeout=3.0)
        #make log file
        logfile = os.path.join(logfiledir,logfilename + str(logfilenumber) + logfiletype)
        f = open(logfile,'w')

        #open pickle file
        fp = open(picklefile,"wb")
        
        while filesizecount <= filesize:
            now = time.time()
            
            line = readlineCR(s)
 #           line = '1,2,3\n'
            data = csv2dict(line,keys)
            
            #display data
#            if (now - displaytimer) >= displayrate:
#                print(data)
#                displaytimer = now
                
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
