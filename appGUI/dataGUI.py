import swisseph as swe
import tkinter
import appGUI.kundliGUI
from AstroKundli import GKundli
from tkinter import messagebox, ttk

swe.set_ephe_path("resources\\swefiles")
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
        self.hour   = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        self.minute = [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
            31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59
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
        self.navamasa_mfd = {
            "move": [1,4,7,10],
            "fixed": [2,5,8,11],
            "dual": [3,6,9,12]
        }
        self.navamasa_degree = [
            [ 0,   3.2, 6.4, 10  , 13.2, 16.4, 20  ,  23.2, 26.4 ],
            [ 3.2, 6.4, 10,  13.2, 16.4, 20  , 23.2,  26.4, 30   ]
        ]

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
        if type(lat) != float:
            messagebox.showerror("Error Latitude", "Inavlid Latitude error code: {0}".format(lat))
            return -1
        if type(lon) != float:
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
        navamsa_chart = self.navamsaChart(birth_chart)
        moon_chart    = self.get_moon_chart(birth_chart)

        appGUI.kundliGUI.KundliGUI(self.top, birth_chart, navamsa_chart,
                                    transit_chart, moon_chart, self.image_pos, self.kundli_design, name, year, month, day, hour, minute, lat, lon, utc)
    
    def get_name(self):
        data = self.app_entry.ent_name.get()
        if len(data) == 0:
            return -1 
        
        return data.strip()
    
    def get_moon_chart(self, lagnaKundli):
        houses = {
            "1":{"sign_num":0, "asc":None, "planets":[]},
            "2":{"sign_num":0, "asc":None, "planets":[]},
            "3":{"sign_num":0, "asc":None, "planets":[]},
            "4":{"sign_num":0, "asc":None, "planets":[]},
            "5":{"sign_num":0, "asc":None, "planets":[]},
            "6":{"sign_num":0, "asc":None, "planets":[]},
            "7":{"sign_num":0, "asc":None, "planets":[]},
            "8":{"sign_num":0, "asc":None, "planets":[]},
            "9":{"sign_num":0, "asc":None, "planets":[]},
            "10":{"sign_num":0, "asc":None, "planets":[]},
            "11":{"sign_num":0, "asc":None, "planets":[]},
            "12":{"sign_num":0, "asc":None, "planets":[]}
        }
        first_house = 0
        for item in lagnaKundli:
            if len(lagnaKundli[item]["planets"]) != 0 and "Mo" in lagnaKundli[item]["planets"]:
                first_house = lagnaKundli[item]["sign_num"]
                break
        
        houses["1"]["sign_num"] = first_house
        for i in range(2,13):
            first_house += 1
            if first_house > 12:
                first_house = 1
            houses[str(i)]["sign_num"] = first_house
            if houses[str(i)]["sign_num"] == lagnaKundli["1"]["sign_num"]:
                houses[str(i)]["asc"] = lagnaKundli["1"]["asc"]
        
        for item in lagnaKundli:
             if len(lagnaKundli[item]["planets"]) != 0:
                for house in houses:
                    if houses[house]["sign_num"] == lagnaKundli[item]["sign_num"]:
                        for planet in lagnaKundli[item]["planets"]:
                            houses[house]["planets"].append(planet)
        return houses

    
    def get_start_count(self, sign_num, pos, current_house):
        if sign_num in self.navamasa_mfd["move"]:
            start_house = current_house
            for i in range(len(self.navamasa_degree[0])):
                if pos >= self.navamasa_degree[0][i] and pos <= self.navamasa_degree[1][i]:
                    house_to_count = i+1
                    current_house = start_house+house_to_count
                    return [start_house+1, house_to_count]
        elif sign_num in self.navamasa_mfd["fixed"]:
            start_house = 9+current_house if 9+current_house <= 12 else 9+current_house-12 
            for i in range(len(self.navamasa_degree[0])):
                if pos >= self.navamasa_degree[0][i] and pos <= self.navamasa_degree[1][i]:
                    house_to_count = i+1
                    current_house = start_house+house_to_count
                    return [start_house, house_to_count]
        elif sign_num in self.navamasa_mfd["dual"]:
            start_house = 5+current_house if 5+current_house <= 12 else 5+current_house-12
            for i in range(len(self.navamasa_degree[0])):
                if pos >= self.navamasa_degree[0][i] and pos <= self.navamasa_degree[1][i]:
                    house_to_count= i+1
                    current_house = start_house+house_to_count
                    return [start_house, house_to_count]
        

    def navamsaChart(self, kundli):
        asc = [int(kundli["1"]["sign_num"]),   float(kundli["1"]["asc"][1]
                                                     +kundli["1"]["asc"][2]+"."+kundli["1"]["asc"][4]
                                                     +kundli["1"]["asc"][5]) ]
        houses = {
            "1":{"sign_num":1, "asc":kundli["1"]["asc"], "planets":[]},
            "2":{"sign_num":2, "planets":[]},
            "3":{"sign_num":3, "planets":[]},
            "4":{"sign_num":4, "planets":[]},
            "5":{"sign_num":5, "planets":[]},
            "6":{"sign_num":6, "planets":[]},
            "7":{"sign_num":7, "planets":[]},
            "8":{"sign_num":8, "planets":[]},
            "9":{"sign_num":9, "planets":[]},
            "10":{"sign_num":10, "planets":[]},
            "11":{"sign_num":11, "planets":[]},
            "12":{"sign_num":12, "planets":[]}
        }
        count_house = self.get_start_count(asc[0], asc[1], 1-1)
        temp = count_house[0]-1
        for _ in range(count_house[1]):
            temp += 1
            if temp > 12:
                temp = 1
        
        for i in range(12):
            houses[str(i+1)]["sign_num"] = kundli[str(temp)]["sign_num"]
            temp += 1
            if temp > 12:
                temp = temp-12
        
        for house in kundli:
            if len(kundli[house]["planets"]) != 0:
                for item in kundli[house]["planets"]:
                    count_house = self.get_start_count(kundli[house]["sign_num"], float(kundli[house]["planets"][item][1]
                                                                                        +kundli[house]["planets"][item][2]+"."+kundli[house]["planets"][item][4]
                                                                                        +kundli[house]["planets"][item][5]   ), int(house)-1)
                    temp = count_house[0]-1
                    for _ in range(count_house[1]):
                        temp += 1
                        if temp > 12:
                            temp = 1
                    
                    rashi = kundli[str(temp)]["sign_num"]
                    for i in houses:
                        if houses[i]["sign_num"] == rashi:
                            houses[i]["planets"].append(item)
        return houses
    
    def get_year(self):
        data = self.app_entry.ent_year.get().lower().strip("am pm")
        if len(data) == 0:
            return -1 
        
        if not data.isnumeric():
            return -2
        
        return int(data)
    
    def get_month(self):
        # data = self.app_entry.ent_month.get().lower().strip("am pm")
        data = self.app_dropdownlist.droplist_months.get().strip()
        if len(data) == 0:
            return -1 
        
        if not data.isnumeric():
            return -2
        
        return int(data)
    
    def get_day(self):
        # data = self.app_entry.ent_day.get().lower().strip("am pm")
        data = self.app_dropdownlist.droplist_days.get().strip()
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
        data = self.app_dropdownlist.droplist_hour.get().strip()
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
        
        return data
