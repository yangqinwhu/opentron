
import os
from pathlib import Path
import tkinter as tk
# import shutil
import json,requests

saliva_to_dtt={
    "protocol":"saliva_to_dtt",
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":True,
        "deck":"saliva_to_dtt_micronic_96_wellplate_1400ul",
    },
    "sample_info":{
        "samples":8,
        "sample_per_column":8,
        "total_batch":1,
        "start_batch":1,
        "start_tube":1,
        "start_tip":1,
        "replicates":1,
    },
    "transfer_param":{
        "samp_vol":50,
        "air_vol": 25,
        "disp":1,
        "asp_bottom":20,
        "disp_bottom":2,
        'mix':0,
        "get_time":1,
        'dry_run':False,
        "aspirate_rate": 120,
        "dispense_rate": 120,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    },
}


sample_to_lamp_96well={
    "protocol":"sample_to_lamp_96well",
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":True,
        "deck":"sample_to_lamp_96well",
    },
    "sample_info":{
        "samples":8,
        "sample_per_column":8,
        "total_batch":1,
        "start_batch":1,
        "start_tube":1,
        "start_tip":1,
        "replicates":2,
    },
    "transfer_param":{
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
    },
}


BOTTON_FONT=12
LABEL_FONT=10

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
        for F in (HomePage,DTTPage,LAMPPage):
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
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self,text='Saliva to DTT\n 96 well\n P300',font=('Arial',40),command=lambda:self.master.showPage('DTTPage')).place(
            x=20,y=40,height=150,width=360)
        tk.Button(self,text='Sample to LAMP \n P20',font=('Arial',40),command=lambda:self.master.showPage('LAMPPage')).place(
            x=420,y=40,height=150,width=360)
        tk.Button(self,text='Exit',font=('Arial',60),command=self.master.on_closing).place(
            x=20,y=210,height=150,width=360)

    def showPage(self):
        self.tkraise()
        self.focus_set()

class RunPage(tk.Frame):
    """Parameters in the essential will be displayed seperately.
    Other parameters will only display in the developer page"""



    def __init__(self,parent,master):
        super().__init__(parent)
        self.master = master
        self.parent=parent
        self.robot_url="http://192.168.1.46:8000"
        # self.robot_url="http://127.0.0.1:8000"
        self.forms=["robot_param","sample_info","transfer_param"]
        self.essential = ["simulate","samples","start_tip","replicates"]
        self.form_row=0
        self.form_column=1
        self.para_confirmed=0
        self.create_widgets()

    def create_widgets(self):
        ### botton control area
        self.create_buttons()

        ### Input area
        self.create_forms(self.defaultParams)

        ### Text output area
        self.frm_txt = tk.Text(self)
        self.frm_txt.place(
            x=600,y=20,height=400,width=180)

    def create_form(self,dic):
        for idx, text in enumerate(dic.keys()):
            label = tk.Label(master=self, text=text,width=10,font=('Arial',LABEL_FONT))
            entry = tk.Entry(master=self, textvariable=dic[text],width=10,font=('Arial',LABEL_FONT))
            label.grid(row=idx+self.form_row, column=self.form_column,sticky="e")
            entry.grid(row=idx+self.form_row, column=self.form_column+1,sticky="e")
        # self.form_row+=len(dic.keys())

    def create_forms(self,dic):
        """Parse input dic and create forms for multiple parameters"""
        tk.Label(master=self, text="protocol",font=('Arial',LABEL_FONT)).grid(
            row=self.form_row, column=self.form_column, sticky="w")
        entry = tk.Entry(master=self, width=10,font=('Arial',LABEL_FONT))
        entry.grid(
            row=self.form_row, column=self.form_column+1, sticky="w")
        k="protocol"
        entry.insert(0,dic[k])
        self.form_row+=1
        self.run_params = {}
        for form in self.forms:
            self.run_params[form]={}
            for k,i in self.defaultParams[form].items():
                if isinstance(i,int): var = tk.IntVar()
                elif isinstance(i,float): var = tk.DoubleVar()
                else: var = tk.StringVar()
                var.set(i)
                self.run_params[form][k]=var
            tk.Label(master=self, text = form,font=('Arial',14)).grid(
                row=self.form_row, column=self.form_column, sticky="w")
            self.form_row+=1
            self.create_form(self.run_params[form])
            self.form_row=1
            self.form_column+=2
        ROW_MAX=max([len(i) if isinstance(i, dict) else 0 for i in self.run_params.values()])
        tk.Button(self, text ="Apply", font=('Arial',BOTTON_FONT),command=self.confirm_run_params).grid(
            row=(ROW_MAX+2), column=1, sticky="e")
        tk.Button(self, text ="Save", font=('Arial',BOTTON_FONT),command=self.save_run_params).grid(
            row=(ROW_MAX+2), column=2, sticky="w")

    def create_buttons(self):
        tk.Button(master=self,text='Home',font=('Arial',BOTTON_FONT),command=self.init_robot).grid(
            row=0, column=0, sticky="we")
        tk.Button(master=self,text='Run',font=('Arial',BOTTON_FONT),command=self.run_robot).grid(
            row=1, column=0, sticky="we")
        tk.Button(master=self,text='Pause',font=('Arial',BOTTON_FONT),command=self.pause_robot).grid(
            row=2, column=0, sticky="we")
        tk.Button(master=self,text='Resume',font=('Arial',BOTTON_FONT),command=self.resume_robot).grid(
            row=3, column=0, sticky="we")
        tk.Button(master=self,text='Back',font=('Arial',BOTTON_FONT),command=self.goToHome).grid(
            row=4, column=0, sticky="we")

    def showPage(self):
        self.tkraise()
        self.focus_set()

    def goToHome(self):
        self.master.showPage('HomePage')

    def run_robot(self):
        if self.para_confirmed:
            url=self.robot_url+'/run_robot'
            js=json.dumps(self.get_run_params())
            res=requests.get(url,json=self.get_run_params())
            self.frm_txt.insert(tk.END,"\n"+"*"*40+"\n")
            self.frm_txt.insert(tk.END,res.text)
            self.frm_txt.see(tk.END)
        else:
            self.frm_txt.insert(tk.END,"\n"+"*"*40+"\n")
            self.frm_txt.insert(tk.END,"Please confirm the run parameters first by pressing Apply botton")
            self.frm_txt.see(tk.END)

    def init_robot(self):
        if self.para_confirmed:
            url=self.robot_url+'/init_robot'
            js=json.dumps(self.get_run_params())
            res=requests.get(url,json=self.get_run_params())
            self.frm_txt.insert(tk.END,"\n"+"*"*40+"\n")
            self.frm_txt.insert(tk.END,res.text)
        else:
            self.frm_txt.insert(tk.END,"\n"+"*"*40+"\n")
            self.frm_txt.insert(tk.END,"Please confirm the run parameters first by pressing Apply botton")

    def pause_robot(self):
        url=self.robot_url+'/pause'
        res=requests.get(url,json=self.get_run_params())

    def resume_robot(self):
        url=self.robot_url+'/resume'
        res=requests.get(url,json=self.get_run_params())

    def get_run_params_1(self):
        #to be deleted after running the robot
        para = self.defaultParams
        for f in self.forms:
            para.pop(f)
            para[f]={}
            for k,i in self.run_params[f].items():
                try:
                    para[f][k]=i.get()
                except:
                    para[f][k] = self.defaultParams[f][k]
        return para

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
        pp=f".{self.defaultParams['protocol']}.configure"
        with open(pp, 'wt') as f:
            json.dump(para, f, indent=2)
        f.close()

class DTTPage(RunPage):
    pp=f".saliva_to_dtt.configure"
    if os.path.exists(pp):
        defaultParams = json.load(open(pp, 'rt'))
    else:
        defaultParams=saliva_to_dtt
    pass

class LAMPPage(RunPage):
    pp=f".sample_to_lamp_96well.configure"
    if os.path.exists(pp):
        defaultParams = json.load(open(pp, 'rt'))
    else:
        defaultParams=sample_to_lamp_96well
    pass


app = OpentronApp()
app.protocol('WM_DELETE_WINDOW',app.on_closing)
app.mainloop()
