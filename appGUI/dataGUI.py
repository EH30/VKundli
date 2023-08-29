import tkinter
import appGUI.kundliGUI
from AstroKundli import GKundli
from tkinter import messagebox, ttk

class AppButton:
    def __init__(self, root, command_a):
        self.ent_btn_enter = tkinter.Button(root, text="Enter", command=command_a, height=3, width=16)

class AppLabel:
    def __init__(self, root):
        self.lbl_name      = tkinter.Label(root, text="Name:")
        self.lbl_year      = tkinter.Label(root, text="Year:")
        self.lbl_month     = tkinter.Label(root, text="Month:")
        self.lbl_day       = tkinter.Label(root, text="Day:")
        self.lbl_hour      = tkinter.Label(root, text="Hour:")
        self.lbl_minute    = tkinter.Label(root, text="Minute:")
        self.lbl_utc       = tkinter.Label(root, text="UTC:")
        self.lbl_latitude  = tkinter.Label(root, text="Latitude:")
        self.lbl_longitude = tkinter.Label(root, text="Longitude:")

class AppEntry:
    def __init__(self, root):
        self.ent_name      = tkinter.Entry(root, width=20)
        self.ent_year      = tkinter.Entry(root, width=6)
        self.ent_month     = tkinter.Entry(root, width=3)
        self.ent_day       = tkinter.Entry(root, width=3)
        self.ent_hour      = tkinter.Entry(root, width=3)
        self.ent_minute    = tkinter.Entry(root, width=3)
        self.ent_utc       = tkinter.Entry(root, width=6)
        self.ent_latitude  = tkinter.Entry(root, width=10)
        self.ent_longitude = tkinter.Entry(root, width=10)

class AppDropDownList:
    def __init__(self, root):
        self.days   = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
            17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
        ]
        self.months = [1,2,3,4,5,6,7,8,9,10,11,12]
        self.hour   = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        self.minute = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
            31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60
        ]
        self.droplist_days   = ttk.Combobox(root, state="readonly", values=self.days, width=3)
        self.droplist_months = ttk.Combobox(root, state="readonly", values=self.months, width=3)
        self.droplist_hour  = ttk.Combobox(root, state="readonly", values=self.hour, width=3)
        self.droplist_minute = ttk.Combobox(root, state="readonly", values=self.minute, width=3)

class App:
    def __init__(self, root, top, image_pos, kundli_design):
        self.top  = top
        self.root = root
        self.kundli_design = kundli_design
        self.image_pos     = image_pos
        self.app_entry     = AppEntry(root)
        self.app_label     = AppLabel(root)
        self.app_button    = AppButton(root, self.gen_kundli)
        self.app_dropdownlist = AppDropDownList(root)

    def gen_kundli(self):
        name   = self.get_name()
        year   = self.get_year()
        month  = self.get_month()
        day    = self.get_day()
        lat    = self.get_latitude()
        lon    = self.get_longitude()
        utc    = self.get_utc()
        hour   = self.get_hour()
        minute = self.get_minute()
        if type(name) == int and name < 0:
            messagebox.showerror("Error Name", "Inavlid Name error code: {0}".format( name))
            return -1
        if year < 0:
            messagebox.showerror("Error Year", "Inavlid Year error code: {0}".format(year))
            return -1
        if month < 0:
            messagebox.showerror("Error month", "Inavlid month error code: {0}".format(month))
            return -1
        if day < 0:
            messagebox.showerror("Error day", "Inavlid day error code: {0}".format(day))
            return -1
        if lat < 0:
            messagebox.showerror("Error Latitude", "Inavlid Latitude error code: {0}".format(lat))
            return -1
        if lon < 0:
            messagebox.showerror("Error Longitude", "Inavlid Longitude error code: {0}".format(lon))
            return -1
        if type(utc) == int and utc < 0:
            messagebox.showerror("Error UTC", "Inavlid UTC error code: {0}".format(utc))
            return -1
        if hour < 0:
            messagebox.showerror("Error Hour", "Inavlid Hour error code: {0}".format(hour))
            return -1
        if minute < 0:
            messagebox.showerror("Error Minute", "Inavlid Minute error code: {0}".format(minute))
            return -1

        birth_chart   = GKundli.GKundli(year, month, day, hour, minute, utc, lat, lon).lagnaChart()
        transit_chart = GKundli.GKundli(year, month, day, hour, minute, utc, lat, lon).transitChart(birth_chart)

        appGUI.kundliGUI.KundliGUI(self.top, birth_chart, transit_chart, self.image_pos, self.kundli_design)
    
    def get_name(self):
        data = self.app_entry.ent_name.get()
        if len(data) == 0:
            return -1 
        
        return data.strip()
    
    def get_year(self):
        data = self.app_entry.ent_year.get().lower().strip("am pm")
        if len(data) == 0:
            return -1 
        
        if not data.isnumeric():
            return -2
        
        return int(data)
    
    def get_month(self):
        # data = self.app_entry.ent_month.get().lower().strip("am pm")
        data = self.app_dropdownlist.droplist_months.get()
        if len(data) == 0:
            return -1 
        
        if not data.isnumeric():
            return -2
        
        return int(data)
    
    def get_day(self):
        # data = self.app_entry.ent_day.get().lower().strip("am pm")
        data = self.app_dropdownlist.droplist_days.get()
        if len(data) == 0:
            return -1 
        
        if not data.isnumeric():
            return -2
        
        return int(data)
    
    def get_latitude(self):
        data = self.app_entry.ent_latitude.get().lower().strip("° E N W S")
        if len(data) == 0:
            return -1 
        
        return float(data)
    
    def get_longitude(self):
        data = self.app_entry.ent_longitude.get().lower().strip("° E N W S")
        if len(data) == 0:
            return -1 
        
        return float(data)
    
    def get_hour(self):
        # data = self.app_entry.ent_hour.get().lower().strip("am pm")
        data = self.app_dropdownlist.droplist_hour.get()
        if len(data) == 0:
            return -1 
        
        if not data.isnumeric():
            return -2
        
        return int(data)
    
    def get_minute(self):
        data = self.app_dropdownlist.droplist_minute.get().lower().strip("am pm")
        if len(data) == 0:
            return -1 
        
        if not data.isnumeric():
            return -2
        
        return int(data)
    
    def get_utc(self):
        data = self.app_entry.ent_utc.get().lower().strip("+ am pm")
        if len(data) == 0:
            return -1 
        
        out = ""
        for i in range(len(data)):
            if data[i] == ":" or data[i].isnumeric():
                out += data[i]
        
        return out
