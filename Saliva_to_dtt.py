"""Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""

from opentrons import protocol_api
# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import json,timeit,time
import common_task as ct
import importlib
importlib.reload(ct)

ct.load_deck("saliva_to_dtt_GEBplate",simulate = False)
deck_plan = ct.protocol.deck
pipette = ct.multi_pipette
# sample info

samp_vol = 50
disp = 2
air_vol = 25
samples = 4

def run():
    """
    Pipette: P300 mounted on the left
    1st set of labwares:
    2,
    Current run uses the multi pipette P300 mounted on the left
    To do
    1. Insert manual pause """
    batch = 1
    while batch <=2:
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

        start = timeit.default_timer()
        sample_c = int((samples-1)/4)+1
        for s, d in zip(src_tubes[:sample_c],dest_plate.rows()[0][:sample_c]):
            print ("Start transfering Saliva to 96 well plate")
            run_time,well,incubation_start_time = ct.p_transfer(p300m,s,d,samp_vol = samp_vol,get_time=1,disp=disp,mix=0)
            print ("Total transfer time for 4 samples is {:.2f} second".format(run_time))

        batch +=1
        ct._log_time(start, 'Total run time for {:.2f} columns'.format(sample_c))
        print ("####################### END ######################")



run()
