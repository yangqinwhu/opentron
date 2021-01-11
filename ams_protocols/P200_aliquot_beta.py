"""Saliva to DTT: This protocol transfer saliva to DTT solution.
Disp: Same reagent dispense to mutiple wells without change tip. Current setting shift by row from A1 to B1, instead of A1 to A2.
Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""

from opentrons import protocol_api
# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import json,timeit,time
import common_task_beta as ct
import importlib
import sys,json
sys.path.append("/var/lib/jupyter/notebooks")
sys.path.append("/Users/chunxiao/Dropbox/python/aptitude_project/opentron")
importlib.reload(ct)




def initialize_robot(deck = "saliva_to_dtt_micronic_96_wellplate_1400ul",simulate = True,**kwarg):
    rt.load_deck(deck,simulate = simulate)
    deck_plan = rt.protocol.deck
    pipette = rt.multi_pipette
    return deck_plan

def pause_robot():
    rt.protocol.pause(msg="robot paused")
    status = "robot paused"

def resume_robot():
    rt.protocol.resume()
    status = "protocol resumed"

def run_batch(start_tip=1,start_tube=1,start_dest=1,batch=1,samples=8,sample_per_column=8,aspirate_rate=0,replicates=1,dispense_rate=0,repl_chg_tip=False,**kwarg):
    """
    Pipette: P300 mounted on the left
    1st set of labwares:
    2,
    Current run uses the multi pipette P300 mounted on the left
    To do
    1. Insert manual pause """
    print ("###################### BATCH BEGIN ########################")
    print ("Batch # {} running".format(batch))
    if batch%2:
        src_tubes = rt.src_tubes
        dest_tubes = rt.dest_tubes
        p = rt.multi_pipette
        p.pipette.tip_racks = rt.tips
        p.pipette.reset_tipracks()
        p.pipette.starting_tip=rt.tips[0].rows()[0][start_tip-1]
        # p.trash_container = rt.trash


    p.pipette.flow_rate.aspirate = aspirate_rate
    p.pipette.flow_rate.dispense = dispense_rate
    start = timeit.default_timer()
    sample_c = int((samples-1)/sample_per_column)+1
    sts=[]
    for i in src_tubes[(start_tube-1):(sample_c+start_tube-1)]:
        for j in range(0,replicates):
            sts.append(i)
    dts = dest_tubes[(start_dest-1):(sample_c*replicates+start_dest-1)]
    print (len(sts))
    print (len(dts))
    if len(sts)>len(dts):
        raise Exception("Destination plate well is less than sample well. Please double check sample and replicate number.")

    rev_vol=kwarg["reverse_vol"]
    samp_vol=kwarg["samp_vol"]
    rev_status=0
    total_vol=rev_vol+samp_vol
    for i, (s, d) in enumerate(zip(sts,dts)):
        # p.trash_container = rt.trash_2 if i > 11 else rt.trash
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
        p.p_transfer(s,d,**kwarg)
        rev_status=0 if kwarg["chgTip"] else 1
    p._log_time(start, 'Total run time for {:.2f} columns'.format(sample_c))
    print ("####################### BATCH END ######################")

def run(total_batch=2,start_batch=1,**kwarg):
    batch = start_batch
    while batch <= total_batch:
        run_batch(batch=batch,**kwarg)
        batch+=1

def test_run():
    """This function is to run this file locally with all the parameters"""
    sample_info={
        "samples":8,
        "sample_per_column":8,
        "total_batch":1,
        "start_batch":1,
        "start_tube":1,
        "start_dest":1,
        "start_tip":2,
        "replicates":1,
    }
    transfer_param={
        "samp_vol":50,
        "reverse_vol":20,
        "air_vol": 25,
        "disp":1,
        "asp_bottom":10,
        "disp_bottom":2,
        'mix':0,
        "get_time":1,
        'returnTip':False,
        "aspirate_rate": 120,
        "dispense_rate": 120,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    }
    initialize_robot(deck = "saliva_to_dtt_micronic_96_wellplate_1400ul",simulate = True)
    run(**sample_info,**transfer_param)


def test_run2():
    """This function is to run this file locally with all the parameters"""
    sample_info={
        "samples":8,
        "sample_per_column":8,
        "total_batch":1,
        "start_batch":1,
        "start_tube":1,
        "start_dest":1,
        "start_tip":2,
        "replicates":1,
    }
    transfer_param={
        "samp_vol":50,
        "reverse_vol":20,
        "air_vol": 25,
        "disp":1,
        "asp_bottom":10,
        "disp_bottom":2,
        'mix':0,
        "get_time":1,
        'returnTip':False,
        "aspirate_rate": 120,
        "dispense_rate": 120,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    }
    run(**sample_info,**transfer_param)
rt=ct.robot()
test_run2()
