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


import time
from threading import Thread

answer = None

def check():
    time.sleep(2)
    if answer == "n":
        return
    print("Too Slow")

Thread(target = check).start()

answer = input("Input something: ")


a=[0,1,2]



from opentrons import protocol_api
# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import json,timeit,time
import common_task as ct


protocol = ct.load_deck(simulate=True)


protocol = ct.initialize(simulate=True)
p200_tip_name = "opentrons_96_filtertiprack_200ul"
p200_tip_slots = ["1","2"]
p200_tips_2 = [protocol.load_labware(p200_tip_name, slot) for slot in p200_tip_slots]
left_pip_name = "p300_multi"
multi_pipette = protocol.load_instrument(left_pip_name, 'left', tip_racks=p200_tips)
multi_pipette.tip_racks
multi_pipette_2 = multi_pipette
multi_pipette_2.tip_racks = p200_tips_2
multi_pipette_2.tip_racks
protocol.cleanup()
protocol.deck

2%1
2%2
3%2
4%2
1%2
