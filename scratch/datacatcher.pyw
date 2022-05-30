import tkinter as tk
from tkinter import ttk
import serieslist
from ttkwidgets.autocomplete import AutocompleteCombobox
import webscraper

class MainFrame(ttk.Frame):
    def __init__(self,container,site,database):
        super().__init__(container)
        
        self.site = site
        self.database = database
        
        #Body
        
        self.title = ttk.Label(self, text='Symbol')
        self.title.grid(column=1,row=2, ipady=5)
        
        self.serie = tk.StringVar()
        self.seriecb = AutocompleteCombobox(self, width=50)        
        self.seriecb.grid(column=1,row=3)
        
        self.assettitle = ttk.Label(self, text='Asset')
        self.assettitle.grid(column=1,row=0, ipady=5)
        
        self.asset = AutocompleteCombobox(self, width=50, completevalues=list(site.values()))
        self.asset.grid(column=1,row=1)

        self.startdatetitle = ttk.Label(self, text='Start date')
        self.startdatetitle.grid(column=1,row=5, ipady=5, sticky='w')
    
        self.startdate = tk.Entry(self, width=25)
        self.startdate.grid(column=1,row=6, sticky='w')

        self.enddate = tk.Entry(self, width=25)
        self.enddate.grid(column=1,row=6, sticky='e')
       
        self.enddatetitle = ttk.Label(self, text='End date')
        self.enddatetitle.place(x=170,y=105)
        
        self.button = tk.Button(self, text='Export',command=self.getdata)
        self.button.grid(column=1,row=8, pady=20, ipadx=30, ipady=5)
        
        self.grid(column=1, row=0)
        self.populate(self.site)
        
        #Binds
        
        self.seriecb.bind('<<ComboboxSelected>>', self.getsymbolname)
        self.seriecb.bind('<Return>', self.getsymbolname)
        self.asset.bind('<<ComboboxSelected>>', self.getassetname)
        self.asset.bind('<Return>', self.getassetname)

    def populate(self, site):
        self.seriecb['values'] = list(site.keys())
        self.asset['values'] = list(site.values())
        

    def getsymbolname(self, event):
        try:
            self.asset.set(self.site.get(self.seriecb.get()))
        except:
            self.asset['text'] = ''

    def getassetname(self, event):
        try:
            self.seriecb.set(list(self.site.keys())[list(self.site.values()).index(self.asset.get())])
        except:
            self.asset['text'] = ''
            
    def getdata(self):
        method = self.database
        seriescode = self.seriecb.get()
        seriesstart = self.startdate.get()
        seriesend = self.enddate.get()
        getattr(webscraper, method)(seriescode, seriesstart, seriesend)


class WebsiteSelection(ttk.LabelFrame):
    def __init__(self, container):
        
        super().__init__(container)
        
        self.selected_value = tk.IntVar()
        self['text'] = 'Data Source'
        
        ttk.Radiobutton(
            self,
            text='Nasdaq',
            value=0,
            variable=self.selected_value,
            command=self.change_frame).grid(column=0,row=0)
        
        ttk.Radiobutton(
            self,
            text='B3',
            value=1,
            variable=self.selected_value,
            command=self.change_frame).grid(column=0,row=1)
        
        ttk.Radiobutton(
            self,
            text='BCB',
            value=2,
            variable=self.selected_value,
            command=self.change_frame).grid(column=0,row=2)
        
        ttk.Radiobutton(
            self,
            text='FRED',
            value=3,
            variable=self.selected_value,
            command=self.change_frame).grid(column=0,row=3)
        
        ttk.Radiobutton(
            self,
            text='IPEA',
            value=4,
            variable=self.selected_value,
            command=self.change_frame).grid(column=0,row=4)
        
        self.grid(column=0,row=0, padx= 20)
        
        self.frames = {}
        self.frames[0] = MainFrame(container, serieslist.nasdaqbase, 'NASDAQ')
        self.frames[1] = MainFrame(container, serieslist.b3base, 'B3')
        self.frames[2] = MainFrame(container, serieslist.bcbbase, 'BCB')
        self.frames[3] = MainFrame(container, serieslist.fredbase, 'FRED')
        self.frames[4] = MainFrame(container, serieslist.ipeabase, 'IPEA')
        
    def change_frame(self):
        frame = self.frames[self.selected_value.get()]
        frame.tkraise()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Data Catcher')
        self.geometry('500x230')
        self.resizable(False,False)
        
        
if __name__ == '__main__':
    app = App()
    WebsiteSelection(app)
    app.mainloop()
