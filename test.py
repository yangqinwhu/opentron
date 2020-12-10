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

res = requests.get("http://127.0.0.1:8000",json={'hello':3})
res.text

import sys,json
# sys.path.append("/var/lib/jupyter/notebooks")
sys.path.append("/Users/chunxiao/Dropbox/python/aptitude_project/opentron")
from ams_protocols import saliva_to_dtt


def addtest(a=3,b=4):
    print (a+b)

d={'a':3}
e={"b":8}
addtest()
addtest(**d)
