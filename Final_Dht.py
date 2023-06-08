import paho.mqtt.client as mqtt
import json
import time
import sys
from pymata4 import pymata4

"""
Setup a pin for dht mode
One pin is set for a dht22 and another for dht11
Both polling and callback are being used in this example.
"""

#
POLL_TIME = 10 # number of seconds between polls

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


#def on_publish(client, userdata, mid):
    

client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_publish = on_publish
# address : localhost, port: 1883 에 연결
client.connect('59.1.188.107', 3883)
client.loop_start()
# common topic 으로 메세지 발행

def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred
    :param data: [report_type, pin, dht_type, error_value,
                  humidity, temperature, timestamp]
    """
    
    temp = data[5] 
    if temp > 30 :
        temp = temp +30
    print(f'{temp}')
    message = temp
        
        
    
    client.publish("Detector", json.dumps(message))
def dht(board, callback=None):
    """
     This function establishes the pin as a
     digital input. Any changes on this pin will
     be reported through the call back function.
     :param my_board: a pymata4 instance
     :param callback: callback funtion
     """
    # set the pin mode - for pin 6 differential is set explicitly
    board.set_pin_mode_dht(4, sensor_type=11, differential=.05, callback=callback)
    
    try:
        message = {}
   
        while True:
    
            # poll the first dht
         value = board.dht_read(4)
         if len(value)>= 6:

            
            temp = value[5] 
            if temp > 30 :
                temp = temp +30
            print(f'{temp}') 

            message = temp
                
            
                  
            client.publish('Detector', json.dumps(message))
            

    except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)


board = pymata4.Pymata4()

for i in range(100):
    dht(board, the_callback)
    time.sleep(POLL_TIME)
