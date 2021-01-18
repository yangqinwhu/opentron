from opentrons import protocol_api
import sys,json,timeit,time,math
# This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
import importlib
sys.path.append("/var/lib/jupyter/notebooks")
sys.path.append("/Users/chunxiao/Dropbox/python/aptitude_project/opentron")

def _number_to_list(n,p):
    t=math.ceil(n/p)
    l=[]
    for i in range(t):
        if i ==t-1:
            l.append(n-p*(t-1))
        else:
            l.append(p)
    return l


class RobotClass:
    def __init__(self,simulate =True,**kwarg):
        self.status=RunLog()
        self.load_deck(simulate =simulate,**kwarg)

    def robot_initialize(self,simulate =False,**kwarg):
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
        # global protocol,lw
        self.lw=lw
        if simulate:
            import opentrons.simulate
            self.protocol = opentrons.simulate.get_protocol_api('2.1')
        else:
            import opentrons.execute # This returns the same kind of object - a ProtocolContext - that is passed into your protocol’s run function when you upload your protocol in the Opentrons App
            self.protocol = opentrons.execute.get_protocol_api('2.7')
        self.protocol.home()
        self.status.set_status("Robot status: Initialized")

    def assign_deck(self,tip_name = "opentrons_96_filtertiprack_200ul",
        tip_slots = ["7","8"],pip_name = "p300_multi",pip_location="left",
        trash_slots=[],
        src_name="None",src_slots = ["2"],
        dest_name = 'nest_96_wellplate_100ul_pcr_full_skirt',
        dest_slots =["3","4"],**kwarg):
        self.tip_name= tip_name
        self.tip_slots=tip_slots
        self.pip_name=pip_name
        self.pip_location=pip_location
        self.src_name=src_name
        self.src_slots=src_slots
        self.dest_name=dest_name
        self.dest_slots=dest_slots
        self.trash_slots=trash_slots

    def load_deck(self,**kwarg):
        """Single source, single destination"""
        self.robot_initialize(**kwarg)
        self.assign_deck(**kwarg)
        self.tips = [self.protocol.load_labware(self.tip_name, slot) for slot in self.tip_slots]

        try:
            self.src_plates = [self.protocol.load_labware(self.src_name,slot) for slot in self.src_slots]
        except:
            if self.src_name=="micronic_96_wellplate_1400ul" or self.src_name=="None" :
                self.src_name = json.loads(self.lw.micronic_96_wellplate_1400ul)
            self.src_plates = [self.protocol.load_labware_from_definition(self.src_name,slot) for slot in self.src_slots]
        self.src_tubes=[]
        for i in range(0,len(self.src_slots)):
            self.src_tubes += self.src_plates[i].rows()[0]

        self.dest_plates = [self.protocol.load_labware(self.dest_name, slot) for slot in self.dest_slots]
        self.dest_tubes=[]
        for i in range(0,len(self.dest_slots)):
            self.dest_tubes += self.dest_plates[i].rows()[0]

        multi_pipette = self.protocol.load_instrument(self.pip_name, self.pip_location, tip_racks=self.tips)
        self.multi_pipette=PipetteClass(multi_pipette,self.status)

        if len(self.trash_slots)>0:
            liquid_trash_rack=json.loads(self.lw.amsliquidtrash)
            self.trash = [self.protocol.load_labware_from_definition(liquid_trash_rack,slot) for slot in self.trash_slots]
            self.multi_pipette.pipette.trash_container=self.trash[0]

class PipetteClass:
    def __init__(self,pipette,status):
        self.pipette=pipette
        self.status=status

    def _log_time(self,start_time,event = 'This step',print_log=1):
        stop = timeit.default_timer()
        run_time = stop - start_time
        unit = "sec" if run_time<60 else "min"
        run_time = run_time/60 if unit == "min" else run_time
        log ='{} takes {:.2} {}'.format(event,run_time,unit)
        self.status.set_status(log)

    def set_p_param(self,**kwarg):
        self.p_param=kwarg

    def p_dispense(self,well,volume,disp=1,disp_bottom=3):
        """ Use pipette to perform multiple dispense
        volume: sample volume for each dispense
        disp: dispense times
        destination well by default is shift well by 1 row each time for disp times.
        """
        def _next_well(w):
            """n_r_w: return the well in the next row. E.g. A1 well to B1 well
            n_c_w: return the well in the next column. E.g. A1 well to A2 well """
            p=w.parent
            w_name = w._display_name.split(' ')[0]
            row =  w_name[0]
            column = w_name[1:].strip()
            new_row = chr(ord(row) + 1) if ord(row)<ord("H") else chr(ord(row))
            n_r_w= p[new_row+column]  #

            new_column=str(int(column) + 1) if int(column)<12 else str(int(column))
            n_c_w=p[row+new_column]
            return n_r_w , n_c_w

        for i in range(0,disp):
            status="current dispensing well is {}".format(well)
            print (status)
            self.pipette.dispense(volume, well.bottom(disp_bottom))
            well = _next_well(well)[1]

    def p_transfer(self,s,d, b = 0,samp_vol= 50,air_vol = 25,mix=0, buffer_vol = 0,returnTip = False,chgTip=True,get_time = 1,disp=1,asp_bottom=2,disp_bottom=3,blowout = False,tip_presses = 1,tip_press_increment=0.3,reverse_vol=0,reverse_pip=0,simulate=False,**kwarg):
        """ s: source well  d: destination well b: buffer well.
        dispense: how many times the same to be dispensed
        Transfer from source well: s to destination well"""
        #set up pipette parameter

        #pipette parameters
        asp_vol = (samp_vol*disp)*1.0
        if reverse_pip:
            asp_vol+=reverse_vol
        total_vol = asp_vol+air_vol+buffer_vol
        self.asp_vol=total_vol

        start = timeit.default_timer()
        st = timeit.default_timer() if get_time else 1
        if simulate:
            try:
                self.pipette.pick_up_tip(presses=tip_presses, increment=tip_press_increment)
                self._log_time(st,event = 'Pick up tip') if get_time else 1
            except:
                pass
        else:
            if self.pipette.has_tip:
                pass
            else:
                self.pipette.pick_up_tip(presses=tip_presses, increment=tip_press_increment)
                self._log_time(st,event = 'Pick up tip') if get_time else 1
        st = timeit.default_timer() if get_time else st

        if buffer_vol !=0:
            self.pipette.aspirate(buffer_vol, location = b.bottom(2))
            self.pipette.air_gap(air_vol)
            total_vol +=air_vol
            self._log_time(st,event = 'Aspirate DTT buffer') if get_time else 1
            st = timeit.default_timer() if get_time else 1

        self.pipette.aspirate(asp_vol, s.bottom(asp_bottom))
        status = "Aspirate {:.1f} uL from {}".format(asp_vol,s)
        print (status)
        self.pipette.air_gap(air_vol)
        self._log_time(st,event = 'Aspirate saliva') if get_time else 1
        st = timeit.default_timer() if get_time else 1

        self.p_dispense(d,air_vol) if air_vol >0 else 1
        self.p_dispense(d,samp_vol,disp=disp,disp_bottom=disp_bottom)
        status = "Dispense {:.1f} uL from {}".format(samp_vol,s)
        print (status)
        if blowout:
            self.pipette.blow_out()
        self._log_time(st,event = 'Dispense saliva') if get_time else 1
        st = timeit.default_timer() if get_time else 1

        if mix >0:
            if self.pipette.max_volume>100:
                self.pipette.flow_rate.dispense = 40
            self.pipette.mix(mix,int(total_vol/2))
            self.pipette.air_gap(air_vol)
            self._log_time(st,event = 'Mix saliva dtt') if get_time else 1
            st = timeit.default_timer() if get_time else 1

        stop = timeit.default_timer()
        if chgTip:
            if returnTip:
                self.pipette.return_tip()
                st = timeit.default_timer() if get_time else st
            else:
                self.pipette.drop_tip(home_after=False,)
                self.pipette.home()
                print ("Tip changed")
                self._log_time(st,event = 'Drop tip') if get_time else 1
                st = timeit.default_timer() if get_time else st


class RunLog:
    def __init__(self):
        self.status=""

    def set_status(self,s):
        self.status=s
        print (s)

class RunRobot(RobotClass):
    def __init__(self,**kwarg):
        self.robot=RobotClass(**kwarg)
        self.mp=self.robot.multi_pipette
        self.init_protocol(**kwarg)

    def init_protocol(self,**kwarg):
        self.init_plate(**kwarg)
        self.init_well(**kwarg)
        self.init_pipette(**kwarg)

    def init_plate(self,src_plate=1,dest_plate=1,**kwarg):
        self.current_srcplate=src_plate-1
        self.next_srcplate=self.current_srcplate+1
        self.current_destplate=dest_plate-1
        self.next_destplate=self.current_destplate+1

    def init_well(self,start_tube=1,start_dest=1,**kwarg):
        self.current_srctube=start_tube-1
        self.current_desttube=start_dest-1

    def init_pipette(self,start_tip=1,**kwarg):
        self.current_tip=start_tip-1
        self.mp.pipette.reset_tipracks()
        self.mp.pipette.starting_tip=self.robot.tips[0].rows()[0][start_tip-1]

    def _set_transfer(self,**kwarg):
        self.sts=self.robot.src_plates[self.current_srcplate].rows()[0][self.current_srctube:self.current_srctube+1]
        self.dts=self.robot.dest_plates[self.current_destplate].rows()[0][self.current_desttube:self.current_desttube+1]

    def _update_aliquot(self,disp=1,**kwarg):
        self.next_srctube=self.current_srctube+1
        self.next_desttube=self.current_desttube+disp

    def _set_replicate(self,replicates=1,**kwarg):
        self.sts=self.robot.src_plates[self.current_srcplate].rows()[0][self.current_srctube:self.current_srctube+1]
        self.dts=self.robot.dest_plates[self.current_destplate].rows()[0][self.current_desttube:self.current_desttube+replicates]

    def _update_replicate(self,replicates=1,**kwarg):
        self.next_srctube=self.current_srctube+1
        self.next_desttube=self.current_desttube+replicates

    def _update_one(self,c,n):
        return n,n+1

    def _src_empty(self,trans_v,src_vol=150,**kwarg):
        self.src_remaining_vol-=trans_v
        print (f"{self.src_remaining_vol}ul remaining in {self.current_srctube}")
        if self.src_remaining_vol>0:
            return 0
        else:
            return 1

    def _aliquot(self,target_columns=1,**kwarg):
        disps=_number_to_list(target_columns,kwarg["disp"])
        kwarg.update({"reverse_pip":1})
        h=0
        for disp in disps:
            h+=1
            kwarg.pop("disp")
            kwarg.update({"chgTip":0})
            kwarg.update({"disp":disp})
            trans_v=(kwarg["disp"]*kwarg["samp_vol"])+(kwarg["reverse_pip"]*kwarg["reverse_vol"])
            if self._src_empty(trans_v,**kwarg):
                self.current_srctube,self.next_srctube=self._update_one(self.current_srctube,self.next_srctube)
                self.src_remaining_vol=self.src_vol-trans_v
            self._set_transfer(disp=disp)
            for i, (s, d) in enumerate(zip(self.sts,self.dts)):
                if i==(len(self.dts)-1) and h==(len(disps)):
                    kwarg.update({"chgTip":1})
                self.mp.p_transfer(s,d,**kwarg)
                kwarg.update({"reverse_pip":0})
            self._update_aliquot(disp=disp)
            self.current_desttube,self.next_desttube=self._update_one(self.current_desttube,self.next_desttube)

    def _aliquot_lamp_one_plate(self,**kwarg):
        self._aliquot(**kwarg)
        self.current_desttube=11
        s=self.robot.src_plates[self.current_srcplate].rows()[0][11]
        d=self.robot.dest_plates[self.current_destplate].rows()[0][self.current_desttube]
        kwarg.update({"disp":1})
        kwarg.update({"chgTip":1})
        self.mp.p_transfer(s,d,**kwarg)

    def aliquot_dtt_p100(self,target_plates=1,**kwarg):
        self.src_vol=kwarg["src_vol"]
        self.src_remaining_vol=self.src_vol
        for p in range(0,target_plates):
            self._aliquot(**kwarg)
            self.current_destplate,self.next_destplate=self._update_one(self.current_destplate,self.next_destplate)
            self.current_desttube=kwarg["start_dest"]-1

    def aliquot_lamp_p100(self,target_plates=1,**kwarg):
        self.src_vol=kwarg["src_vol"]
        self.src_remaining_vol=self.src_vol
        for p in range(0,target_plates):
            self._aliquot_lamp_one_plate(**kwarg)
            self.current_destplate,self.next_destplate=self._update_one(self.current_destplate,self.next_destplate)
            self.current_desttube=kwarg["start_dest"]-1

    def sample_to_lamp(self,target_columns=1,rp4=0,**kwarg):
        for i in range(0,target_columns):
            s=self.robot.src_plates[self.current_srcplate].rows()[0][self.current_srctube]
            d=self.robot.dest_plates[self.current_destplate].rows()[0][self.current_desttube]
            self.mp.p_transfer(s,d,**kwarg)
            if rp4:
                d=self.robot.dest_plates[self.current_destplate+1].rows()[0][self.current_desttube]
                self.mp.p_transfer(s,d,**kwarg)
            self.next_desttube=self.current_desttube+1
            self.current_desttube,self.next_desttube=self._update_one(self.current_desttube,self.next_desttube)





#
# r=RunRobot()
# p=r.robot.multi_pipette.pipette
# p
#
# trash.wells()
# p.pick_up_tip()
# drop_tip_location=p.trash_container.wells()[0].bottom(50)
# p.move_to(drop_tip_location)
