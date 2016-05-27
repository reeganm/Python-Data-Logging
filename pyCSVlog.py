#script for Loging CSV data from Serial

import serial
import time
import os
import pickle

##SETTINGS##
#serial
port = 'COM5'
baud = '115200'
endline = '\n'
#log file
filesize = 5000
filesizecount = 0
#http://stackoverflow.com/questions/647769/why-cant-pythons-raw-string-literals-end-with-a-single-backslash
logfiledir = r"C:\Users\Reegan\Documents\GitHub\Python-Data-Logging\Log"
logfilename = 'log'
logfiletype = '.csv'
logfilenumber = 0
logsessionnumber = 0
lograte = 0.05
#display
displayrate = 3.0
#pickle
picklerate = 1.0
picklefile = r"data.pkl"

#variables for timing
logtimer = 0
pickletimer = 0
displaytimer = 0

#data dictionary
data = {"data1":0}

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
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch==endline:
            return rv
try:
    while 1:
        #s = serial.Serial(port, baudrate=baud, timeout=3.0)

        #make log file
        logfile = os.path.join(logfiledir,logfilename + str(logfilenumber) + logfiletype)
        f = open(logfile,'a')

        #open pickle file
        fp = open(picklefile,"wb")
        
        while filesizecount <= filesize:
            #do stuff
            now = time.time()
            data["data1"] = "hi " + str(time.time()) + "\n"

            #display data
            if (now - displaytimer) >= displayrate:
                print(data)
                displaytimer = now
                
            #log data
            if (now - logtimer) >= lograte:
                f.write(data["data1"])
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
                pickle.dump(data,fp)
                pickletimer = now
                
except KeyboardInterrupt:
    f.close()
    fp.close()
