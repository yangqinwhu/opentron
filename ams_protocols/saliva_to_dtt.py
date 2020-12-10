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
# sys.path.append("/var/lib/jupyter/notebooks")
sys.path.append("/Users/chunxiao/Dropbox/python/aptitude_project/opentron")
importlib.reload(ct)


ct.load_deck("saliva_to_dtt_biobank_96well_1000ul",simulate = True)
deck_plan = ct.protocol.deck
pipette = ct.multi_pipette
# sample info

# samp_vol = 50
# disp = 1
# air_vol = 25
# samples = 96
# sample_per_column = 8
# total_batch = 1

sample_info={
    "samples":48,
    "sample_per_column":8,
    "total_batch":2,
    "start_batch":1,
}
transfer_param={
    "samp_vol":50,
    "air_vol": 25,
    "disp":1,
    "asp_bottom":10,
    "disp_bottom":2,
    'mix':0,
    "get_time":1,
    'dry_run':True
}

def run_batch(batch=1,samples=8,sample_per_column=8,**kwarg):
    """
    Pipette: P300 mounted on the left
    1st set of labwares:
    2,
    Current run uses the multi pipette P300 mounted on the left
    To do
    1. Insert manual pause """
    print ("###################### BEGIN ########################")
    print ("Batch # {} running".format(batch))
    if batch%2:
        src_tubes = ct.src_tubes
        dest_plate = ct.dest_plate
        p300m = ct.multi_pipette
        p300m.tip_racks = ct.p200_tips
        tip_start = ct.p200_tips[0]['A1']
        p300m.reset_tipracks()
        p300m.trash_container = ct.trash
    else:
        src_tubes = ct.src_tubes_2
        dest_plate = ct.dest_plate_2
        p300m = ct.multi_pipette
        p300m.tip_racks = ct.p200_tips_2
        tip_start = ct.p200_tips_2[0]['A1']
        p300m.reset_tipracks()
        p300m.trash_container = ct.trash_2

    p=p300m
    start = timeit.default_timer()
    sample_c = int((samples-1)/sample_per_column)+1
    for s, d in zip(src_tubes[:sample_c],dest_plate.rows()[0][:sample_c]):
        print ("Start transfering Saliva to 96 well plate")
        run_time,well,incubation_start_time = ct.p_transfer(p,s,d,**kwarg)
        print ("Total transfer time for {} samples is {:.2f} second".format(samples,run_time))

    batch +=1
    ct._log_time(start, 'Total run time for {:.2f} columns'.format(sample_c))
    print ("####################### END ######################")

def run(total_batch=2,start_batch=1,**kwarg):
    batch = start_batch%2
    while batch <= total_batch:
        run_batch(batch=batch,**kwarg)
        batch+=1


run(**sample_info,**transfer_param)
