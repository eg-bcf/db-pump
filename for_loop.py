import tkinter as Tkinter
import serial
import time
import statistics
import random
from decimal import *
from tkinter import messagebox
from datetime import datetime,tzinfo,timedelta
import sqlite3
from sqlalchemy import *

class App:
    def __init__(self, master):
        self.db = create_engine('sqlite:///pump.db')
        self.db.echo = False  # Try changing this to True and see what happens

        self.metadata = MetaData(self.db)

        self.pumps = Table('pumps', self.metadata,
            Column('board', String),
            Column('operator', String),
            Column('date', REAL),
            Column('serial_number', Integer),
            Column('pump_description', String),
            Column('velocity', Integer),
            Column('acceleration', Integer),
            Column('tpi', Integer),
            Column('sequential', Boolean),
            Column('dispense_percent', REAL),
            Column('dispense_1', REAL),
            Column('dispense_2', REAL),
            Column('dispense_3', REAL),
            Column('dispense_4', REAL),
            Column('dispense_5', REAL),
            Column('dispense_6', REAL),
            Column('dispense_7', REAL),
            Column('dispense_8', REAL),
            Column('dispense_9', REAL),
            Column('dispense_10', REAL),
            Column('backlash_value', REAL),
            Column('average', REAL),
            Column('stdev', REAL),
            Column('cv', REAL),
            Column('target', REAL),
            Column('variation', REAL),
            Column('test_description', Text)
        )

        b = list()

        backlash_value = "0.0150"
        for l in range(0,4):
            b.append(list())
            for t in range(0,10):
                b[l].append(float(l*random.randint(1,5)))

        tableData = list()
        objData = list()
        stTime = time.time()
        for k in range(0, 4):
            tableData.append(list())
            for z in range(0,10):
                tableData[k].append(float(b[k][z]))

        for j in range(0,4):
            objcontainer = {}
            objcontainer['board'] = 'all_motion'
            objcontainer['operator'] = 'jim beahm'
            objcontainer['date'] = stTime
            objcontainer['serial_number'] = '100'
            objcontainer['pump_description'] = 'MP5000CAV11200'
            objcontainer['velocity'] = int('8000')
            objcontainer['acceleration'] = int('100000')
            objcontainer['tpi'] = int('40')
            objcontainer['sequential'] =  True if b[j][0] <= 10 else False
            objcontainer['dispense_percent'] = float(b[j][0])
            for i in range(0,10):
                objcontainer['dispense_' + str(i)] = b[j][i]
            objcontainer['backlash_value'] = float('0.0150')
            objcontainer['average'] = 100.0000 #statistics.mean(tableData[j-1])
            objcontainer['stdev'] = 100.0000 #statistics.pstdev(tableData[j-1])
            objcontainer['cv'] = 100.0000 #statistics.pstdev(tableData[j-1])/statistics.mean(tableData[j-1])*100
            volume = int(b[j][0])/100 * 5000
            objcontainer['target'] = volume
            objcontainer['variation'] = 1000.0000 #statistics.mean(tableData[j-1])/volume
            objcontainer['test_description'] = 'Standard Customer'
            objData.append(objcontainer)
        print(objData)

        pump = [{
            'board': 'all_motion',
            'operator': 'Jim Beahm',
            'date': 1517925648.7772746,
            'serial_number': 1,
            'pump_description': "MP5000CAV11200",
            'velocity': 16000,
            'acceleration': 100000,
            'tpi': 20,
            'sequential': True,
            'dispense_percent': .01,
            'dispense_1': 0.00102,
            'dispense_2': 0.001,
            'dispense_3': 0.00098,
            'dispense_4': 0.00099,
            'dispense_5': 0.001,
            'dispense_6': 0.001,
            'dispense_7': 0.00099,
            'dispense_8': 0.00099,
            'dispense_9': 0.00098,
            'dispense_10': 0.00099,
            'backlash_value': 0,
            'average': 0.0010,
            'stdev': 0.000011,
            'cv': 0.01120,
            'target': 0.0010,
            'variation': 0.994,
            'test_description': 'Standard Customer'
        },
        {
            'board': 'all_motion',
            'operator': 'Jim Beahm',
            'date': 1517925648.7772746,
            'serial_number': 1,
            'pump_description': "MP5000CAV11200",
            'velocity': 16000,
            'acceleration': 100000,
            'tpi': 20,
            'sequential': True,
            'dispense_percent': .10,
            'dispense_1': 0.00102,
            'dispense_2': 0.001,
            'dispense_3': 0.00098,
            'dispense_4': 0.00099,
            'dispense_5': 0.001,
            'dispense_6': 0.001,
            'dispense_7': 0.00099,
            'dispense_8': 0.00099,
            'dispense_9': 0.00098,
            'dispense_10': 0.00099,
            'backlash_value': 0,
            'average': 0.0010,
            'stdev': 0.000011,
            'cv': 0.01120,
            'target': 0.0010,
            'variation': 0.994,
            'test_description': 'Standard Customer'
        },
        {
            'board': 'all_motion',
            'operator': 'Jim Beahm',
            'date': 1517925648.7772746,
            'serial_number': 1,
            'pump_description': "MP5000CAV11200",
            'velocity': 16000,
            'acceleration': 100000,
            'tpi': 20,
            'sequential': True,
            'dispense_percent': .50,
            'dispense_1': 0.00102,
            'dispense_2': 0.001,
            'dispense_3': 0.00098,
            'dispense_4': 0.00099,
            'dispense_5': 0.001,
            'dispense_6': 0.001,
            'dispense_7': 0.00099,
            'dispense_8': 0.00099,
            'dispense_9': 0.00098,
            'dispense_10': 0.00099,
            'backlash_value': 0,
            'average': 0.0010,
            'stdev': 0.000011,
            'cv': 0.01120,
            'target': 0.0010,
            'variation': 0.994,
            'test_description': 'Standard Customer'
        },
        {
            'board': 'all_motion',
            'operator': 'Jim Beahm',
            'date': 1517925648.7772746,
            'serial_number': 1,
            'pump_description': "MP5000CAV11200",
            'velocity': 16000,
            'acceleration': 100000,
            'tpi': 20,
            'sequential': True,
            'dispense_percent': 1.00,
            'dispense_1': 0.00102,
            'dispense_2': 0.001,
            'dispense_3': 0.00098,
            'dispense_4': 0.00099,
            'dispense_5': 0.001,
            'dispense_6': 0.001,
            'dispense_7': 0.00099,
            'dispense_8': 0.00099,
            'dispense_9': 0.00098,
            'dispense_10': 0.00099,
            'backlash_value': 0,
            'average': 0.0010,
            'stdev': 0.000011,
            'cv': 0.01120,
            'target': 0.0010,
            'variation': 0.994,
            'test_description': 'Standard Customer'
        }]

        i = self.pumps.insert()
        print("past insert")
        for p in pump:
            print(p)
            i.execute(p)
            print("executed")
            #s = self.pumps.select()
            print("selected")
            #rs = s.execute()
            print("executed again")

        frame.grid(row=0, column=0, padx=20, pady=20)



if __name__ == "__main__":
    root = Tkinter.Tk()
    app = App(root)
    root.mainloop()
