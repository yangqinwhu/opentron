"""Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""



def choose_protocol(protocols_dic):
    """
    print out currently protocols.
    """
    s="Currently these protocols are available:\n"
    for k in protocols_dic.keys():
        s+="{}: {} \n".format(k,protocols_dic[k])
    s += "Please choose the protocols to run (e.g. 1) \n Other inputs will leads to error \n"
    to_do = int(input(s))

    if to_do == 1:
        import ams_protocols.saliva_to_dtt as prot
        return prot
    elif to_do ==2:
        import ams_protocols.sample_to_lamp_96well as prot
        return prot

def confirm_deckplan(deck_plan):
    s="Check the deck plan:\n"
    for k in deck_plan.keys():
        v= deck_plan[k]
        if v != None:
            s+="{}: {} \n".format(k,v)
    s += "Please confirm the deck_plan \n Enter 'y' to start the run \n Enter 'e' to exit\n"
    to_run = input(s)
    return to_run

sample_info={
    "samples":48,
    "sample_per_column":8,
    "replicates":2,
    "total_batch":1,
    "start_batch":1,
}
transfer_param={
    "samp_vol":5,
    "air_vol": 0,
    "disp":1,
    "asp_bottom":0,
    "disp_bottom":0,
    'mix':0,
    "get_time":1,
    'dry_run':False,
    "aspirate_rate": 7.6,
    "dispense_rate": 7.6,
    "tip_press_increment":0.3,
    "tip_presses" : 1,
}

protocols_dic = {
1:"Saliva to DTT",
2:"Sample to LAMP",}


prot = choose_protocol(protocols_dic)

to_run = ""
while to_run !="y":
    deck_plan=prot.initialize_robot()
    to_run = confirm_deckplan(deck_plan)
    if to_run in 'yY':

        prot.run(**sample_info,**transfer_param)
        break
    elif to_run == 'e':
        print ("Exited")
        break


# prot.run()







# print_available_protocols()
