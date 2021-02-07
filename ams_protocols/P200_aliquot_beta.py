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
# importlib.reload(ct)


def _log_time(start_time,event = 'This step',print_log=1):
    stop = timeit.default_timer()
    run_time = stop - start_time
    unit = "sec" if run_time<60 else "min"
    run_time = run_time/60 if unit == "min" else run_time
    log ='{} takes {:.2} {}'.format(event,run_time,unit)
    print (log)

def _conca_param(**kwarg):
    param={}
    for k,i in kwarg.items():
        try:
            param={**param,**i}
        except:
            param=param
    return param

def prot_deco(func):
    def inner(**kwarg):
        start = timeit.default_timer()
        print (f'******************** {kwarg["protocol"]["run"]} ****************')
        r.init_protocol(**_conca_param(**kwarg))
        func(**kwarg)
        _log_time(start,event = kwarg["protocol"]["run"])
        r.statusQ.put("RUN FINISHED")
    return inner

def initialize_robot(**kwarg):
    global r
    r=ct.RunRobot(**_conca_param(**kwarg))
    r.statusQ.put("INITIALIZED")

@prot_deco
def aliquot_dtt(**kwarg):
    r.aliquot_dtt_p100(**_conca_param(**kwarg))


@prot_deco
def aliquot_lamp(**kwarg):
    r.aliquot_lamp_p100(**_conca_param(**kwarg))

@prot_deco
def sample_to_lamp(**kwarg):
    r.sample_to_lamp(**_conca_param(**kwarg))

@prot_deco
def aliquot_dtt_p20(**kwarg):
    r.aliquot_dtt_p20(**_conca_param(**kwarg))

@prot_deco
def aliquot_lamp_p20(**kwarg):
    r.aliquot_lamp_p20(**_conca_param(**kwarg))

@prot_deco
def aliquot_lamp_p20_noNBC(**kwarg):
    r.aliquot_lamp_p20_noNBC(**_conca_param(**kwarg))

def deactivate_tm():
    r.robot.tm_deck.deactivate()

def set_temp():
    r.robot.tm_deck.start_set_temperature(4)

def run(**kwarg):
    if kwarg["protocol"]["run"]=="aliquotDTT":
        aliquot_dtt(**kwarg)
    elif kwarg["protocol"]["run"]=="aliquotLamp":
        aliquot_lamp(**kwarg)
    elif kwarg["protocol"]["run"]=="sampleToLamp":
        sample_to_lamp(**kwarg)
    elif kwarg["protocol"]["run"]=="aliquotDTTP20":
        aliquot_dtt_p20(**kwarg)
    elif kwarg["protocol"]["run"]=="aliquotLampP20":
        aliquot_lamp_p20(**kwarg)
    elif kwarg["protocol"]["run"]=="aliquotLampP20noNBC":
        aliquot_lamp_p20_noNBC(**kwarg)
    elif kwarg["protocol"]["run"]=="set_temp":
        set_temp()
    elif kwarg["protocol"]["run"]=="deactivate_tm":
        deactivate_tm()


def test_run_p100():
    run_param={
        "protocol":{
        "file":"p200_aliquot",
        "run":"p200_aliqot"
        },
        "robot_param":{
            "simulate":True,
            "deck":"saliva_to_dtt_micronic_96_wellplate_1400ul",
        },
        "sample_info":{
            "target_columns":12,
            "target_plates":1,
            "samples":8,
            "sample_per_column":8,
            "total_batch":1,
            "start_batch":1,
            "start_tube":1,
            "start_dest":1,
            "start_tip":2,
            "replicates":1,
        },
        "transfer_param":{
            "samp_vol":15,
            "reverse_vol":15,
            "src_vol":150,
            "air_vol": 0,
            "disp":5,
            "asp_bottom":-3,
            "disp_bottom":-8,
            'mix':0,
            "get_time":1,
            'returnTip':False,
            "aspirate_rate": 60,
            "dispense_rate": 40,
            "tip_press_increment":0.6,
            "tip_presses" : 3,
        },
        "deck_param":{"tip_name":"opentrons_96_filtertiprack_200ul",
            "tip_slots":["7","8"],
            "pip_name":"p300_multi",
            "pip_location":"left",
            "trash_slot":"9",
            "src_name":"None",
            "src_slots": ["2"],
            "dest_name": 'nest_96_wellplate_100ul_pcr_full_skirt',
            "dest_slots":["5","6","10","11","1"]
        }
    }

    initialize_robot(**run_param)
    aliquot_dtt(**run_param)

def test_run_p20():
    run_param={
        "protocol":{
        "file":"p200_aliquot",
        "run":"sampleToLamp"
        },
        "robot_status":{
            "initialized":0,
            "to_run":1,
        },
        "robot_param":{
            "simulate":True,
            "deck":"sample_to_lamp_96well_n7_rp4",
            "tm":"",
            "tm_temp":4,
        },
        "sample_info":{
            "target_columns":3,
            "target_plates":1,
            "samples":8,
            "sample_per_column":8,
            "total_batch":1,
            "start_batch":1,
            "start_tube":1,
            "start_dest":1,
            "start_tip":2,
            "replicates":2,
            "repl_chg_tip":0,
        },
        "transfer_param":{
            "samp_vol":5,
            "reverse_vol":5,
            "src_vol":350,
            "rp4":1,
            "air_vol": 0,
            "disp":1,
            "asp_bottom":11,
            "disp_bottom":0,
            'mix':0,
            "get_time":1,
            'returnTip':False,
            "aspirate_rate": 7.6,
            "dispense_rate": 7.6,
            "tip_press_increment":0.3,
            "tip_presses" : 1,
        },
        "deck_param":{"tip_name":"opentrons_96_filtertiprack_20ul",
            "tip_slots":["7","8"],
            "pip_name":"p20_multi_gen2",
            "pip_location":"right",
            "trash_slots":["9","6"],
            "src_name":'nest_96_wellplate_100ul_pcr_full_skirt',
            "src_slots": ["5"],
            "dest_name": 'nest_96_wellplate_100ul_pcr_full_skirt',
            "dest_slots":["1","2","3","4"],
            "tm_name":'nest_96_wellplate_100ul_pcr_full_skirt',
            "temp_module_slot": ["10"],
        }
    }

    initialize_robot(**run_param)
    # aliquot_lamp_p20_noNBC(**run_param)
    # sample_to_lamp(**run_param)
    aliquot_lamp_p20(**run_param)
    aliquot_dtt_p20(**run_param)
    

#

# while r.statusQ.not_empty:
#     print (r.statusQ.get())
#     time.sleep(0.1)
#     continue

if __name__ == "__main__":
    test_run_p20()
