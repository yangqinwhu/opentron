import os
from pathlib import Path
import tkinter as tk
import shutil
import json,requests

SalivaToDTT={
    "protocol":"saliva_to_dtt",
    "robot_status":{
        "initialized":0,
        "to_run":1,
    },
    "robot_param":{
        "simulate":True,
        "deck":"saliva_to_dtt_biobank_96well_1000ul",
    },
    "sample_info":{
        "samples":8,
        "sample_per_column":8,
        "total_batch":2,
        "start_batch":2,
        "start_tube":1,
        "replicates":2,
    },
    "transfer_param":{
        "samp_vol":50,
        "air_vol": 25,
        "disp":1,
        "asp_bottom":10,
        "disp_bottom":2,
        'mix':0,
        "get_time":1,
        'dry_run':True,
        "aspirate_rate": 120,
        "dispense_rate": 120,
        "tip_press_increment":0.3,
        "tip_presses" : 1,
    },
}



class ScannerApp(tk.Tk):
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
    def __init__(self,parent,master):
        super().__init__(parent)
        self.master = master
        self.parent=parent
        self.robot_url="http://127.0.0.1:8000"
        self.forms=["robot_param","sample_info","transfer_param"]
        self.form_row=0
        # self.defaultParams=input
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
            x=400,y=20,height=400,width=380)

    def create_form(self,dic):
        for idx, text in enumerate(dic.keys()):
            label = tk.Label(master=self, text=text,font=('Arial',8))
            entry = tk.Entry(master=self, textvariable=dic[text],width=20,font=('Arial',8))
            label.grid(row=idx+self.form_row, column=1,sticky="e")
            entry.grid(row=idx+self.form_row, column=2,sticky="e")
        self.form_row+=len(dic.keys())

    def create_forms(self,dic):
        """Parse input dic and create forms for multiple parameters"""

        tk.Label(master=self, text="protocol").grid(
            row=self.form_row, column=1, sticky="e")
        entry = tk.Entry(master=self, width=20,font=('Arial',8))
        entry.grid(
            row=self.form_row, column=2, sticky="e")
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
            tk.Label(master=self, text = form,font=('Arial',10)).grid(
                row=self.form_row, column=1, sticky="e")
            self.form_row+=1
            self.create_form(self.run_params[form])
        tk.Button(self, text ="Apply", font=('Arial',10),command=self.confirm_run_params).grid(
            row=(self.form_row+1), column=1, sticky="e")
        tk.Button(self, text ="Save", font=('Arial',10)).grid(
            row=(self.form_row+1), column=2, sticky="w")

    def create_buttons(self):
        tk.Button(master=self,text='Run',font=('Arial',10),command=self.run_robot).grid(
            row=0, column=0, sticky="e")
        tk.Button(master=self,text='Home',font=('Arial',10)).grid(
            row=1, column=0, sticky="e")
        tk.Button(master=self,text='Stop',font=('Arial',10)).grid(
            row=2, column=0, sticky="e")
        tk.Button(master=self,text='Back',font=('Arial',10),command=self.goToHome).grid(
            row=3, column=0, sticky="e")

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
        else:
            self.frm_txt.insert(tk.END,"\n"+"*"*40+"\n")
            self.frm_txt.insert(tk.END,"Please confirm the run parameters first by pressing Apply botton")

    def get_run_params(self):
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

    def confirm_run_params(self):
        js=json.dumps(self.get_run_params(),indent=4)
        self.frm_txt.insert(tk.END,"\n"+"*"*40+"\n")
        self.frm_txt.insert(tk.END,js)
        self.para_confirmed=1

class DTTPage(RunPage):
    defaultParams=SalivaToDTT
    pass


class LAMPPage(RunPage):
    defaultParams=SalivaToDTT
    pass





app = ScannerApp()
app.protocol('WM_DELETE_WINDOW',app.on_closing)
app.mainloop()
# parent = tk.Frame()
# h=HomePage(parent,app)
# HomePage.__name__

#
# import tkinter as tk
#
# class MyApp():
#     def __init__(self):
#         self.root = tk.Tk()
#         l1 = tk.Label(self.root, text="Hello")
#         l2 = tk.Label(self.root, text="World")
#         l1.grid(row=0, column=0, )
#         l2.grid(row=1, column=0, )
#
# app = MyApp()
# app.root.mainloop()

# window.title("Simple Text Editor")
# window.rowconfigure(0, minsize=800, weight=1)
# window.columnconfigure(1, minsize=800, weight=1)
#
# txt_edit = tk.Text(window)
# fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
# btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
# btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)
#
# btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
# btn_save.grid(row=1, column=0, sticky="ew", padx=5)
#
# fr_buttons.grid(row=0, column=0, sticky="ns")
# txt_edit.grid(row=0, column=1, sticky="nsew")
#
# window.mainloop()
