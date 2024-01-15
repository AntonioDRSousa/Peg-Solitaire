import os
import tkinter as tk
from tkinter import Tk, ttk, Label
from Peg import Peg

class Menu:
    def __init__(self):
        root= Tk()
        root.geometry("600x600")
        root.resizable(False,False)
        root.title("PEG")
        self.win1 = tk.Frame(root)
        self.win2 = tk.Frame(root)
        self.win1.pack(fill='both',expand=1)
        self.createMenu()
        
    def createMenu(self):
        self.sboards=os.listdir(os.getcwd()+'/boards')
        for i in range(len(self.sboards)):
            self.sboards[i] = (self.sboards[i].split('.'))[0]
        self.nboards = len(self.sboards)
        self.pointer = 0
        
        self.ltitle = Label(self.win1,text='Board')
        self.bback = ttk.Button(self.win1,text='back')
        self.ltext = Label(self.win1,text=self.sboards[self.pointer])
        self.bnext = ttk.Button(self.win1,text='next')
        self.bstart = ttk.Button(self.win1,text='Start') 
        
        self.ltitle.grid(row=0,column=0,columnspan=3,sticky="news")
        self.bback.grid(row=1,column=0,sticky="news")
        self.ltext.grid(row=1,column=1,sticky="news")
        self.bnext.grid(row=1,column=2,sticky="news")
        self.bstart.grid(row=2,column=0,columnspan=3,sticky="news")
        
        self.bback.bind("<Button-1>",self.back)
        self.bnext.bind("<Button-1>",self.next)
        self.bstart.bind("<Button-1>",self.start)
        
        self.win1.mainloop()
        
    def back(self,event):
        pointer = (self.pointer-1)%self.nboards
        self.ltext.configure(text=self.sboards[pointer])
        
    def next(self,event):
        pointer = (self.pointer+1)%self.nboards
        self.ltext.configure(text=self.sboards[pointer])
        
    def start(self,event):
        Peg(self.win1,self.win2,self.sboards[self.pointer])