"""Use lamp_setup_app.py to calibrate all labware first
If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server. Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""

protocols_dic = {
1:"Saliva to DTT",
2:"Sample to LAMP",}

def choose_protocol():
    """
    print out currently protocols.
    """
    s="Currently these protocols are available:\n"
    for k in protocols_dic.keys():
        s+="{}: {} \n".format(k,protocols_dic[k])
    s += "Please choose the protocols to run (e.g. 1) \n Press 0 to exit \n"
    to_do = int(input(s))

    if to_do == 1:
        import Saliva_to_dtt as prot
        return prot
    elif to_do ==2:
        import sample_to_lamp_96well as prot
        return prot


prot = choose_protocol()
prot.deck_plan
prot.run()







# print_available_protocols()
