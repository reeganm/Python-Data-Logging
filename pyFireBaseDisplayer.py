import time
from firebase import firebase
import json

myDataBase = 'https://mydatabase-f7de1.firebaseio.com/'
refreshInterval = 5

firebase = firebase.FirebaseApplication(myDataBase,None)

while 1:
    result = firebase.get('/data','Current')
    data = json.loads(result)
    for key,value in sorted(data.items()):
        print(key + ': ' + str(data[key]))
    time.sleep(refreshInterval)
    
