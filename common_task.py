from opentrons import protocol_api
import json,timeit,time

def _log_time(start_time,event = 'This step',print_log=1):
    stop = timeit.default_timer()
    run_time = stop - start_time
    unit = "sec" if run_time<60 else "min"
    run_time = run_time/60 if unit == "min" else run_time
    log ='{} takes {:.2} {}'.format(event,run_time,unit)
    print (log) if print_log else 1
    return run_time,log

def initialize(simulate =False,**kwarg):
    """
    connect, reset and home robot. create protocol variables to use.
    initialize is already built into load_deck(deck_plan).
    don't need to specifically use initialize.
    """
    metadata = {
        'protocolName': 'Saliva to DTT',
        'apiLevel': '2.7'
    }

    from opentrons import protocol_api
    import ams_labware as lw
    import sys
    # sys.path.append("/data/user_storage/opentrons_data/jupyter/modules_storage")
    # import labware_volume as lv
    global protocol,lw
    if simulate:
        import opentrons.simulate
        protocol = opentrons.simulate.get_protocol_api('2.1')
    else:
        import opentrons.execute # This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
        protocol = opentrons.execute.get_protocol_api('2.7')
    protocol = protocol
    protocol.home()
    return protocol

def load_deck(deck_plan='default',simulate =False,**kwarg):
    if deck_plan == 'default':
        global p200_tips,src_racks,src_tubes,trash,dest_plate,multi_pipette
        protocol = initialize(**kwarg)
        p200_tip_name = "opentrons_96_filtertiprack_200ul"
        p200_tip_slots = ["2","10"]
        left_pip_name = "p300_multi"
        plate_name = 'nest_96_wellplate_100ul_pcr_full_skirt'
        plate_slot ="6"
        rack_slots = ["3","9"]
        trash_slot="5"
        liquid_trash_rack=json.loads(lw.amsliquidtrash)
        saliva_rack = json.loads(lw.ams2401)

        p200_tips = [protocol.load_labware(p200_tip_name, slot) for slot in p200_tip_slots]
        src_racks = [protocol.load_labware_from_definition(saliva_rack,slot) for slot in rack_slots]
        src_tubes = src_racks[0].rows()[0]+src_racks[1].rows()[0]
        trash = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot)
        dest_plate = protocol.load_labware(plate_name, plate_slot)
        multi_pipette = protocol.load_instrument(left_pip_name, 'left', tip_racks=p200_tips)


def p_dispense(pipette,well,volume,disp=1):
    """ Use pipette to perform multiple dispense
    volume: sample volume for each dispense
    dis: dispense times
    destination well by default is well + dis"""
    def _next_row_well(w):
        """return the well in the next row. E.g. A1 well to B1 well"""
        p=w.parent
        w_name = w._display_name.split(' ')[0]
        row =  w_name[0]
        column = w_name[1:].strip()
        new_row = chr(ord(row) + 1)
        n_r_w= p[new_row+column]
        return n_r_w

    for i in range(0,disp):
        print ("current dispensing well is {}".format(well))
        pipette.dispense(volume, well.bottom(3))
        well = _next_row_well(well)

def p_transfer(pipette,s,d, b = 0,samp_vol= 50,air_vol = 25,mix=0, buffer_vol = 0,simulate = False,get_time = 0,disp=2):
    """ s: source well  d: destination well b: buffer well.
    dispense: how many times the same to be dispensed
    Transfer from source well: s to destination well"""
        #print ("Transfering saliva samples in rack {} column {}:".format(1,2))
    #set up pipette parameter
    multi_pipette = pipette
    multi_pipette.flow_rate.aspirate = 120
    multi_pipette.flow_rate.dispense = 120
    tip_press_increment=0.4
    tip_presses = 1

    #pipette parameters
    asp_vol = (samp_vol*disp)*1.1
    print ("asp volume: ", int(asp_vol))
    total_vol = asp_vol+air_vol+buffer_vol

    start = timeit.default_timer()
    st = timeit.default_timer() if get_time else 1
    multi_pipette.pick_up_tip(presses=tip_presses, increment=tip_press_increment)
    _log_time(st,event = 'Pick up tip') if get_time else 1
    st = timeit.default_timer() if get_time else 1

    if buffer_vol !=0:
        multi_pipette.aspirate(buffer_vol, location = b.bottom(2))
        multi_pipette.air_gap(air_vol)
        total_vol +=air_vol
        _log_time(st,event = 'Aspirate DTT buffer') if get_time else 1
        st = timeit.default_timer() if get_time else 1
    multi_pipette.aspirate(asp_vol, s.bottom(10))
    multi_pipette.air_gap(air_vol)
    _log_time(st,event = 'Aspirate saliva') if get_time else 1
    st = timeit.default_timer() if get_time else 1

    p_dispense(multi_pipette,d,air_vol) if air_vol >0 else 1
    p_dispense(multi_pipette,d,samp_vol,disp=disp)
    _log_time(st,event = 'Dispense saliva') if get_time else 1
    st = timeit.default_timer() if get_time else 1

    if mix >0:
        multi_pipette.flow_rate.dispense = 40
        multi_pipette.mix(mix,int(total_vol/2))
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
