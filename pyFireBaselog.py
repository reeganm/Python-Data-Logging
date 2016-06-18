import pickle
import time
import datetime
from firebase import firebase
import json
import os
import sys

#code that stops this process from running twice
pid = str(os.getpid()) #get process id
pidfile = 'pyFireBaselog.pid'

if os.path.isfile(pidfile):
    print("%s already exists, exiting",pidfile)
    sys.exit()
open(pidfile, 'w').write(pid) #create lock file
try:
    #put actual code here
    myDataBase = 'https://mydatabase-f7de1.firebaseio.com/'
    refreshInterval = 5

    firebase = firebase.FirebaseApplication(myDataBase,None)

    while 1:
        try:
            #load pickle file
            data = pickle.load( open('data.pkl','rb'))
            print(data)

            TimeStamp = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")

            #convert to json
            data_j = json.dumps(data)
        
            #update current data on server
            firebase.put('/data','Current',data_j)
            #have past log on server
            firebase.put('/data',TimeStamp,data_j)
        except EOFError:
            print('Unable to open pickle file')
        time.sleep(refreshInterval)
#this runs when the process closes
finally:
    os.unlink(pidfile)
