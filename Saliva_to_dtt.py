"""Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""

from opentrons import protocol_api
# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import json,timeit,time
import common_task as ct



protocol = ct.load_deck(simulate=True)

# sample info
samp_vol = 50
disp = 2
buffer_vol = int(samp_vol/4)
air_vol = 25
samples = 48
p300m = ct.multi_pipette
p300m.trash_container = ct.trash

p300m.reset_tipracks()
start = timeit.default_timer()
sample_c = int((samples-1)/4)+1
for s, d in zip(ct.src_tubes[:sample_c],ct.dest_plate.rows()[0][:sample_c]):
    print ("Start transfering Saliva to 96 well plate")
    run_time,well,incubation_start_time = ct.p_transfer(p300m,s,d,samp_vol = samp_vol,buffer_vol=0,get_time=1,disp=disp,mix=0)
    print ("Total transfer time for 4 samples is {} second".format(run_time))
ct._log_time(start, 'Total run time for {} columns'.format(sample_c))
