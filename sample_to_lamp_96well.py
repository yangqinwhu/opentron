"""Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""

from opentrons import protocol_api
# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import json,timeit,time
import common_task as ct
import importlib
importlib.reload(ct)

ct.load_deck("sample_to_lamp_96well",simulate = True)
deck_plan = ct.protocol.deck
pipette = ct.multi_pipette
# sample info
deck_plan
samp_vol = 5
disp = 1
air_vol = 0
samples = 8
sample_per_column = 8
total_batch = 1
replicates = 4 # i.e. one saliva sample into multiple MM. Default is 2, one for N7 and one for RP4

def run(asp_bottom=0,disp_bottom=0):
    """
    Pipette: P20 mounted on the right
    1st set of labwares:
    2,
    Current run uses the multi pipette P300 mounted on the left
    To do
    1. Insert manual pause """
    batch = 1
    while batch <=total_batch:
        print ("###################### BEGIN ########################")
        print ("Batch # {} running".format(batch))
        src_tubes = ct.src_tubes
        dest_tubes = ct.dest_plate.rows()[0]+ct.dest_plate_2.rows()[0]
        p = ct.multi_pipette
        p.tip_racks = ct.p20_tips+ct.p20_tips_2
        tip_start = ct.p20_tips[0]['A1']
        p.reset_tipracks()
        p.trash_container = ct.trash


        start = timeit.default_timer()
        sample_c = int((samples-1)/sample_per_column)+1
        sts=[]
        for i in src_tubes[:sample_c]:
            for j in range(0,replicates):
                sts.append(i)
        dts = dest_tubes[:sample_c*replicates]
        print (len(sts))
        print (len(dts))
        if len(sts)>len(dts):
            raise Exception("Destination plate well is less than sample well. Please double check sample and replicate number.")
        for i, (s, d) in enumerate(zip(sts,dts)):
            p.trash_container = ct.trash_2 if i > 11 else ct.trash
            print ("Start transfering Saliva to 96 well plate")
            run_time,well,incubation_start_time = ct.p_transfer(p,s,d,samp_vol = samp_vol,asp_bottom =asp_bottom, disp_bottom =disp_bottom, air_vol=air_vol,get_time=1,disp=disp,mix=0,dry_run=False)
            print ("Total transfer time for 8 samples is {:.2f} second".format(run_time))

        batch +=1
        ct._log_time(start, 'Total run time for {:.2f} columns'.format(sample_c))
        print ("####################### END ######################")
