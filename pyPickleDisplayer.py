import pickle
import time

while 1:
    try:
        data = pickle.load( open('data.pkl','rb'))
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        for keys in data:
            print(keys," ", data[keys])
        
    except EOFError:
        print('File open in another proccess')
        time.sleep(1)
    time.sleep(5)
