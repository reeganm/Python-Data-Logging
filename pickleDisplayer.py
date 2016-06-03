import pickle
import time

while 1:
    try:
        data = pickle.load( open('data.pkl','rb'))
        print(data)
        time.sleep(0.5)
    except EOFError:
        print('File open in another proccess')
        time.sleep(1)

