"""Saliva to DTT: This protocol transfer saliva to DTT solution.
Disp: Same reagent dispense to mutiple wells without change tip. Current setting shift by row from A1 to B1, instead of A1 to A2.
Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""

from opentrons import protocol_api
# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import json,timeit,time
import common_task as ct
import importlib
import sys,json
sys.path.append("/var/lib/jupyter/notebooks")
sys.path.append("/Users/chunxiao/Dropbox/python/aptitude_project/opentron")
importlib.reload(ct)

status = ct.status

def initialize_robot(deck = "saliva_to_dtt_biobank_96well_1000ul",simulate = True,**kwarg):
    ct.load_deck(deck,simulate = simulate)
    deck_plan = ct.protocol.deck
    pipette = ct.multi_pipette
    return deck_plan


def run_batch(start_tube=1,batch=1,samples=8,sample_per_column=8,aspirate_rate=0,replicates=1,dispense_rate=0,**kwarg):
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
        src_tubes = ct.src_tubes
        dest_tubes = ct.dest_plate.rows()[0]
        p = ct.multi_pipette
        p.tip_racks = ct.tips
        tip_start = ct.tips[0]['A1']
        p.reset_tipracks()
        p.trash_container = ct.trash
    else:
        src_tubes = ct.src_tubes_2
        dest_tubes = ct.dest_plate_2.rows()[0]
        p = ct.multi_pipette
        p.tip_racks = ct.tips_2
        tip_start = ct.tips_2[0]['A1']
        p.reset_tipracks()
        p.trash_container = ct.trash_2

    p.flow_rate.aspirate = aspirate_rate
    p.flow_rate.dispense = dispense_rate
    start = timeit.default_timer()
    sample_c = int((samples-1)/sample_per_column)+1
    sts=[]
    for i in src_tubes[(start_tube-1):(sample_c+start_tube-1)]:
        for j in range(0,replicates):
            sts.append(i)
    dts = dest_tubes[(start_tube-1):(sample_c*replicates+start_tube-1)]
    print (len(sts))
    print (len(dts))
    if len(sts)>len(dts):
        raise Exception("Destination plate well is less than sample well. Please double check sample and replicate number.")
    for i, (s, d) in enumerate(zip(sts,dts)):
        print ("Start transfering Saliva to 96 well plate")
        run_time,well,incubation_start_time = ct.p_transfer(p,s,d,**kwarg)
        print ("Total transfer time for {} samples is {:.2f} second".format(samples,run_time))

    ct._log_time(start, 'Total run time for {:.2f} columns'.format(sample_c))
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
        "replicates":1,
    }
    transfer_param={
        "samp_vol":50,
        "air_vol": 25,
        "disp":1,
        "asp_bottom":10,
        "disp_bottom":2,
        'mix':0,
        "get_time":1,
        'dry_run':False,
        "aspirate_rate": 120,
        "dispense_rate": 120,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    }
    initialize_robot(deck = "saliva_to_dtt_biobank_96well_1000ul",simulate = True)
    run(**sample_info,**transfer_param)
