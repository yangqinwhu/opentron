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


def _conca_param(**kwarg):
    param={}
    for k,i in kwarg.items():
        try:
            param={**param,**i}
        except:
            param=param
    return param

def initialize_robot(**kwarg):
    global r
    r=ct.RunRobot(**_conca_param(**kwarg))

def aliquot_dtt(**kwarg):
    """This function is to run this file locally with all the parameters"""
    r.aliquot_dtt_p100(**_conca_param(**kwarg))

def aliquot_lamp(**kwarg):
    """This function is to run this file locally with all the parameters"""
    r.init_protocol(**_conca_param(**kwarg))
    r.aliquot_lamp_p100(**_conca_param(**kwarg))

def run(**kwarg):
    if kwarg["protocol"]["run"]=="aliquotDTT":
        aliquot_dtt(**kwarg)
    elif kwarg["protocol"]["run"]=="aliquotLamp":
        aliquot_lamp(**kwarg)


def test_run_p100():
    run_param={
        "robot_param":{
            "simulate":True,
            "deck":"saliva_to_dtt_micronic_96_wellplate_1400ul",
        },
        "sample_info":{
            "target_c":10,
            "target_p":2,
            "samples":8,
            "sample_per_column":8,
            "total_batch":1,
            "start_batch":1,
            "start_tube":1,
            "start_dest":1,
            "start_tip":1,
            "replicates":1,
        },
        "transfer_param":{
            "samp_vol":15,
            "reverse_vol":10,
            "air_vol": 0,
            "disp":5,
            "asp_bottom":-2,
            "disp_bottom":-10,
            'mix':0,
            "get_time":1,
            'returnTip':False,
            "aspirate_rate": 120,
            "dispense_rate": 20,
            "tip_press_increment":0.3,
            "tip_presses" : 1,
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
        "robot_param":{
            "simulate":True,
            "deck":"saliva_to_dtt_micronic_96_wellplate_1400ul",
        },
        "sample_info":{
            "target_c":10,
            "target_p":2,
            "samples":8,
            "sample_per_column":8,
            "total_batch":1,
            "start_batch":1,
            "start_tube":1,
            "start_dest":1,
            "start_tip":1,
            "replicates":1,
        },
        "transfer_param":{
            "samp_vol":15,
            "reverse_vol":10,
            "air_vol": 0,
            "disp":5,
            "asp_bottom":-2,
            "disp_bottom":-10,
            'mix':0,
            "get_time":1,
            'returnTip':False,
            "aspirate_rate": 120,
            "dispense_rate": 20,
            "tip_press_increment":0.3,
            "tip_presses" : 1,
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


# test_run_p100()
