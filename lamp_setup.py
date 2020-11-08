"""Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""

from opentrons import protocol_api
# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import json,timeit,time
import common_task as ct


def _log_time(start_time,event = 'This step',print_log=1):
    stop = timeit.default_timer()
    run_time = stop - start_time
    unit = "sec" if run_time<60 else "min"
    run_time = run_time/60 if unit == "min" else run_time
    log ='{} takes {:.2} {}'.format(event,run_time,unit)
    print (log) if print_log else 1
    return run_time,log

# def heating(tm_deck,temp = 95, heat_time = 5):
#     """Set the temperature to temp, then heat for time (5) minutes
#     lower the temperature to 37C and deactivate the temp deck"""
#     import timeit,heat_time
#     temp,heat_time = temp,heat_time
#     start = timeit.default_timer()
#     tm_deck.set_temperature(temp)
#     ramp_time = timeit.default_timer() - start
#     time.sleep(heat_time*60)
#     tm_deck.set_temperature(25)
#     tm_deck.deactivate()

# def multi_transfer(s,d, b = 0,samp_vol= 100,air_vol = 25, buffer_vol = 0,simulate = False,get_time = 0):
    """ buffer_well
    s: source well
    d: destination well
    Transfer from source well: s to destination well"""
        #print ("Transfering saliva samples in rack {} column {}:".format(1,2))
    multi_pipette.flow_rate.aspirate = 120
    multi_pipette.flow_rate.dispense = 120

    start = timeit.default_timer()
    st = timeit.default_timer() if get_time else 1
    total_vol = samp_vol+air_vol+buffer_vol
    multi_pipette.pick_up_tip(presses=tip_presses, increment=tip_press_increment)
    _log_time(st,event = 'Pick up tip') if get_time else 1
    st = timeit.default_timer() if get_time else 1

    if buffer_vol !=0:
        multi_pipette.aspirate(buffer_vol, location = b.bottom(2))
        multi_pipette.air_gap(air_vol)
        total_vol +=air_vol
        _log_time(st,event = 'Aspirate DTT buffer') if get_time else 1
        st = timeit.default_timer() if get_time else 1
    multi_pipette.aspirate(samp_vol, s.bottom(10))
    multi_pipette.air_gap(air_vol)
    _log_time(st,event = 'Aspirate saliva') if get_time else 1
    st = timeit.default_timer() if get_time else 1

    multi_pipette.dispense(total_vol, d.bottom(5))
    _log_time(st,event = 'Dispense saliva') if get_time else 1
    st = timeit.default_timer() if get_time else 1
    multi_pipette.flow_rate.dispense = 40
    multi_pipette.mix(1,int(total_vol/2))
    multi_pipette.air_gap(air_vol)
    _log_time(st,event = 'Mix saliva dtt') if get_time else 1
    st = timeit.default_timer() if get_time else 1
    stop = timeit.default_timer()

    if simulate:
        multi_pipette.return_tip()
        st = timeit.default_timer() if get_time else 1
    else:
        multi_pipette.drop_tip()
        _log_time(st,event = 'Drop tip') if get_time else 1
        st = timeit.default_timer() if get_time else 1
    run_time = st - start
    dest_well = d
    return run_time,dest_well,stop


LABWARE_DEF_JSON = """{"ordering":[["A1","B1","C1","D1"],["A2","B2","C2","D2"],["A3","B3","C3","D3"],["A4","B4","C4","D4"],["A5","B5","C5","D5"],["A6","B6","C6","D6"]],"brand":{"brand":"ams2401","brandId":[]},"metadata":{"displayName":"ams2401 5ml rack","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.47,"zDimension":72},"wells":{"A1":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":18.38,"y":69.73,"z":22},"B1":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":18.38,"y":51.83,"z":22},"C1":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":18.38,"y":33.93,"z":22},"D1":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":18.38,"y":16.03,"z":22},"A2":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":36.28,"y":69.73,"z":22},"B2":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":36.28,"y":51.83,"z":22},"C2":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":36.28,"y":33.93,"z":22},"D2":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":36.28,"y":16.03,"z":22},"A3":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":54.18,"y":69.73,"z":22},"B3":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":54.18,"y":51.83,"z":22},"C3":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":54.18,"y":33.93,"z":22},"D3":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":54.18,"y":16.03,"z":22},"A4":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":72.08,"y":69.73,"z":22},"B4":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":72.08,"y":51.83,"z":22},"C4":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":72.08,"y":33.93,"z":22},"D4":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":72.08,"y":16.03,"z":22},"A5":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":89.98,"y":69.73,"z":22},"B5":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":89.98,"y":51.83,"z":22},"C5":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":89.98,"y":33.93,"z":22},"D5":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":89.98,"y":16.03,"z":22},"A6":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":107.88,"y":69.73,"z":22},"B6":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":107.88,"y":51.83,"z":22},"C6":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":107.88,"y":33.93,"z":22},"D6":{"depth":50,"totalLiquidVolume":5000,"shape":"circular","diameter":14.2,"x":107.88,"y":16.03,"z":22}},"groups":[{"metadata":{"wellBottomShape":"v"},"wells":["A1","B1","C1","D1","A2","B2","C2","D2","A3","B3","C3","D3","A4","B4","C4","D4","A5","B5","C5","D5","A6","B6","C6","D6"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"ams2401_24_wellplate_5000ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}"""
saliva_rack = json.loads(LABWARE_DEF_JSON)
LABWARE_LABEL = saliva_rack.get('metadata', {}).get(
    'displayName', 'test labware')

# metadata = {
#     'protocolName': 'Saliva to DTT',
#     'apiLevel': '2.1'
# }


# protocol = opentrons.execute.get_protocol_api('2.7')
protocol = ct.initialize()


# load labware and pipettes
p200_tip_name = "opentrons_96_filtertiprack_200ul"
p200_tip_slots = ["2","3"]
p10_tip_name = "opentrons_96_filtertiprack_20ul"
p10_tip_slots = ["11"]
right_pip_name = "p300_multi"
left_pip_name = "p300_multi"
plate_name = 'nest_96_wellplate_100ul_pcr_full_skirt'
plate_slot ="7"
lampMM_plate_slot = '8'
dtt_slot = "1"
rack_name = saliva_rack
rack_slots = ["5","6"]
temp_module_slot = '9'

p200_tips = [protocol.load_labware(p200_tip_name, slot) for slot in p200_tip_slots]
p10_tips = [protocol.load_labware(p10_tip_name, slot) for slot in p10_tip_slots]
# single_pipette = protocol.load_instrument(right_pip_name, 'right', tip_racks=p10_tips)
multi_pipette_2 = protocol.load_instrument(right_pip_name, 'right', tip_racks=p200_tips)
multi_pipette_1 = protocol.load_instrument(left_pip_name, 'left', tip_racks=p200_tips)
multi_pipette = multi_pipette_1
src_racks = [protocol.load_labware_from_definition(rack_name,slot) for slot in rack_slots]
src_tubes = src_racks[0].rows()[0]+src_racks[1].rows()[0]
dtt_plate = protocol.load_labware(plate_name, dtt_slot)
lampMM_plate = protocol.load_labware(plate_name, lampMM_plate_slot)

load_tm=False
if load_tm:
    tm_deck = protocol.load_module('Temperature Module', temp_module_slot)
    dest_plate = tm_deck.load_labware(plate_name)
else:
    dest_plate = protocol.load_labware(plate_name, temp_module_slot)




# sample info
samp_vol = 50
disp = 2
buffer_vol = int(samp_vol/4)
air_vol = 20
samples = 48



start_all = timeit.default_timer()
sample_c = int((samples-1)/4)+1
wells = []
incubation_start_times =[]
for s, d,b in zip(src_tubes[:sample_c],dest_plate.rows()[0][:sample_c],dtt_plate.rows()[0][:sample_c]):
    print ("Start transfering Saliva to 96 well plate")
    run_time,well,incubation_start_time = ct.p_transfer(multi_pipette,s,d,b,samp_vol = samp_vol,buffer_vol=0,get_time=1,disp=disp,mix=0)
    wells.append(well)
    incubation_start_times.append(incubation_start_time)
    print ("Total transfer time for 4 samples is {} second".format(run_time))

# for s,d,t in zip(wells,lampMM_plate.rows()[0][:len(wells)],incubation_start_times):
#     start = timeit.default_timer()
#     t0 = start-t
#     print ("Sample already on hot plate for {} minutes.".format(t0/60))
#     if t0 >300:
#         print ("Sample already on hot plate for {} minutes.".format(t0/60))
#     else:
#         time.sleep(300-t0)
#     multi_transfer(s,d)

_log_time(start_all, 'Total run time for {} columns'.format(sample_c))
