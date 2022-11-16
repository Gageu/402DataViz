import pandas as pd
import numpy as np
from enum import IntEnum
import datetime as dt
from statistics import mode
import matplotlib.pyplot as plt

class Condtion(IntEnum):
   # """Enum class for the condition of the weather"""
    FAIR = 0
    PARTLY_CLOUDY = 1
    CLOUDY = 2
    MOSTLY_CLOUDY = 3
    OVERCAST = 4
    LIGHT_RAIN = 5
    RAIN = 6
    HEAVY_RAIN = 7
    LIGHT_SNOW = 8
    SNOW = 9
    HEAVY_SNOW = 10
    STORMY = 11

def intfromstr(string):
    a = int(''.join(filter(str.isdigit, string)))
    return a

def parse_condition(str):
    if str == 'Fair':
        return Condtion.FAIR
    elif str == 'Partly Cloudy':
        return Condtion.PARTLY_CLOUDY
    elif str == 'Cloudy':
        return Condtion.CLOUDY
    elif str == 'Mostly Cloudy':
        return Condtion.MOSTLY_CLOUDY
    elif str == 'Overcast':
        return Condtion.OVERCAST
    elif str == 'Light Rain':
        return Condtion.LIGHT_RAIN
    elif str == 'Rain':
        return Condtion.RAIN
    elif str == 'Heavy Rain':
        return Condtion.HEAVY_RAIN
    elif str == 'Light Snow':
        return Condtion.LIGHT_SNOW
    elif str == 'Snow':
        return Condtion.SNOW
    elif str == 'Heavy Snow':
        return Condtion.HEAVY_SNOW
    elif str == 'Stormy':
        return Condtion.STORMY
    else:
        return Condtion.FAIR

class time_entry:
    time = dt.datetime.strptime('12:00 AM', '%I:%M %p')
    temp = 0
    caffeine = 0
    condition = Condtion.FAIR
    windy = False

    def __init__(self, time_str, temp, caffeine, condition, windy):
        self.time = dt.datetime.strptime(time_str, '%I:%M %p')
        self.temp = temp
        self.caffeine = caffeine
        self.condition = parse_condition(condition)
        self.windy = windy

class day:
    date = dt.date(2022, 1, 1)
    campus_hours = 0
    average_temp = 0
    average_caffeine = 0
    average_condition = Condtion.FAIR
    average_windy = False
    HOURS = ('05:00 AM',
             '06:00 AM',
             '07:00 AM',
             '08:00 AM', 
             '09:00 AM',
             '10:00 AM',
             '11:00 AM',
             '12:00 PM',
             '01:00 PM',
             '02:00 PM',
             '03:00 PM',
             '04:00 PM',
             '05:00 PM',
             '06:00 PM',
             '07:00 PM',
             '08:00 PM',
             '09:00 PM',
             '10:00 PM',
             '11:00 PM',
             '12:00 AM',
             '01:00 AM',
             '02:00 AM',)

    def __init__(self, date, caffeine, temp, condition, windy, campus_hours):
        self.Times = []
        for i in range (0, len(self.HOURS)-1):
            self.Times.append(time_entry(self.HOURS[i], intfromstr(temp[i]), intfromstr(caffeine[i]), parse_condition(condition[i]), windy[i]))
            
        self.average_temp = np.mean([x.temp for x in self.Times if x.caffeine > 0])
        self.average_caffeine = np.mean([x.caffeine for x in self.Times if x.caffeine > 0])
        self.average_condition = mode([int(x.condition) for x in self.Times])
        self.average_windy = mode([int(x.windy) for x in self.Times])
        self.date = dt.datetime.strptime(date, '%m/%d/%y')
        self.campus_hours = campus_hours

    def print_avg(self):
        print(self.date)
        print('Average Temp: ' + str(self.average_temp))
        print('Average Caffeine: ' + str(self.average_caffeine))
        print('Average Condition: ' + str(self.average_condition))
        print('Average Windy: ' + str(self.average_windy) + '\n\n')


class Data:

    def __init__(self, cfname, wfname, confname):
        self.days = []
        self.weather_raw = pd.read_csv(wfname)
        self.caffeine_raw = pd.read_csv(cfname)
        self.conditions_raw = pd.read_csv(confname)


        self.caffeine_raw.drop(columns=self.caffeine_raw.columns[0], axis=1, inplace=True)
        self.caffeine_raw.drop(self.caffeine_raw.tail(2).index, inplace=True)
        self.caffeine_raw.drop([0], inplace=True)

        self.weather_raw.dropna(thresh=2, inplace=True)
        self.weather_raw.dropna(axis='columns' , thresh=2, inplace=True)
        self.weather_raw.drop(columns=self.weather_raw.columns[0], axis=1, inplace=True)
        
        self.conditions_raw.dropna(thresh=2, inplace=True)
        self.conditions_raw.dropna(axis='columns' , thresh=2, inplace=True)
        self.conditions_raw.drop(columns=self.conditions_raw.columns[0], axis=1, inplace=True)
        self.conditions_raw.drop([54], inplace=True)

        delta = (dt.date.today() - dt.date(2022, 10, 24)).days

        print(self.caffeine_raw)
        print(self.weather_raw)
        print(self.conditions_raw)
        print (delta)

        for i in range(delta):
            windy = []
            date = self.weather_raw.iat[0, i]
            caffeine = self.caffeine_raw.iloc[:, i].to_numpy()
            temp = self.weather_raw.iloc[1:, i].to_numpy()
            condition = self.conditions_raw.iloc[:, i].to_numpy()
            for j in condition:
                if type(j) != str:
                    windy.append(False)
                else:
                    if len(str.split(j, ' / ')) > 1:
                        condition[condition == j] = str.split(j, ' / ')[0]
                        windy.append(True)
                    else:
                        windy.append(False)
            
            campus_hours = self.caffeine_raw.iat[-1, i]
            self.days.append(day(date, caffeine, temp, condition, windy, campus_hours))

        




#"""Main"""
gage_data = Data("Data - Gage's Data (1).csv", "Data - Processed Weather.csv", "Data - Processed Conditions.csv")
keegan_data = Data("Data - Keegan's Data.csv", "Data - Processed Weather.csv", "Data - Processed Conditions.csv")
ryan_data = Data("Data - Ryan's Data.csv", "Data - Processed Weather.csv", "Data - Processed Conditions.csv")
taylor_data = Data("Data - Taylor's Data.csv", "Data - Processed Weather.csv", "Data - Processed Conditions.csv")

print (len(gage_data.days))
print (len(gage_data.days[0].Times))
for day in gage_data.days:
    print(day.date.strftime('%H:%M %p'))
    day.print_avg()
    print( day.campus_hours)
    print('Time\t\tTemp\tCaffeine\tCondition\tWindy')
    print(len(day.Times))
    for time in day.Times:
        print("{}\t{}\t{}\t{}\t{}".format(time.time, time.temp, time.caffeine, time.condition, time.windy))
    print('\n\n')

