# from threading import Timer
# import time
#
# loop =1
# while loop:
#     print ("Run starts")
#     time.sleep(5)
#     timeout = 5
#     t = Timer(timeout, print, ['Sorry, times up'])
#     t.start()
#     prompt = "Conitune to next run?\n Press 'n' to stop the run."
#     answer = input(prompt)
#     if answer =="n" or answer =="N":
#         loop = 0
#         t.cancel()
#         print ("Run stopped")
#     else:
#         answer =1
#         t.cancel()


# import time
# from threading import Thread
#
# answer = None
#
# def check():
#     time.sleep(2)
#     if answer == "n":
#         return
#     print("Too Slow")
#
# Thread(target = check).start()
#
# answer = input("Input something: ")


##

import requests,json

server_ip = "192.168.1.46"
server_ip = "127.0.0.1"
PORT = 8000

sample_info={
    "samples":48,
    "sample_per_column":8,
    "total_batch":2,
    "start_batch":2,
}
transfer_param={
    "samp_vol":50,
    "air_vol": 25,
    "disp":1,
    "asp_bottom":10,
    "disp_bottom":2,
    'mix':0,
    "get_time":1,
    'dry_run':True,
    "aspirate_rate": 120,
    "dispense_rate": 120,
    "tip_press_increment":0.3,
    "tip_presses" : 1,
}

input = {**sample_info,**transfer_param}


res = requests.get("http://127.0.0.1:8000",json=input)
res.text
