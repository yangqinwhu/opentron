import os,time
from pathlib import Path
from threading import Thread
import tkinter as tk
# import shutil
import json,requests,copy

BOTTON_FONT=16
LABEL_FONT=8
server_ip = "127.0.0.1"
# server_ip = "192.168.1.46"
DEV=True if server_ip == "127.0.0.1" else False


PORT = 8000

saliva_to_dtt={
    "protocol":{
    "file":"saliva_to_dtt",
    "run":"p200_aliqot"
    },
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":False,
        "deck":"saliva_to_dtt_micronic_96_wellplate_1400ul",
    },
    "sample_info":{
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
        "samp_vol":50,
        "reverse_vol":0,
        "air_vol": 25,
        "disp":1,
        "asp_bottom":20,
        "disp_bottom":2,
        'mix':0,
        "get_time":1,
        'returnTip':False,
        "aspirate_rate": 120,
        "dispense_rate": 120,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    },
    "deck_param":{"tip_name":"opentrons_96_filtertiprack_200ul",
        "tip_slots":["7","8"],
        "pip_name":"p300_multi",
        "pip_location":"left",
        "trash_slots":[],
        "src_name":"micronic_96_wellplate_1400ul",
        "src_slots": ["1"],
        "dest_name": 'nest_96_wellplate_100ul_pcr_full_skirt',
        "dest_slots":["2","3","4","5","6"],
    }
}

sample_to_lamp_96well={
    "protocol":{
    "file":"p200_aliquot",
    "run":"sampleToLamp"
    },
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":False,
        "deck":"sample_to_lamp_96well_n7_rp4",
    },
    "sample_info":{
        "target_columns":12,
        "start_tube":1,
        "start_dest":1,
        "start_tip":1,
        "replicates":2,
        "repl_chg_tip":0,
    },
    "transfer_param":{
        "samp_vol":5,
        "reverse_vol":5,
        "rp4":0,
        "air_vol": 0,
        "asp_bottom":1,
        "disp_bottom":0.5,
        'mix':0,
        'returnTip':False,
        "aspirate_rate": 5,
        "dispense_rate": 5,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    },
    "deck_param":{"tip_name":"opentrons_96_filtertiprack_20ul",
        "tip_slots":["4","7","8"],
        "pip_name":"p20_multi_gen2",
        "pip_location":"right",
        "trash_slots":[],
        "src_name":'nest_96_wellplate_100ul_pcr_full_skirt',
        "src_slots": ["1"],
        "dest_name": 'nest_96_wellplate_100ul_pcr_full_skirt',
        "dest_slots":["2","3"],
    }
}

aliquot_p20_96well={
    "protocol":{
    "file":"p200_aliquot",
    "run":"aliquotDTTP20"
    },
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":True,
        "deck":"sample_to_lamp_96well_n7_rp4",
    },
    "sample_info":{
        "target_columns":12,
        "target_plates":1,
        "start_tube":1,
        "start_dest":1,
        "start_tip":1,
        "replicates":2,
        "repl_chg_tip":0,
    },
    "transfer_param":{
        "samp_vol":10,
        "reverse_vol":5,
        "src_vol":150,
        "rp4":0,
        "air_vol": 0,
        "asp_bottom":0,
        "disp_bottom":-2,
        'mix':0,
        'returnTip':False,
        "aspirate_rate": 2.5,
        "dispense_rate": 2.5,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    },
    "deck_param":{"tip_name":"opentrons_96_filtertiprack_20ul",
        "tip_slots":["10","11"],
        "pip_name":"p20_multi_gen2",
        "pip_location":"right",
        "trash_slot":["9"],
        "src_name":'nest_96_wellplate_100ul_pcr_full_skirt',
        "src_slots": ["7"],
        "dest_name": 'nest_96_wellplate_100ul_pcr_full_skirt',
        "dest_slots":["2","4","5","6"],
    }
}

aliquot_p100_96well={
    "protocol":{
    "file":"p200_aliquot",
    "run":"p200_aliqot"
    },
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":False,
        "deck":"saliva_to_dtt_micronic_96_wellplate_1400ul",
    },
    "sample_info":{
        "target_columns":2,
        "target_plates":1,
        "start_tube":1,
        "start_dest":1,
        "src_plate":1,
        "dest_plate":1,
        "start_tip":1,
        "replicates":2,
    },
    "transfer_param":{
        "samp_vol":10,
        "reverse_vol":10,
        "src_vol":150,
        "air_vol": 0,
        "disp":6,
        "asp_bottom":-3,
        "disp_bottom":-11,
        'mix':0,
        'returnTip':False,
        "aspirate_rate": 60,
        "dispense_rate": 20,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    },
    "deck_param":{"tip_name":"opentrons_96_filtertiprack_200ul",
        "tip_slots":["7","8"],
        "pip_name":"p300_multi",
        "pip_location":"left",
        "trash_slots":[],
        "src_name":"micronic_96_wellplate_1400ul",
        "src_slots": ["1"],
        "dest_name": 'nest_96_wellplate_100ul_pcr_full_skirt',
        "dest_slots":["2","3","4","5","6"],
    }
}

aliquot_p20_dtt_tm={
    "protocol":{
    "file":"p200_aliquot",
    "run":"aliquotDTTP20"
    },
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":False,
        "tm":"src",
        "tm_temp":4,
    },
    "sample_info":{
        "target_columns":12,
        "target_plates":1,
        "start_tube":1,
        "start_dest":1,
        "start_tip":1,
        "repl_chg_tip":0,
    },
    "transfer_param":{
        "samp_vol":10,
        "reverse_vol":5,
        "src_vol":300,
        "rp4":0,
        "asp_bottom":12,
        "disp_bottom":0,
        "disp":1,
        'returnTip':False,
        "aspirate_rate": 7.6,
        "dispense_rate": 7.6,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    },
    "deck_param":{"tip_name":"opentrons_96_filtertiprack_20ul",
        "tip_slots":["4","7"],
        "pip_name":"p20_multi_gen2",
        "pip_location":"right",
        "trash_slots":[],
        "src_name":'nest_96_wellplate_100ul_pcr_full_skirt',
        "src_slots": ["11"],
        "dest_name": 'nest_96_wellplate_100ul_pcr_full_skirt',
        "dest_slots":["2","3","5","6","8","9"],
        "tm_name":'nest_96_wellplate_2ml_deep',
        "temp_module_slot": ["10"],
    }
}

aliquot_p20_lamp_tm={
    "protocol":{
    "file":"p200_aliquot",
    "run":"aliquotLampP20"
    },
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":False,
        "tm":"src",
        "tm_temp":4,
    },
    "sample_info":{
        "target_columns":11,
        "target_plates":1,
        "n7_wells":"3,5",
        "rp4_wells":"7,9",
        "start_dest":1,
        "start_tip":1,
        "repl_chg_tip":0,
    },
    "transfer_param":{
        "samp_vol":15,
        "reverse_vol":3,
        "src_vol":350,
        "asp_bottom":12,
        "disp_bottom":0.5,
        "disp":1,
        'returnTip':False,
        "aspirate_rate": 5,
        "dispense_rate": 5,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    },
    "deck_param":{"tip_name":"opentrons_96_filtertiprack_20ul",
        "tip_slots":["4","7"],
        "pip_name":"p20_multi_gen2",
        "pip_location":"right",
        "trash_slots":[],
        "src_name":'nest_96_wellplate_100ul_pcr_full_skirt',
        "src_slots": ["11"],
        "dest_name": 'nest_96_wellplate_100ul_pcr_full_skirt',
        "dest_slots":["2","3","5","6","8","9"],
        "tm_name":'nest_96_wellplate_2ml_deep',
        "temp_module_slot": ["10"],
    }
}

class OpentronApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Opentron app')
        self.geometry('800x480+0+-30')#-30
        # self.resizable(0,0)

        container = tk.Frame(self)

        container.pack(side='top',fill='both',expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for F in (HomePage,DTTPage,LAMPPage,AliquotDTTPage,AliquotLAMPPage,AliquotLAMPNoNBCPage):
             self.pages[F.__name__] = F(parent=container,master=self)
             self.pages[F.__name__].grid(row=0, column=0, sticky="nsew")

        self.showPage('HomePage')

    def showPage(self,page):
        self.pages[page].showPage()

    def on_closing(self):
        print('exit')
        self.destroy()

class HomePage(tk.Frame):
    def __init__(self,parent,master):
        super().__init__(parent)
        self.master = master
        self.create_frames()
        self.create_widgets()

    def create_frames(self):
        self.BottomFrame = tk.Frame(self)
        self.BottomFrame.place(x=0,y=380,height=100,width=800)
        self.TopFrame = tk.Frame(self)
        self.TopFrame.place(x=0,y=0,height=380,width=800)

    def create_widgets(self):
        self.create_bottom()
        self.create_top()

    def create_bottom(self):
        master=self.BottomFrame
        tk.Button(master,text='Exit',font=('Arial',30),command=self.master.on_closing).place(
            x=340,y=0,height=50,width=120)
        self.back_btn=tk.Button(master,text='<<',font=('Arial',30),state=tk.DISABLED,command=self.get_page_1)
        self.back_btn.place(
            x=280,y=0,height=50,width=50)
        self.fwd_btn=tk.Button(master,text='>>',font=('Arial',30),command=self.get_page_2)
        self.fwd_btn.place(
            x=470,y=0,height=50,width=50)

    def create_top(self,page=1):
        master=self.TopFrame
        master.destroy()
        self.TopFrame=tk.Frame(self)
        self.TopFrame.place(x=0,y=0,height=380,width=800)
        master=self.TopFrame
        if page==1:
            self.page_1=tk.Button(master,text='Saliva to DTT\n 96 well\n P300',font=('Arial',30),state=tk.DISABLED,command=lambda:self.master.showPage('DTTPage')).place(
                x=20,y=40,height=150,width=360)
            self.page_2=tk.Button(master,text='Sample to LAMP \n P20',font=('Arial',30),command=lambda:self.master.showPage('LAMPPage')).place(
                x=420,y=40,height=150,width=360)
            self.page_3=tk.Button(master,text='Aliquot DTT \n P20 Temp Deck',font=('Arial',30),command=lambda:self.master.showPage('AliquotDTTPage')).place(
                x=20,y=210,height=150,width=360)
            self.page_4=tk.Button(master,text='Aliquot LAMP \n P20 Temp Deck',font=('Arial',30),command=lambda:self.master.showPage('AliquotLAMPPage')).place(
                x=420,y=210,height=150,width=360)
        elif page==2:
            self.page_1=tk.Button(master,text='Aliquot LAMP no NBC \n P20 Temp Deck',font=('Arial',20),command=lambda:self.master.showPage('AliquotLAMPNoNBCPage')).place(
                x=20,y=40,height=150,width=360)


    def get_page_1(self):
        self.create_top(page=1)
        self.back_btn.config(state=tk.DISABLED)
        self.fwd_btn.config(state=tk.NORMAL)

    def get_page_2(self):
        self.create_top(page=2)
        self.back_btn.config(state=tk.NORMAL)
        self.fwd_btn.config(state=tk.DISABLED)




    def showPage(self):
        self.tkraise()
        self.focus_set()

class RunPage(tk.Frame):
    """Parameters in the essential will be displayed seperately.
    Other parameters will only display in the developer page"""

    basic=["start_tip","start_tube"]
    def __init__(self,parent,master):
        super().__init__(parent)
        self.master = master
        self.parent=parent
        self.robot_url=f"http://{server_ip}:{PORT}"
        self.forms=["robot_param","sample_info","transfer_param"]
        self.initialized=0
        self.create_frames()
        self.create_widgets()
        self.config_side_buttons()

    def create_frames(self):
        self.SideFrame = tk.Frame(self)  # Frame 1 is the side button
        self.SideFrame.place(x=0,y=0,height=400,width=150)
        self.BottomFrame = tk.Frame(self)
        self.BottomFrame.place(x=150,y=350,height=50,width=450) # Frame 2 is the bottom button
        self.FormFrame = tk.Frame(self) # param is the parameter region
        self.FormFrame.place(x=150,y=0,height=350,width=450)
        self.DeckFrame=tk.Frame(self,relief=tk.RIDGE)
        self.frm_txt = tk.Text(self)
        self.frm_txt.place(
            x=600,y=20,height=360,width=200)
        self.StatusFrame=tk.Frame(self)
        self.StatusFrame.place(x=0,y=400,height=60,width=150)

    def create_widgets(self):
        ### botton control area
        self.create_side_buttons()
        self.create_bottom_buttons()
        self.create_status_view()
        ### Input area
        self.create_forms(self.defaultParams,basic=True)
        self.create_deck_btn()


    def _create_form(self,dic,master):
        for idx, text in enumerate(dic.keys()):
            label = tk.Label(master, text=text,width=10,font=('Arial',LABEL_FONT))
            entry = tk.Entry(master, textvariable=dic[text],width=10,font=('Arial',LABEL_FONT))
            label.grid(row=idx+self.form_row, column=self.form_column,sticky="e")
            entry.grid(row=idx+self.form_row, column=self.form_column+1,sticky="e")
        # self.form_row+=len(dic.keys())

    def create_forms(self,dic,basic=True):
        """Parse input dic and create forms for multiple parameters"""
        master=self.FormFrame
        master.destroy()
        self.FormFrame = tk.Frame(self)
        if basic:
            self.FormFrame.place(x=150,y=0,height=150,width=450)
        else:
            self.FormFrame.place(x=150,y=0,height=350,width=450)
        master=self.FormFrame
        self.form_row=0
        self.form_column=0
        tk.Label(master, text="Run Config",font=('Arial',LABEL_FONT+2)).grid(
            row=self.form_row, column=self.form_column, columnspan=1,sticky="e")
        entry = tk.Entry(master, width=40,font=('Arial',LABEL_FONT))
        entry.grid(
            row=self.form_row, column=self.form_column+1,columnspan=3, sticky="w")
        entry.insert(0,self.config)
        self.form_row+=1
        self._create_forms(dic,master,basic=basic)

    def _create_forms(self,dic,master,basic=True):
        self.run_params = {}
        for form in self.forms:
            self.run_params[form]={}
            for k,i in self.defaultParams[form].items():
                p = self.basic if basic else self.defaultParams[form]
                if k in p:
                    if isinstance(i,int): var = tk.IntVar()
                    elif isinstance(i,float): var = tk.DoubleVar()
                    else: var = tk.StringVar()
                    var.set(i)
                    self.run_params[form][k]=var
            if len(self.run_params[form])>0:
                tk.Label(master,text=form,font=('Arial',LABEL_FONT+2)).grid(
                    row=self.form_row, column=self.form_column,columnspan=2, sticky="ew")
                self.form_row+=1
                self._create_form(self.run_params[form],master)
                self.form_row=1
                self.form_column+=2

    def create_bottom_buttons(self):
        master=self.BottomFrame
        # tk.Button(master, text ="Apply", font=('Arial',BOTTON_FONT),command=self.confirm_run_params).grid(
        #     row=0, column=1, columnspan=2,sticky="e")
        tk.Button(master, text ="Save", font=('Arial',BOTTON_FONT),command=self.save_run_params).grid(
            row=0, column=3,  columnspan=2,sticky="w")
        self.adv_btn=tk.Button(master, text =">> Adv", font=('Arial',BOTTON_FONT),command=self.get_all_forms)
        self.adv_btn.grid(row=0, column=5,  columnspan=1,sticky="w")
        self.basic_btn=tk.Button(master, text ="  <<", font=('Arial',BOTTON_FONT),state=tk.DISABLED,command=self.get_basic_forms)
        self.basic_btn.grid(row=0, column=0,  columnspan=1,sticky="w")

    def create_side_buttons(self):
        master = self.SideFrame
        self.qrun_btn=tk.Button(master,text='Quick Run',font=('Arial',BOTTON_FONT),command=self.quick_run)
        self.qrun_btn.grid(
            row=0, column=0,rowspan=2, sticky="we")
        self.home_btn=tk.Button(master,text='Home',font=('Arial',BOTTON_FONT),command=self.init_robot)
        self.home_btn.grid(
            row=3, column=0, rowspan=2,sticky="we")
        self.run_btn=tk.Button(master,text='Run',font=('Arial',BOTTON_FONT),command=self.run_robot)
        self.run_btn.grid(
            row=6, column=0, rowspan=2,sticky="we")
        self.pause_btn=tk.Button(master,text='Pause',font=('Arial',BOTTON_FONT),state=tk.DISABLED,command=self.pause_robot)
        self.pause_btn.grid(
            row=9, column=0, rowspan=2,sticky="we")
        self.resume_btn=tk.Button(master,text='Resume',font=('Arial',BOTTON_FONT),state=tk.DISABLED,command=self.resume_robot)
        self.resume_btn.grid(
            row=12, column=0, rowspan=2,sticky="we")
        self.back_btn=tk.Button(master,text='Back',font=('Arial',BOTTON_FONT),command=self.goToHome)
        self.back_btn.grid(
            row=15, column=0,rowspan=2, sticky="we")
        if "tm" in self.defaultParams["robot_param"].keys():
            if len(self.defaultParams["robot_param"]["tm"])>0:
                self.tm_temp_btn=tk.Button(master,text='TM ON',font=('Arial',BOTTON_FONT),state=tk.DISABLED,command=self.set_temp)
                self.tm_temp_btn.grid(
                    row=18, column=0,rowspan=2, sticky="we")
                self.tm_deactivate_btn=tk.Button(master,text='TM OFF',font=('Arial',BOTTON_FONT),state=tk.DISABLED,command=self.deactivate_tm)
                self.tm_deactivate_btn.grid(
                    row=21, column=0,rowspan=2, sticky="we")

        for i in range(7):
            tk.Label(master, text="",font=('Arial',LABEL_FONT-10)).grid(row=(i*3+2), column=0,sticky="e")

    def create_status_view(self):
        master=self.StatusFrame
        self.robot_status = tk.StringVar()
        self.robot_status.set("Unknown")
        tk.Label(master, textvariable=self.robot_status,font=('Arial',BOTTON_FONT-1),relief="sunken").grid(
            row=0, column=0, columnspan=1,sticky="ewsn")

    def update_status_view(self):
        self.get_status=True
        if not hasattr(self,"r_status_thread"):
            self.r_status_thread=Thread(target=self.get_run_status)
            self.r_status_thread.start()
        else:
            if not self.r_status_thread.is_alive():
                self.r_status_thread=Thread(target=self.get_run_status)
                self.r_status_thread.start()

    def _get_deck(self):
        deck={}
        for s in range(1,13):
            for i,k in self.defaultParams["deck_param"].items():
                if str(s) in k and isinstance(k,list):
                    deck[s]=i
                    break
                else:
                    deck[s]= "None"
        return deck

    def create_deck_btn(self):
        self.DeckFrame.grid_rowconfigure(4, weight=10)
        self.DeckFrame.grid_columnconfigure(3, weight=10)
        self.DeckFrame.place(x=150,y=150,height=200,width=450)
        master = self.DeckFrame
        s=1
        deck=self._get_deck()
        for r in [3,2,1,0]:
            for c in [0,1,2]:
                tk.Label(master, text =f"{s}\n {deck[s]}", font=('Arial'),relief="solid").grid(row=r, column=c,columnspan=1,sticky="ewns")
                s+=1

    def config_side_buttons(self):
        if self.initialized:
            self.run_btn.config(state=tk.NORMAL)
            if hasattr(self,"tm_temp_btn"):
                self.tm_temp_btn.config(state=tk.NORMAL)
                self.tm_deactivate_btn.config(state=tk.NORMAL)
        else:
            self.run_btn.config(state=tk.DISABLED)
            if hasattr(self,"tm_temp_btn"):
                self.tm_temp_btn.config(state=tk.DISABLED)
                self.tm_deactivate_btn.config(state=tk.DISABLED)
        if self.robot_status.get()=="BUSY":
            self.run_btn.config(state=tk.DISABLED)
            self.qrun_btn.config(state=tk.DISABLED)
            self.home_btn.config(state=tk.DISABLED)
            self.back_btn.config(state=tk.DISABLED)
        elif self.robot_status.get()=="IDLE":
            if self.initialized:
                self.run_btn.config(state=tk.NORMAL)
        elif self.robot_status.get()=="Robot Error":
            self.initialized=0
            self.run_btn.config(state=tk.DISABLED)
        if self.robot_status.get()!="BUSY":
            self.qrun_btn.config(state=tk.NORMAL)
            self.home_btn.config(state=tk.NORMAL)
            self.back_btn.config(state=tk.NORMAL)



    def showPage(self):
        self.tkraise()
        self.focus_set()

    def goToHome(self):
        self.master.showPage('HomePage')
        self.initialized=0
        self.config_side_buttons()
        self.get_status=False
        self.robot_status.set("Unknown")

    def init_robot(self):
        self.update_status_view()
        url=self.robot_url+'/init_robot'
        res=requests.get(url,json=self.get_run_params())
        self.frm_txt.insert(tk.END,"\n"+"*"*10+"\n")
        self.frm_txt.insert(tk.END,res.text)
        self.initialized=1
        self.config_side_buttons()

    def run_robot(self):
        if self.initialized:
            url=self.robot_url+'/run_robot'
            # js=json.dumps(self.get_run_params())
            res=requests.get(url,json=self.get_run_params())
            self.frm_txt.insert(tk.END,"\n"+"*"*10+"\n")
            self.frm_txt.insert(tk.END,res.text)
            self.frm_txt.see(tk.END)
        else:
            self.frm_txt.insert(tk.END,"\n"+"*"*10+"\n")
            self.frm_txt.insert(tk.END,"Initialize the robot first")
            self.frm_txt.see(tk.END)

    def quick_run(self):
        self.init_robot()
        self.run_robot()

    def pause_robot(self):
        url=self.robot_url+'/pause'
        res=requests.get(url,json=self.get_run_params())

    def resume_robot(self):
        url=self.robot_url+'/resume'
        res=requests.get(url,json=self.get_run_params())

    def set_temp(self):
        url=self.robot_url+'/run_robot'
        set_temp={
            "protocol":{
            "file":"p200_aliquot",
            "run":"set_temp",
            },
            "robot_status":{
                "initialized":0,
                "to_run":1,
            },
        }
        res=requests.get(url,json=set_temp)

    def deactivate_tm(self):
        url=self.robot_url+'/run_robot'
        set_temp={
            "protocol":{
            "file":"p200_aliquot",
            "run":"deactivate_tm",
            },
            "robot_status":{
                "initialized":0,
                "to_run":1,
            },
        }
        res=requests.get(url,json=set_temp)

    def get_run_status(self):
        while self.get_status:
            sleep_time=2 if DEV else 5
            time.sleep(sleep_time)
            try:
                url=self.robot_url+'/get_status'
                res=requests.get(url,json={})
                # self.frm_txt.insert(tk.END,f"{res.text}\n")
                # self.frm_txt.see(tk.END)
                self.robot_status.set(res.text)
            except Exception as e:
                st="No Server"
                # self.frm_txt.insert(tk.END,f"{st}\n")
                # self.frm_txt.see(tk.END)
                self.robot_status.set(st)
                self.initialized=0
            self.config_side_buttons()


    def get_run_params(self):
        para = {}
        for f in self.defaultParams.keys():
            para[f]={}
            if isinstance(self.defaultParams[f],dict):
                for k,i in self.defaultParams[f].items():
                    try:
                        para[f][k]=self.run_params[f][k].get()
                    except:
                        para[f][k] = self.defaultParams[f][k]
            else:
                para[f]=self.defaultParams[f]
        return para

    def confirm_run_params(self):
        js=json.dumps(self.get_run_params(),indent=4)
        self.frm_txt.insert(tk.END,"\n"+"*"*40+"\n")
        self.frm_txt.insert(tk.END,js)
        self.frm_txt.see(tk.END)
        self.para_confirmed=1

    def save_run_params(self):
        para=self.get_run_params()
        self.defaultParams=copy.deepcopy(para)
        pp=Path(__file__).parent / "defaultRunParam"/ f"{self.config}.configure"
        with open(pp, 'wt') as f:
            json.dump(para, f, indent=2)
        f.close()

    def get_all_forms(self):
        self.create_forms(self.defaultParams,basic=False)
        self.basic_btn.config(state=tk.NORMAL)
        self.adv_btn.config(state=tk.DISABLED)
        self.DeckFrame.destroy()
        self.DeckFrame=tk.Frame(self)

    def get_basic_forms(self):
        self.create_forms(self.defaultParams,basic=True)
        self.basic_btn.config(state=tk.DISABLED)
        self.adv_btn.config(state=tk.NORMAL)
        self.create_deck_btn()


class DTTPage(RunPage):
    config="saliva_to_dtt"
    pp=Path(__file__).parent / "defaultRunParam"/ f"{config}.configure"
    if os.path.exists(pp):
        defaultParams = json.load(open(pp, 'rt'))
    else:
        defaultParams=json.loads(json.dumps(saliva_to_dtt))
    defaultParams["protocol"]["run"]=config.split("_")[0]
    pass

class LAMPPage(RunPage):
    config="sampleToLamp_96well"
    pp=Path(__file__).parent / "defaultRunParam"/ f"{config}.configure"
    basic=["target_columns","start_tip"]
    if os.path.exists(pp):
        defaultParams = json.load(open(pp, 'rt'))
    else:
        defaultParams=json.loads(json.dumps(sample_to_lamp_96well))
    defaultParams["protocol"]["run"]=config.split("_")[0]
    pass

class AliquotDTTPage(RunPage):
    # config="aliquotDTT_p100"
    config="aliquotDTTP20_tm"
    pp=Path(__file__).parent / "defaultRunParam"/ f"{config}.configure"
    basic=["target_columns","target_plates","start_tip"]
    if os.path.exists(pp):
        defaultParams = json.load(open(pp, 'rt'))
    else:
        defaultParams=json.loads(json.dumps(aliquot_p20_dtt_tm))
    defaultParams["protocol"]["run"]=config.split("_")[0]

class AliquotLAMPPage(RunPage):
    config="aliquotLampP20_tm"
    basic=["target_columns","start_tip"]
    pp=Path(__file__).parent / "defaultRunParam"/ f"{config}.configure"
    if os.path.exists(pp):
        defaultParams = json.load(open(pp, 'rt'))
    else:
        # defaultParams=json.loads(json.dumps(aliquot_p100_96well))
        defaultParams=json.loads(json.dumps(aliquot_p20_lamp_tm))
    defaultParams["protocol"]["run"]=config.split("_")[0]

class AliquotLAMPNoNBCPage(RunPage):
    config="aliquotLampP20noNBC_tm"
    basic=["target_columns","start_tip"]
    pp=Path(__file__).parent / "defaultRunParam"/ f"{config}.configure"
    if os.path.exists(pp):
        defaultParams = json.load(open(pp, 'rt'))
    else:
        # defaultParams=json.loads(json.dumps(aliquot_p100_96well))
        defaultParams=json.loads(json.dumps(aliquot_p20_lamp_tm))
    defaultParams["protocol"]["run"]=config.split("_")[0]



app = OpentronApp()
app.protocol('WM_DELETE_WINDOW',app.on_closing)
app.mainloop()
