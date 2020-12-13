import os
from pathlib import Path
import tkinter as tk
import shutil

class ScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Opentron app')
        self.geometry('800x480+0+-30')#-30
        self.resizable(0,0)

        container = tk.Frame(self)

        container.pack(side='top',fill='both',expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for F in (HomePage,RunPage,LogPage):
        #     self.pages[F.__name__] = F(parent=container,master=self)
        #     self.pages[F.__name__].grid(row=0, column=0, sticky="nsew")
        #
        # self.showPage('HomePage')

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
        tk.Button(self,text='Saliva to DTT P300',font=('Arial',55),command=lambda:self.master.showPage('DTTPage')).place(
            x=20,y=40,height=150,width=360)
        tk.Button(self,text='Sample to LAMP P20',font=('Arial',60),command=lambda:self.master.showPage('LAMPPage')).place(
            x=420,y=40,height=150,width=360)
        tk.Button(self,text='Exit',font=('Arial',60),command=self.master.on_closing).place(
            x=20,y=210,height=150,width=360)

    def showPage(self):
        self.tkraise()
        self.focus_set()

import tkinter as tk

window = tk.Tk()

# window = tk.Tk()
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
