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
        import Saliva_to_dtt as prot
        return prot
    elif to_do ==2:
        import sample_to_lamp_96well as prot
        return prot

def confirm_deckplan(prot):
    prot.deck_plan
    s="Check following deck plan:\n"
    for k in prot.deck_plan.keys():
        v= prot.deck_plan[k]
        if v != None:
            s+="{}: {} \n".format(k,v)
    s += "Please confirm the deck_plan \n Enter 'y' to start the run \n Enter 'e' to exit\n"
    to_run = input(s)
    return to_run


protocols_dic = {
1:"Saliva to DTT",
2:"Sample to LAMP",}

prot = choose_protocol(protocols_dic)

to_run = ""
while to_run !="y":
    to_run = confirm_deckplan(prot)
    if to_run =='y' or 'Y':
        prot.run()
        break
    elif to_run == 'e':
        print ("Exited")
        break


# prot.run()







# print_available_protocols()
