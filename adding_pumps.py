import sqlite3
from sqlalchemy import *

db = create_engine('sqlite:///pump.db')
db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

pumps = Table('pumps', metadata,
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

i = pumps.insert()
#i.execute(name='Mary', age=30, password='secret')
for p in pump:
    i.execute(p)

s = pumps.select()
rs = s.execute()
"""
row = rs.fetchone()
print('Id:', row[0])
print('Name:', row['name'])
print('Age:', row.age)
print('Password:', row[users.c.password])

for row in rs:
    print(row.name, 'is', row.age, 'years old')
"""
