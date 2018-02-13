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
        self.go = 2
        self.state = 1

        self.db = create_engine('sqlite:///pump.db')
        self.db.echo = False  # Try changing this to True and see what happens

        self.metadata = MetaData(self.db)

        self.pumps = Table('pumps', self.metadata,
            Column('board', String),
            Column('operator', String),
            Column('date', REAL),#how
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

        frame = Tkinter.Frame(master)

        self.communication_options = Tkinter.LabelFrame(frame, text="Communication Options", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.communication_options.grid(row=0, column=0, padx=20, pady=20, rowspan=2)

        self.scale_com_label = Tkinter.Label(self.communication_options, text="Scale COM Port")
        self.scale_com_label.grid(row=0, column=0, padx=5, pady=5)

        self.scale_com = Tkinter.StringVar()
        self.scale_com.set("COM7")
        self.scale_port = Tkinter.Entry(self.communication_options, textvariable=self.scale_com)
        self.scale_port.grid(row=1,column=0, padx=5, pady=5)

        self.scale_connect = Tkinter.Button(self.communication_options, text="Scale Connect", bd=10, height=1, width=10, command=self.createScalePort)
        self.scale_connect.grid(row=2, column=0, padx=5, pady=5)

        self.piston_com_label = Tkinter.Label(self.communication_options, text="Pump COM Port")
        self.piston_com_label.grid(row=3, column=0, padx=5, pady=5)

        self.piston_com = Tkinter.StringVar()
        self.piston_com.set("COM12")
        self.piston_port = Tkinter.Entry(self.communication_options, textvariable=self.piston_com)
        self.piston_port.grid(row=4,column=0, padx=5, pady=5)

        self.piston_address_label = Tkinter.Label(self.communication_options, text="Pump Address")
        self.piston_address_label.grid(row=5, column=0, padx=5, pady=5)

        self.piston_address = Tkinter.StringVar()
        self.piston_address.set("1")
        self.piston_address = Tkinter.Entry(self.communication_options, textvariable=self.piston_address)
        self.piston_address.grid(row=6,column=0, padx=5, pady=5)

        self.piston_connect = Tkinter.Button(self.communication_options, text="Piston Connect", bd=10, height=1, width=10, command=self.createPistonPort)
        self.piston_connect.grid(row=7, column=0, padx=5, pady=5)

        self.operator_label = Tkinter.Label(self.communication_options, text="Operator")
        self.operator_label.grid(row=8, column=0, padx=5, pady=5)

        self.operator_name = Tkinter.StringVar()
        self.operator_name.set("Jim Beahm")
        self.operator_entry = Tkinter.Entry(self.communication_options, textvariable=self.operator_name)
        self.operator_entry.grid(row=9,column=0, padx=5, pady=5)

        self.sn_label = Tkinter.Label(self.communication_options, text="Serial #")
        self.sn_label.grid(row=10, column=0, padx=5, pady=5)

        self.sn = Tkinter.StringVar()
        self.sn.set("#########")
        self.sn_entry = Tkinter.Entry(self.communication_options, textvariable=self.sn)
        self.sn_entry.grid(row=11,column=0, padx=5, pady=5)

        self.piston_desc_label = Tkinter.Label(self.communication_options, text="Piston Desc")
        self.piston_desc_label.grid(row=12, column=0, padx=5, pady=5)

        self.piston_desc = Tkinter.StringVar()
        self.piston_desc.set("MP5000CAV11200")
        self.piston_desc_entry = Tkinter.Entry(self.communication_options, textvariable=self.piston_desc)
        self.piston_desc_entry.grid(row=13,column=0, padx=5, pady=5)

        self.save_data = Tkinter.Button(self.communication_options, text="Save", bd=10, height=1, width=10, command=self.saveFile)
        self.save_data.grid(row=14, column=0, padx=5, pady=5)

        self.piston_a = Tkinter.StringVar()
        self.piston_a.set("100000")


        self.piston_v = Tkinter.StringVar()
        self.piston_v.set("16000")

        self.piston_t = Tkinter.StringVar()
        self.piston_t.set("20")

        ################
        self.scale_options = Tkinter.LabelFrame(frame, text="Scale Commands", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.scale_options.grid(row=0, column=1, padx=20, pady=20)

        self.scale_weight_label = Tkinter.Label(self.scale_options, text="Most Recent Reading")
        self.scale_weight_label.grid(row=0, column=0, padx=5, pady=5)

        self.scale_weight = Tkinter.StringVar()
        self.scale_weight.set("Take A Reading")
        self.scale_weight_holder = Tkinter.Entry(self.scale_options, textvariable= self.scale_weight)
        self.scale_weight_holder.grid(row=1,column=0, padx=5, pady=5)

        self.get_scale_data = Tkinter.Button(self.scale_options, text="READ MASS", bd=10, height=1, width=10, command=lambda: self.insertData(self.target_coords["x"],self.target_coords["y"]))
        self.get_scale_data.grid(row=2, column=0, padx=5, pady=5)

        self.zero_scale_data = Tkinter.Button(self.scale_options, text="ZERO SCALE", bd=10, height=1, width=10, command=self.zeroScale)
        self.zero_scale_data.grid(row=3, column=0, padx=5, pady=5)
        ##########################

        self.piston_test_options = Tkinter.LabelFrame(frame, text="Piston Setup", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.piston_test_options.grid(row=1, column=1, padx=20, pady=20)

        self.setup_piston = Tkinter.Button(self.piston_test_options, text="SETUP", bd=10, height=1, width=10, command=self.setupPump)
        self.setup_piston.grid(row=2, column=0, padx=5, pady=5)

        self.home_piston = Tkinter.Button(self.piston_test_options, text="HOME", bd=10, height=1, width=10, command=self.homePiston)
        self.home_piston.grid(row=3, column=0, padx=5, pady=5)

        self.prime = Tkinter.Button(self.piston_test_options, text="PRIME", bd=10, height=1, width=10, command=self.primePiston)
        self.prime.grid(row=4, column=0, padx=5, pady=5)

        self.stop = Tkinter.Button(self.piston_test_options, text="STOP", bd=10, height=1, width=10, command=self.stopPiston)
        self.stop.grid(row=5, column=0, padx=5, pady=5)

        self.run = Tkinter.Button(self.piston_test_options, text="RUN", bd=10, height=1, width=10, command=self.startAuto)
        self.run.grid(row=6, column=0, padx=5, pady=5)

        self.clear = Tkinter.Button(self.piston_test_options, text="CLEAR", bd=10, height=1, width=10, command=lambda: self.clearAll(self.table_values, int(self.number_dispenses.get())+1, self.dispenses.get()))
        self.clear.grid(row=7, column=0, padx=5, pady=5)

        self.dbButton = Tkinter.Button(self.piston_test_options, text="DB", bd=10, height=1, width=10, command=lambda: self.dbFunc())
        self.dbButton.grid(row=8, column=0, padx=5, pady=5)

        self.populateButton = Tkinter.Button(self.piston_test_options, text="DB", bd=10, height=1, width=10, command=self.populate)
        self.populateButton.grid(row=9, column=0, padx=5, pady=5)
        ##############################################

        self.dispense_options = Tkinter.LabelFrame(frame, text="Dispense Options", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.dispense_options.grid(row=0, column=2, padx=20, pady=20)

        self.dispense_1 = Tkinter.Button(self.dispense_options, text="1%", bd=10, height=1, width=10, command=lambda: self.dispensePercent(1))
        self.dispense_1.grid(row=0, column=0, padx=5, pady=5)

        self.dispense_10 = Tkinter.Button(self.dispense_options, text="10%", bd=10, height=1, width=10, command=lambda: self.dispensePercent(10))
        self.dispense_10.grid(row=1, column=0, padx=5, pady=5)

        self.dispense_50 = Tkinter.Button(self.dispense_options, text="50%", bd=10, height=1, width=10, command=lambda: self.dispensePercent(50))
        self.dispense_50.grid(row=2, column=0, padx=5, pady=5)

        self.dispense_100 = Tkinter.Button(self.dispense_options, text="100%", bd=10, height=1, width=10, command=lambda: self.dispensePercent(100))
        self.dispense_100.grid(row=3, column=0, padx=5, pady=5)
        ######################################

        self.aspirate_options = Tkinter.LabelFrame(frame, text="Aspirate Options", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.aspirate_options.grid(row=1, column=2, padx=20, pady=20)

        self.aspirate_1 = Tkinter.Button(self.aspirate_options, text="1%", bd=10, height=1, width=10, command=lambda: self.aspiratePercent(1))
        self.aspirate_1.grid(row=0, column=0, padx=5, pady=5)

        self.aspirate_10 = Tkinter.Button(self.aspirate_options, text="10%", bd=10, height=1, width=10, command=lambda: self.aspiratePercent(10))
        self.aspirate_10.grid(row=1, column=0, padx=5, pady=5)

        self.aspirate_50 = Tkinter.Button(self.aspirate_options, text="50%", bd=10, height=1, width=10, command=lambda: self.aspiratePercent(50))
        self.aspirate_50.grid(row=2, column=0, padx=5, pady=5)

        self.aspirate_100 = Tkinter.Button(self.aspirate_options, text="100%", bd=10, height=1, width=10, command=lambda: self.aspiratePercent(100))
        self.aspirate_100.grid(row=3, column=0, padx=5, pady=5)

        ######################################################
        self.directory_path = Tkinter.StringVar()
        self.directory_path.set("C:\\Users\\egardner\\Desktop")


        self.file_path = Tkinter.StringVar()
        self.file_path.set("Sample")
        ###############################################

        self.target_coords = {"x":1,"y":1}

        self.tableReadData = []
        self.b = list()

        self.number_dispenses = Tkinter.StringVar()
        self.number_dispenses.set("10")

        self.dispenses = Tkinter.StringVar()
        self.dispenses.set("1,10,50,100")

        self.table_values = Tkinter.LabelFrame(frame, text="Values", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
        self.table_values.grid(row=0, column=4, padx=20, pady=20)

        self.createTable(self.number_dispenses.get(), self.dispenses.get())

        self.backlash_value = Tkinter.StringVar()
        self.backlash_value.set("0")

        frame.grid(row=0, column=0, padx=20, pady=20)

    def clearAll(self, frame, width, height):
        height = len([dispense.strip() for dispense in height.split(',')]) + 1
        tableData = list()
        for y in range(height):
            tableData.append(list())
            for x in range(width):
                tableData[y].append(self.b[y][x].get())
        self.tableReadData = tableData
        self.tableMaker1(tableData)

    def populate(self):
        self.backlash_value.set("0.0150")
        for i in range(1,5):
            for j in range(1,11):
                self.b[i][j].insert(0, float(i*random.randint(1,5)))

    def dbFunc(self):
        tableData = list()
        objData = list()
        stTime = time.time()
        for j in range(1, 5):
            tableData.append(list())
            for i in range(1,11):
                tableData[j-1].append(float(self.b[j][i].get()))
        for j in range(1, len(self.b)):
            objcontainer = {}
            objcontainer['board'] = 'all_motion'
            objcontainer['operator'] = self.operator_name.get()
            objcontainer['date'] = stTime
            objcontainer['serial_number'] = self.sn.get()
            objcontainer['pump_description'] = self.piston_desc.get()
            objcontainer['velocity'] = self.piston_v.get()
            objcontainer['acceleration'] = self.piston_a.get()
            objcontainer['tpi'] = self.piston_t.get()
            objcontainer['sequential'] =  True if int(self.b[j][0].get()) <= 10 else False
            objcontainer['dispense_percent'] = int(self.b[j][0].get())
            for i in range(1,11):
                objcontainer['dispense_' + str(i)] = float(self.b[j][i].get())
            objcontainer['backlash_value'] = float(self.backlash_value.get())
            objcontainer['average'] = statistics.mean(tableData[j-1])
            objcontainer['stdev'] = statistics.pstdev(tableData[j-1])
            objcontainer['cv'] = statistics.pstdev(tableData[j-1])/statistics.mean(tableData[j-1])*100
            volume = int(self.b[j][0].get())/100 * int(self.piston_desc.get()[2:6])
            objcontainer['target'] = volume
            objcontainer['variation'] = statistics.mean(tableData[j-1])/volume
            objcontainer['test_description'] = 'Standard Customer'
            objData.append(objcontainer)
        print(objData)
        i = self.pumps.insert()
        for p in objData:
            print(p)
            i.execute(p)
            #s = self.pumps.select()
            #rs = s.execute()
        """
        self.pump = [{
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
        """

    def startAuto(self):
        EST = Zone(-5,False,'EST')
        print(datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z'))
        print("I'm Starting")
        self.target_coords = {"x":1,"y":1}
        desc_string = self.piston_desc.get()
        if len(desc_string) <= 13 or len(desc_string) >= 15:
            return messagebox.showerror("Error", "Check to make Sure that the piston description is properly written")
        else:
            pass
        try:
            threads = int(desc_string[11]) * 10
            if threads != 20 and threads != 40:
                return messagebox.showerror("Error", "Check to make Sure threads are 20 or 40")
            else:
                pass
        except:
            return messagebox.showerror("Error", "Make sure a number is entered in the threads field")
        try:
            volume = int(desc_string[2:6])
        except:
            return messagebox.showerror("Error", "Make sure a number is entered in the volume field")
        result = messagebox.askyesno("Final Check","{} {} {} {} {}".format("Are you sure you want to run a test for a pump with: \n", "Operator: " + self.operator_name.get() + "\n", "tpi: " + str(threads) + "\n", "volume: " + str(volume) + "\n", "Serial Number: " + self.sn.get()))
        if result == True:
            self.piston_t.set(str(threads))
            self.state = 1
            self.go = 2
            self.getBacklashValue(4)
        else:
            pass

    def getBacklashValue(self, status):
        print("status main: " + str(status))
        if status == 1:
            print("now I'll move")
            self.dispensePercent(1)
            root.after(2000, self.getBacklashValue(2))
        elif status == 2:
            print("gonna look for that backlash now")
            self.scale.flushInput()
            self.waitForBacklash()
        elif status == 3:
            print("on to the next loop")
            self.getData2()
        elif status == 4:
            print("gonna zero this first")
            self.getBacklashZero()

    def getBacklashZero(self):
        print("In backlash zero")
        self.zeroScale()
        x = self.scale.readline()
        print("x zero: " + str(x))
        decoded = str(x.decode('utf-8').strip())
        print("decoded zero: " + decoded)
        if len(decoded) >= 3:
            if decoded[0] == 'Z' and decoded[2] == 'A':
                print(decoded)
                print('got the backlash zero')
                root.after(2000, self.getBacklashValue(1))
            else:
                print('seeking backlash zero inner')
                root.after(1000, self.getBacklashZero)
        elif len(decoded) < 3:
            print('seeking backlash zero outer')
            root.after(1000, self.getBacklashZero)

    def waitForBacklash(self):
        self.readScale()
        x = self.scale.readline()
        print("x wait for backlash: " + str(x))
        decoded = str(x.decode('utf-8').strip())
        print("decoded wait for backlash: " + decoded)
        if len(decoded) >= 3:
            if decoded[0] == 'S' and decoded[2] == 'S':
                weight = decoded[3:].strip().split(' ')
                print('got the backlash weight')
                print(weight[0])
                self.backlash_value.set(weight[0])
                print('Backlash: ' + self.backlash_value.get())
                print('changed backlash')
                if float(weight[0]) <= .005:
                    root.after(1000, self.waitForBacklash)
                elif float(weight[0]) > .005:
                    self.getBacklashValue(3)
            else:
                print('seeking backlash inner')
                root.after(1000, self.waitForBacklash)
        elif len(decoded) < 3:
            print('seeking backlash outer')
            root.after(1000, self.waitForBacklash)

    def saveFile(self):
        result = messagebox.askyesno("Did you chceck to make sure that there are no zero's in the data")
        if result == True:
            self.dataReadout(self.table_values, int(self.number_dispenses.get())+1, self.dispenses.get())
            intTable = list()
            for i in range(1,len(self.tableReadData)):
                intTable.append(list())
                for j in range(1,len(self.tableReadData[0])):
                    if len(self.tableReadData[i][j]):
                        intTable[i-1].append(float(self.tableReadData[i][j]))
                    else:
                        intTable[i-1].append(0)
            dataTable = list()
            self.tableReadData[0].append('Average')
            self.tableReadData[0].append('Std Dev')
            self.tableReadData[0].append('COV')
            for z in range(0,len(intTable)):
                dataTable.append(list())
                dataTable[z].append(statistics.mean(intTable[z]))
                self.tableReadData[z+1].append(statistics.mean(intTable[z]))
                dataTable[z].append(statistics.pstdev(intTable[z]))
                self.tableReadData[z+1].append(statistics.pstdev(intTable[z]))
                dataTable[z].append(dataTable[z][1]/dataTable[z][0]*100)
                self.tableReadData[z+1].append(dataTable[z][1]/dataTable[z][0])
            dname = "M:\\piston_pump_testing\\practice"
            fname = self.sn.get()
            ftype = ".txt"
            full_path = dname + '\\' + fname + "_" + str(time.time()) + ftype
            F = open(full_path,"w+")
            F.write("Operator:" + "\t" + self.operator_name.get() + '\n')
            EST = Zone(-5,False,'EST')
            F.write("Date:" + "\t" + datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z') + '\n')
            F.write("Serial #:" + "\t" + self.sn.get() + '\n')
            F.write("Pump #:" + "\t" + self.piston_desc.get() + '\n')
            F.write("Accel:" + "\t" + self.piston_a.get() + '\n')
            F.write("Velocity:" + "\t" + self.piston_v.get() + '\n')
            F.write("Backlash Volume:" + "\t" + self.backlash_value.get() + '\n')
            for i in self.tableReadData:
                F.write('\n')
                for j in range(0,len(i)):
                    F.write(str(i[j]) + "\t")
            F.close()
            self.clearAll(self.table_values, int(self.number_dispenses.get())+1, self.dispenses.get())
            self.sn.set("####")

    def getData(self):
        print('started seeking')
        self.waitForZero()
        print('done seeking')
        x = self.scale.readline()
        if len(x) > 0:
            decoded = str(x.decode('utf-8').strip())
            weight = decoded[3:].strip().split(' ')
            self.scale_weight.set(weight[0])

    def getData2(self):
        print("IN THE DATA COLLECTION")
        if self.state == 1:
            if self.go == 0:
                #### Non Sequential Zeroing
                print('started seeking non sequential zero')
                self.scale.flushInput()
                self.waitForNonSequentialZero()
                self.scale.flushInput()
            elif self.go == 1:
                ### Sequential Zeroing
                print('started seeking sequential zero')
                #print('seeking weight')
                #self.waitForWeight()
                self.scale.flushInput()
                self.waitForSequentialZero()
                self.scale.flushInput()
            elif self.go == 2:
                #### Movement Decision
                print('choosing decision path')
                self.choosePath(self.target_coords["x"],self.target_coords["y"])
                #print('found weight')
                #print('inserting')
                #self.insertData(self.target_coords["x"],self.target_coords["y"])
                #print('inserted')
            elif self.go == 3:
                #### Non Sequential movement
                print('moving pump')
                self.movePistonToNextPosition(self.target_coords['x'], self.target_coords['y'])
            elif self.go == 5:
                ### Wait for weight
                print('waiting for the weight')
                self.scale.flushInput()
                self.waitForAutoWeight()
                self.scale.flushInput()
                print('found weight')
            elif self.go == 6:
                print('inserting')
                self.insertAutoData(self.target_coords["x"],self.target_coords["y"])
                print('inserted')
            else:
                print('all over')
                pass

    def waitForNonSequentialZero(self):
        print("I'm waiting for a non sequential zero")
        if self.go == 0:
            self.zeroScale()
            x = self.scale.readline()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'Z' and decoded[2] == 'A':
                    print(decoded)
                    print('got the zero')
                    self.go = 1
                    self.getData2()
                    return
                else:
                    print('seeking zero inner')
                    root.after(500, self.waitForZero)
            else:
                print('seeking zero outer')
                root.after(500, self.waitForZero)
        else:
            pass

    def waitForSequentialZero(self):
        print("I'm waiting for a sequential zero")
        if self.go == 1:
            self.zeroScale()
            x = self.scale.readline()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'Z' and decoded[2] == 'A':
                    print(decoded)
                    print('got the zero')
                    self.go = 3
                    self.getData2()
                    return
                else:
                    print('seeking zero inner')
                    root.after(500, self.waitForSequentialZero)
            else:
                print('seeking zero outer')
                root.after(500, self.waitForSequentialZero)
        else:
            pass

    def nextAutoTarget(self, x, y):
        height = len([dispense.strip() for dispense in self.dispenses.get().split(',')])
        if x >= int(self.number_dispenses.get()) and y < height:
            self.target_coords["x"] = 1
            self.target_coords["y"] = y + 1
            return
        elif x >= int(self.number_dispenses.get()) and y >= height:
            self.target_coords["x"] = 1
            self.target_coords["y"] = 1
            self.state = 0
            print('ending movement')
            self.getData2()
        else:
            self.target_coords["x"] = x + 1
            self.target_coords["y"] = y
            return

    def choosePath(self, x, y):
        if self.go == 2:
            height = len([dispense.strip() for dispense in self.dispenses.get().split(',')])
            print(int(self.b[y][0].get()))
            print(int(self.number_dispenses.get()))
            if (int(self.b[y][0].get()) <= 10 and x == 1) and y != 1:
                print('non sequential movement')
                self.aspiratePiston()
                self.go = 1
                root.after(1000, self.getData2)
            elif int(self.b[y][0].get()) <= 10 and x < int(self.number_dispenses.get()) + 2:
                print('sequential movement')
                self.go = 1
                self.getData2()
            else:
                print('non sequential movement')
                self.aspiratePiston()
                self.go = 1
                root.after(1000, self.getData2)

    def insertAutoData(self, x, y):
        if self.go == 6:
            self.b[y][x].delete(0, 'end')
            self.b[y][x].insert(0, self.scale_weight.get())
            self.nextAutoTarget(x, y)
            self.go = 2
            self.getData2()

    def sendData(self):
        y = str(self.scale_send.get()) + '\r\n'
        self.scale.write(y.encode('utf-8'))

    def zeroScale(self):
        print("I'm zeroing the scale")
        self.scale.write('Z\r\n'.encode('utf-8'))

    def readScale(self):
        print("I'm reading the scale")
        self.scale.write('S\r\n'.encode('utf-8'))

    def createScalePort(self):
        port = self.scale_com.get().upper()
        self.scale = serial.Serial(port, 9600, timeout=0)

    def createPistonPort(self):
        port = self.piston_com.get().upper()
        self.piston = serial.Serial(
            port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def sendToPiston(self):
        pistonData = 'j16m100R'
        piston_address = self.piston_address.get()
        finalPistonData = '/' + piston_address + pistonData + '\r\n'
        self.piston.write(finalPistonData.encode())

    ##################################

    def startTest(self):
        positions = self.piston_positions.get()
        pos_array = positions.split(',')
        pos_array = [ str(-64000 + 640 * int(x)) for x in pos_array] * int(self.piston_times.get())
        velocities = self.piston_velocities.get()
        vel_array = velocities.split(',') * int(self.piston_times.get())
        accelerations = self.piston_accelerations.get()
        accel_array = accelerations.split(',') * int(self.piston_times.get())
        self.positions = pos_array
        self.velocities = vel_array
        self.accelerations = accel_array
        self.test_state = 2
        self.idx = 0
        self.waitForScale()

    def homePiston(self):
        accel = str(round(int(self.piston_a.get()) * 65536 / 400000000))
        homeString = '/' + self.piston_address.get() + 'V' + self.piston_v.get() + 'L' + accel + 'ZR\r\n'
        self.piston.write(homeString.encode())

    def dispensePiston(self):
        dispenseString = '/' + self.piston_address.get() + 'V' + self.piston_v.get() + 'A0R\r\n'
        self.piston.write(dispenseString.encode())
        print("done dispensing")

    def aspiratePiston(self):
        threads = self.piston_desc.get()
        tpi = str(int(threads[11])*10)
        self.piston_t.set(tpi)
        accel = str(round(int(self.piston_a.get()) * 65536 / 400000000))
        aspirateString = '/' + self.piston_address.get() + 'V' + self.piston_v.get() + 'L' + accel  + 'A-' + str(int(self.piston_t.get()) * 1600) + 'R\r\n'
        self.piston.write(aspirateString.encode())
        return

    def primePiston(self):
        threads = self.piston_desc.get()
        tpi = str(int(threads[11])*10)
        self.piston_t.set(tpi)
        primeString = '/' + self.piston_address.get() + 'gV' + self.piston_v.get() + 'A-' + str(int(self.piston_t.get()) * 1600) + 'A0G10R\r\n'
        self.piston.write(primeString.encode())

    def stopPiston(self):
        self.go = 10
        self.state = 0
        stopString = '/' + self.piston_address.get() + 'TR\r\n'
        self.test_state = 0
        self.piston.write(stopString.encode())

    def setupPump(self):
        setupString = '/' + self.piston_address.get() + 'j16m100R\r\n'
        self.piston.write(setupString.encode())

    def dispensePercent(self, amount):
        threads = self.piston_desc.get()
        tpi = str(int(threads[11])*10)
        self.piston_t.set(tpi)
        steps = str(int(int(self.piston_t.get()) * 1600 * amount/100))
        accel = str(round(int(self.piston_a.get()) * 65536 / 400000000))
        dispenseString = '/' + str(self.piston_address.get()) + 'V' + self.piston_v.get() + 'L'  + accel + 'P' + steps + 'R\r\n'
        self.piston.write(dispenseString.encode())


    def aspiratePercent(self, amount):
        threads = self.piston_desc.get()
        tpi = str(int(threads[11])*10)
        self.piston_t.set(tpi)
        steps = str(int(int(self.piston_t.get()) * 1600 * amount/100))
        accel = str(round(int(self.piston_a.get()) * 65536 / 400000000))
        aspirateString = '/' + str(self.piston_address.get()) + 'V' + self.piston_v.get() + 'L'  + accel + 'D' + steps + 'R\r\n'
        self.piston.write(aspirateString.encode())

    def waitForScale(self):
        if self.test_state == 0:
            pass
        elif self.test_state == 1:
            x = self.scale.readline()
            if len(x) > 0:
                decoded = str(x.decode('utf-8').strip())
                weight = decoded[3:].strip().split(' ')
                #print(weight[0])
                self.test_weights.append(weight[0])
                self.scale_weight.set(weight[0])
                self.test_state = 2
                self.scale.flushInput()
            root.after(500, self.waitForScale)
        elif self.test_state == 2:
            command = '/' + self.piston_address.get() + 'L' + str(self.accelerations[self.idx]) + 'V' + str(self.velocities[self.idx]) + 'A' + str(int(self.positions[self.idx])) + 'R\r\n'
            #print(command)
            self.piston.write(command.encode())
            self.idx += 1
            root.after(1000)
            self.scale.write('S\r\n'.encode('utf-8'))
            self.test_state = 1
            self.waitForScale()

    ###
    def createTable(self, xdata, ydata):
        dispenseArray = [dispense.strip() for dispense in ydata.split(',')]
        dispenseArray.insert(0, 'Dispense %')
        value_height = int(len(dispenseArray))
        value_width = int(xdata) + 1
        num_array = [num for num in range(1,int(xdata)+1)]
        for y in range(value_height):
            self.b.append(list())
            for x in range(int(xdata)+1):
                self.b[y].append(Tkinter.Entry(self.table_values, text="", width=10))
                self.b[y][x].grid(row=y, column=x)
                #self.b[y][x].insert(0, str(round(random.random()*100)))
                data = { "row": y, "col": x }
                self.b[y][x].bind("<Button-1>", lambda event, arg=data: self.callback(event, arg))
        for y in range(value_height):
            self.b[y][0].delete(0, 'end')
            self.b[y][0].insert(0, dispenseArray[y])
        for x in range(1, len(num_array) + 1):
            self.b[0][x].delete(0, 'end')
            self.b[0][x].insert(0, num_array[x-1])

    def dataReadout(self, frame, width, height):
        height = len([dispense.strip() for dispense in height.split(',')]) + 1
        tableData = list()
        for y in range(height):
            tableData.append(list())
            for x in range(width):
                tableData[y].append(self.b[y][x].get())
        self.tableReadData = tableData
        self.tableMaker(tableData)

    def tableMaker(self, tableData):
        for y in range(len(tableData)):
            self.b.append(list())
            for x in range(len(tableData[0])):
                self.b[y].append(Tkinter.Entry(self.table_values, text="", width=5))
                self.b[y][x].grid(row=y, column=x)
                self.b[y][x].delete(0, 'end')
                self.b[y][x].insert(0, tableData[y][x])

    def tableMaker1(self, tableData):
        for y in range(len(tableData)):
            self.b.append(list())
            for x in range(len(tableData[0])):
                self.b[y].append(Tkinter.Entry(self.table_values, text="", width=5))
                self.b[y][x].grid(row=y, column=x)
                self.b[y][x].delete(0, 'end')
                if y == 0 or x == 0:
                    self.b[y][x].insert(0, tableData[y][x])

    def getTarget(self, x, y):
        self.target_coords["x"] = x
        self.target_coords["y"] = y

    def updateTarget(self, x, y):
        self.target_coords["x"] = x
        self.target_coords["y"] = y

    def nextTarget(self, x, y):
        print('in here')
        height = len([dispense.strip() for dispense in self.dispenses.get().split(',')])
        if x >= int(self.number_dispenses.get()) and y < height:
            self.target_coords["x"] = 1
            self.target_coords["y"] = y + 1
        elif x >= int(self.number_dispenses.get()) and y >= height:
            self.target_coords["x"] = 1
            self.target_coords["y"] = 1
        else:
            self.target_coords["x"] = x + 1
            self.target_coords["y"] = y

    def callback(self, event, arg):
        y = arg['row']
        x = arg['col']
        self.getTarget(x, y)

    def insertData(self, x, y):
        self.scale.flushInput()
        self.waitForWeight()
        self.b[y][x].delete(0, 'end')
        #self.b[y][x].insert(0, self.scale_weight.get())
        #self.nextTarget(x, y)

    def waitForZero(self):
        if self.go == 0:
            self.zeroScale()
            x = self.scale.readline()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'Z' and decoded[2] == 'A':
                    print(decoded)
                    print('got the zero')
                    self.go = 1
                    self.getData2()
                    return
                else:
                    print('seeking zero inner')
                    root.after(500, self.waitForZero)
            else:
                print('seeking zero outer')
                root.after(500, self.waitForZero)
        if self.go == 4:
            self.zeroScale()
            x = self.scale.readline()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'Z' and decoded[2] == 'A':
                    print(decoded)
                    print('got the zero')
                    self.go = 5
                    self.movePistonToNextPosition()
                    return
                else:
                    print('seeking zero inner')
                    root.after(500, self.waitForZero)
            else:
                print('seeking zero outer')
                root.after(500, self.waitForZero)
        else:
            pass

    def waitForWeight(self):
        self.readScale()
        x = self.scale.readline()
        decoded = str(x.decode('utf-8').strip())
        if len(decoded) >= 3:
            if decoded[0] == 'S' and decoded[2] == 'S':
                weight = decoded[3:].strip().split(' ')
                print('got the weight')
                print(weight[0])
                self.scale_weight.set(weight[0])
                print('changed weight')
                self.b[self.target_coords["y"]][self.target_coords["x"]].insert(0, self.scale_weight.get())
                print('inserted weight')
                self.nextTarget(self.target_coords["x"], self.target_coords["y"])
                print('changed coords')
                return
            else:
                print('seeking weight inner')
                root.after(500, self.waitForWeight)
        else:
            print('seeking weight outer')
            root.after(500, self.waitForWeight)

    def waitForAutoWeight(self):
        if self.go == 5:
            self.readScale()
            x = self.scale.readline()
            decoded = str(x.decode('utf-8').strip())
            if len(decoded) >= 3:
                if decoded[0] == 'S' and decoded[2] == 'S':
                    weight = decoded[3:].strip().split(' ')
                    self.scale_weight.set(weight[0])
                    self.go = 6
                    self.getData2()
                    return
                else:
                    root.after(500, self.waitForAutoWeight)
            else:
                root.after(500, self.waitForAutoWeight)
        else:
            pass

    def movePistonToNextPosition(self, x, y):
        if self.go == 3:
            targetPos = self.b[y][0].get()
            self.dispensePercent(int(targetPos))
            self.go = 5
            root.after(1000,self.getData2)


    def aspirateAndZero():
        threads = self.piston_desc.get()
        tpi = str(int(threads[11])*10)
        self.piston_t.set(tpi)
        aspirateString = '/' + self.piston_address.get() + 'V' + self.piston_v.get() + 'A-' + str(int(self.piston_t.get()) * 1600) + 'R\r\n'
        self.piston.write(aspirateString.encode())
        self.go = 4
        self.waitForZero()

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
         return self.name


if __name__ == "__main__":
    root = Tkinter.Tk()
    app = App(root)
    root.mainloop()
