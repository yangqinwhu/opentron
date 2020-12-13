from opentrons import protocol_api
import json,timeit,time

class robot:
    """robot class to perform common_taks operation
    """
    def __init__(self):
        self.status = "idle"
        self.log =[]

    def _log_time(self,start_time,event = 'This step',print_log=1):
        stop = timeit.default_timer()
        run_time = stop - start_time
        unit = "sec" if run_time<60 else "min"
        run_time = run_time/60 if unit == "min" else run_time
        log ='{} takes {:.2} {}'.format(event,run_time,unit)
        print (log) if print_log else 1
        return log+'\n'

    def initialize(simulate =False,**kwarg):
        """
        connect, reset and home robot. create protocol variables to use.
        initialize is already built into load_deck(deck_plan).
        don't need to specifically use initialize.
        """
        metadata = {
            'protocolName': 'Saliva to DTT',
        }
        from opentrons import protocol_api
        import labwares.ams_labware as lw
        import sys
        # sys.path.append("/var/lib/jupyter/notebooks")
        # import labware_volume as lv
        global protocol,lw
        if simulate:
            import opentrons.simulate
            protocol = opentrons.simulate.get_protocol_api('2.1')
        else:
            import opentrons.execute # This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
            protocol = opentrons.execute.get_protocol_api('2.1')
        protocol = protocol
        protocol.home()
        return protocol

    def load_deck(deck_plan='saliva_to_dtt',simulate =False,**kwarg):
        global tips_2,src_racks_2,src_tubes_2,trash_2,dest_plate_2
        global tips,src_racks,src_tubes,trash,dest_plate,multi_pipette

        if deck_plan == 'saliva_to_dtt':
            # for 1st shift
            protocol = initialize(simulate =simulate,**kwarg)
            tip_name = "opentrons_96_filtertiprack_200ul"
            tip_slots = ["2","1"]
            left_pip_name = "p300_multi"
            plate_name = 'nest_96_wellplate_100ul_pcr_full_skirt'
            plate_slot ="6"
            rack_slots = ["3","9"]
            trash_slot="5"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)
            saliva_rack = json.loads(lw.ams2402)

            tips = [protocol.load_labware(tip_name, slot) for slot in tip_slots]
            src_racks = [protocol.load_labware_from_definition(saliva_rack,slot) for slot in rack_slots]
            src_tubes = src_racks[0].rows()[0]+src_racks[1].rows()[0]
            trash = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot)
            dest_plate = protocol.load_labware(plate_name, plate_slot)
            multi_pipette = protocol.load_instrument(left_pip_name, 'left', tip_racks=tips)
            multi_pipette.trash_container = trash
            # multi_pipette.drop_tips() if multi_pipette.has_tip else 1

            #for 2nd shift
            tip_name = "opentrons_96_filtertiprack_200ul"
            tip_slots_2 = ["11"]
            left_pip_name = "p300_multi"
            plate_name = 'nest_96_wellplate_100ul_pcr_full_skirt'
            plate_slot ="7"
            rack_slots = ["4","10"]
            trash_slot_2="8"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)
            saliva_rack = json.loads(lw.ams2401)

            tips_2 = [protocol.load_labware(tip_name, slot) for slot in tip_slots_2]
            src_racks_2 = [protocol.load_labware_from_definition(saliva_rack,slot) for slot in rack_slots]
            src_tubes_2 = src_racks_2[0].rows()[0]+src_racks_2[1].rows()[0]
            trash_2 = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot_2)
            dest_plate_2 = protocol.load_labware(plate_name, plate_slot)
            multi_pipette_2 = multi_pipette
    #         multi_pipette_2.tip_racks = tips_2
    #         multi_pipette_2.trash_container = trash_2
            # multi_pipette_2.drop_tips() if multi_pipette_2.has_tip else 1

        elif deck_plan == 'saliva_to_dtt_GEBplate':
            # for 1st shift
            protocol = initialize(simulate =simulate,**kwarg)
            tip_name = "opentrons_96_filtertiprack_200ul"
            tip_slots = ["2","1"]
            left_pip_name = "p300_multi"
            plate_name = json.loads(lw.geb_96_wellplate)
            plate_slot ="6"
            rack_slots = ["3","9"]
            trash_slot="5"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)
            saliva_rack = json.loads(lw.ams2402)

            tips = [protocol.load_labware(tip_name, slot) for slot in tip_slots]
            src_racks = [protocol.load_labware_from_definition(saliva_rack,slot) for slot in rack_slots]
            src_tubes = src_racks[0].rows()[0]+src_racks[1].rows()[0]
            trash = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot)
            dest_plate = protocol.load_labware_from_definition(plate_name, plate_slot)
            multi_pipette = protocol.load_instrument(left_pip_name, 'left', tip_racks=tips)
            multi_pipette.trash_container = trash
            # multi_pipette.drop_tips() if multi_pipette.has_tip else 1

            #for 2nd shift
            tip_name = "opentrons_96_filtertiprack_200ul"
            tip_slots_2 = ["11"]
            left_pip_name = "p300_multi"
            plate_name = json.loads(lw.geb_96_wellplate)
            plate_slot ="7"
            rack_slots = ["4","10"]
            trash_slot_2="8"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)
            saliva_rack = json.loads(lw.ams2402)

            tips_2 = [protocol.load_labware(tip_name, slot) for slot in tip_slots_2]
            src_racks_2 = [protocol.load_labware_from_definition(saliva_rack,slot) for slot in rack_slots]
            src_tubes_2 = src_racks_2[0].rows()[0]+src_racks_2[1].rows()[0]
            trash_2 = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot_2)
            dest_plate_2 = protocol.load_labware_from_definition(plate_name, plate_slot)
            multi_pipette_2 = multi_pipette
    #         multi_pipette_2.tip_racks = tips_2
    #         multi_pipette_2.trash_container = trash_2

        elif deck_plan == 'saliva_to_dtt_biobank_96well_1000ul':
            # for 1st shift
            protocol = initialize(simulate =simulate,**kwarg)
            tip_name = "opentrons_96_filtertiprack_200ul"
            tip_slots = ["5","1"]
            left_pip_name = "p300_multi"
            plate_name = 'nest_96_wellplate_100ul_pcr_full_skirt'
            plate_slot ="3"
            trash_slot="2"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)
            saliva_rack = json.loads(lw.biobank_96well_saliva_1000ul)
            rack_slots = ["6"]
            tips = [protocol.load_labware(tip_name, slot) for slot in tip_slots]
            src_racks = [protocol.load_labware_from_definition(saliva_rack,slot,"saliva rack batch 1: biobank_96well_1000ul") for slot in rack_slots]
            src_tubes=[]
            for i in range(0,len(rack_slots)):
                src_tubes += src_racks[i].rows()[0]
            trash = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot)
            dest_plate = protocol.load_labware(plate_name, plate_slot, "DTT plate batch 1: 96 well full skirt no adaptor" )
            multi_pipette = protocol.load_instrument(left_pip_name, 'left', tip_racks=tips)
            multi_pipette.trash_container = trash
            # multi_pipette.drop_tips() if multi_pipette.has_tip else 1

            #for 2nd shift
            tip_name = "opentrons_96_filtertiprack_200ul"
            tip_slots_2 = ["10"]
            left_pip_name = "p300_multi"
            plate_name = 'nest_96_wellplate_100ul_pcr_full_skirt'
            plate_slot ="8"
            trash_slot_2="7"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)
            saliva_rack = json.loads(lw.biobank_96well_saliva_1000ul)
            rack_slots = ["11"]

            tips_2 = [protocol.load_labware(tip_name, slot) for slot in tip_slots_2]
            src_racks_2 = [protocol.load_labware_from_definition(saliva_rack,slot,"saliva rack batch 2: biobank_96well_1000ul") for slot in rack_slots]
            src_tubes_2=[]
            for i in range(0,len(rack_slots)):
                src_tubes_2 += src_racks_2[i].rows()[0]
            trash_2 = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot_2)
            dest_plate_2 = protocol.load_labware(plate_name, plate_slot,"DTT plate batch 2: 96 well full skirt no adaptor")
            multi_pipette_2 = multi_pipette
    #         multi_pipette_2.tip_racks = tips_2
    #         multi_pipette_2.trash_container = trash_2
            # multi_pipette_2.drop_tips() if multi_pipette_2.has_tip else 1



        elif deck_plan == 'sample_to_lamp':
            # for 1st shift
            protocol = initialize(simulate =simulate,**kwarg)
            p20_tip_name = "geb_96_tiprack_10ul"
            p20_tip_slots = ["5","4"]
            right_pip_name = "p20_multi_gen2"
            plate_name = json.loads(lw.geb_96_wellplate)
            sample_plate_slot ="6"
            lamp_plate_slot="3"
            trash_slot="2"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)

            tips = [protocol.load_labware(p20_tip_name, slot) for slot in p20_tip_slots]
            src_plate = protocol.load_labware_from_definition(plate_name, sample_plate_slot)
            src_tubes = src_plate.rows()[0]
            dest_plate = protocol.load_labware_from_definition(plate_name, lamp_plate_slot)
            multi_pipette = protocol.load_instrument(right_pip_name, 'right', tip_racks=tips)
            trash = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot)
            multi_pipette.trash_container = trash
            # multi_pipette.drop_tips() if multi_pipette.has_tip else 1

            p20_tip_name = "geb_96_tiprack_10ul"
            p20_tip_slots_2 = ["10","1"]
            right_pip_name = "p20_multi_gen2"
            plate_name = json.loads(lw.geb_96_wellplate)
            sample_plate_slot_2 ="11"
            lamp_plate_slot_2="8"
            trash_slot_2="7"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)

            tips_2 = [protocol.load_labware(p20_tip_name, slot) for slot in p20_tip_slots_2]
            src_plate_2 = protocol.load_labware_from_definition(plate_name, sample_plate_slot_2)
            src_tubes_2 = src_plate_2.rows()[0]
            dest_plate_2 = protocol.load_labware_from_definition(plate_name, lamp_plate_slot_2)
            trash_2 = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot_2)

        elif deck_plan == 'sample_to_lamp_96well':
            # for 1st shift
            protocol = initialize(simulate =simulate,**kwarg)
            p20_tip_name = "geb_96_tiprack_10ul"
            p20_tip_slots = ["2"]
            right_pip_name = "p20_multi_gen2"
            plate_name = "nest_96_wellplate_100ul_pcr_full_skirt"
            sample_plate_slot ="5"
            lamp_plate_slot="6"
            trash_slot="3"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)

            tips = [protocol.load_labware(p20_tip_name, slot) for slot in p20_tip_slots]
            src_plate = protocol.load_labware(plate_name, sample_plate_slot,"Saliva plate: 96 wellplate full_skirt no adaptor")
            src_tubes = src_plate.rows()[0]
            dest_plate = protocol.load_labware(plate_name, lamp_plate_slot,"LAMP MM plate 1: 96 wellplate full_skirt no adaptor")
            multi_pipette = protocol.load_instrument(right_pip_name, 'right', tip_racks=tips)
            trash = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot)
            multi_pipette.trash_container = trash
            # multi_pipette.drop_tips() if multi_pipette.has_tip else 1

            p20_tip_slots_2 = ["8"]
            right_pip_name = "p20_multi_gen2"
            plate_name = "nest_96_wellplate_100ul_pcr_full_skirt"
            # sample_plate_slot_2 ="11"
            lamp_plate_slot_2="4"
            trash_slot_2="7"
            liquid_trash_rack=json.loads(lw.amsliquidtrash)

            tips_2 = [protocol.load_labware(p20_tip_name, slot) for slot in p20_tip_slots_2]
            # src_plate_2 = protocol.load_labware_from_definition(plate_name, sample_plate_slot_2)
            # src_tubes_2 = src_plate_2.rows()[0]
            dest_plate_2 = protocol.load_labware(plate_name, lamp_plate_slot_2, "LAMP MM plate 2: 96 wellplate full_skirt no adaptor")
            trash_2 = protocol.load_labware_from_definition(liquid_trash_rack,trash_slot_2)





    def p_dispense(pipette,well,volume,disp=1,disp_bottom=3):
        """ Use pipette to perform multiple dispense
        volume: sample volume for each dispense
        disp: dispense times
        destination well by default is shift well by 1 row each time for disp times.
        E.g. First well is A1, then next is A"""
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
            pipette.dispense(volume, well.bottom(disp_bottom))
            well = _next_row_well(well)

    def p_transfer(pipette,s,d, b = 0,samp_vol= 50,air_vol = 25,mix=0, buffer_vol = 0,dry_run = False,get_time = 0,disp=2,asp_bottom=2,disp_bottom=3,blowout = True,tip_presses = 1,tip_press_increment=0.3):
        """ s: source well  d: destination well b: buffer well.
        dispense: how many times the same to be dispensed
        Transfer from source well: s to destination well"""
            #print ("Transfering saliva samples in rack {} column {}:".format(1,2))
        #set up pipette parameter
        multi_pipette = pipette
        # if multi_pipette.max_volume>100:
        #     multi_pipette.flow_rate.aspirate = 120
        #     multi_pipette.flow_rate.dispense = 120

        #pipette parameters
        asp_vol = (samp_vol*disp)*1.0
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

        multi_pipette.aspirate(asp_vol, s.bottom(asp_bottom))
        print ("Aspirate {:.1f} uL from {}".format(asp_vol,s))
        multi_pipette.air_gap(air_vol)
        _log_time(st,event = 'Aspirate saliva') if get_time else 1
        st = timeit.default_timer() if get_time else 1

        p_dispense(multi_pipette,d,air_vol) if air_vol >0 else 1
        p_dispense(multi_pipette,d,samp_vol,disp=disp,disp_bottom=disp_bottom)
        if blowout:
            multi_pipette.blow_out()
        _log_time(st,event = 'Dispense saliva') if get_time else 1
        st = timeit.default_timer() if get_time else 1

        if mix >0:
            if multi_pipette.max_volume>100:
                multi_pipette.flow_rate.dispense = 40
            multi_pipette.mix(mix,int(total_vol/2))
            multi_pipette.air_gap(air_vol)
            _log_time(st,event = 'Mix saliva dtt') if get_time else 1
            st = timeit.default_timer() if get_time else 1

        stop = timeit.default_timer()
        if dry_run:
            multi_pipette.return_tip()
            st = timeit.default_timer() if get_time else 1
        else:
            multi_pipette.drop_tip(home_after=False)
            multi_pipette.home()
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
