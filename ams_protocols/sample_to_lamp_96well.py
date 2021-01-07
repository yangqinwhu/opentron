"""Saliva to LAMP reaction
Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""


# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import sys,json
# sys.path.append("/var/lib/jupyter/notebooks")
sys.path.append("/Users/chunxiao/Dropbox/python/aptitude_project/opentron")
from opentrons import protocol_api
import json,timeit,time
import common_task as ct
import importlib
importlib.reload(ct)

def _split_volume(samp_vol,rev_vol,n):
    if (samp_vol+rev_vol)>10:
        samp_vol=samp_vol/2
        n*=2
        return samp_vol,rev_vol,n
    else:
        return samp_vol,rev_vol,n

def initialize_robot(deck = "sample_to_lamp_96well",simulate = True,**kwarg):
    ct.load_deck(deck,simulate = simulate)
    deck_plan = ct.protocol.deck
    pipette = ct.multi_pipette
    return deck_plan

def pause_robot():
    ct.protocol.pause(msg="robot paused")
    status = "robot paused"

def resume_robot():
    ct.protocol.resume()
    status = "protocol resumed"


def run_batch(start_tip=1,start_tube=1,start_dest=1,batch=1,samples=8,sample_per_column=8,replicates=1,aspirate_rate=0,dispense_rate=0,repl_chg_tip=False,**kwarg):
    """
    Pipette: P20 mounted on the right
    1st set of labwares:
    2,
    Current run uses the multi pipette P300 mounted on the left
    To do
    1. Insert manual pause """
    print ("###################### BATCH BEGIN ########################")
    print ("Batch # {} running".format(batch))
    src_tubes = ct.src_tubes
    dest_tubes = ct.dest_plate.rows()[0]+ct.dest_plate_2.rows()[0]
    p = ct.multi_pipette
    p.tip_racks = ct.tips+ct.tips_2
    # start_tip=1
    p.reset_tipracks()
    p.starting_tip=ct.tips[0].rows()[0][start_tip-1]
    p.trash_container = ct.trash

    # p.flow_rate.aspirate = aspirate_rate
    # p.flow_rate.dispense = dispense_rate
    start = timeit.default_timer()
    sample_c = int((samples-1)/sample_per_column)+1
    sts=[]
    for i in src_tubes[(start_tube-1):(sample_c+start_tube-1)]:
        for j in range(0,replicates):
            sts.append(i)
    dts = dest_tubes[(start_dest-1):(sample_c*replicates+start_dest-1)]
    # print (len(sts))
    # print (len(dts))
    if len(sts)>len(dts):
        raise Exception("Destination plate well is less than sample well. Please double check sample and replicate number.")

    rev_vol=kwarg["reverse_vol"]
    samp_vol=kwarg["samp_vol"]
    rev_status=0
    total_vol=rev_vol+samp_vol
    for i, (s, d) in enumerate(zip(sts,dts)):
        p.trash_container = ct.trash_2 if i > 11 else ct.trash
        # print ("Start transfering sample to lamp MM plate")
        if repl_chg_tip == False and (i+1)%replicates!=0:
            kwarg.update({"chgTip":0})
        else:
            kwarg.update({"chgTip":1})

        if rev_status==0:
            kwarg.update({"reverse_pip":1})
            rev_status=1
        else:
            kwarg.update({"reverse_pip":0})
        run_time,well,incubation_start_time = ct.p_transfer(p,s,d,**kwarg)
        rev_status=0 if kwarg["chgTip"] else 1
        print ("Total transfer time for {} samples is {:.2f} second".format(samples,run_time))
    ct._log_time(start, 'Total run time for {:.2f} columns'.format(sample_c))
    print ("####################### BATCH END ######################")

def run(total_batch=2,start_batch=1,**kwarg):
    batch = start_batch%2
    while batch <= total_batch:
        run_batch(batch=batch,**kwarg)
        batch+=1

def test_run():
    """This function is to run this file locally with all the parameters"""
    sample_info={
        "samples":16,
        "sample_per_column":8,
        "replicates":3,
        "repl_chg_tip":0,
        "total_batch":1,
        "start_batch":1,
        "start_tube":1,
        "start_dest":1,
        "start_tip":1,
    }
    transfer_param={
        "samp_vol":10,
        "reverse_vol":3,
        "air_vol": 0,
        "disp":1,
        "asp_bottom":0,
        "disp_bottom":0,
        'mix':0,
        "get_time":1,
        'returnTip':False,
        "aspirate_rate": 7.6,
        "dispense_rate": 7.6,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    }
    initialize_robot(deck = "sample_to_lamp_96well",simulate = True)
    run(**sample_info,**transfer_param)

test_run()
