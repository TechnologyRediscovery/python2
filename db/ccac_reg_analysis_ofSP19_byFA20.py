#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Pandas introduction using a flat file of all registrations for courses at CCAC during
# spring 2019:
# What programs are home to students whose mid-term grades are, on average, lower than 
# other? Are mid-term grades good predictors of final grades?
# How likely is a C or lower at MT to lead to a withdraw or F?

import pandas as pd
import numpy as np
import matplotlib as plt
# Special magic function for enabling pyplot charts in jupyter
get_ipython().run_line_magic('matplotlib', 'inline')

# read in the CSV, it's pretty to start with, so that's easy
stud_records = pd.read_csv('19sp_gradestud_only_clean.csv')
stud_records.dtypes
# get just the department column (indexes always come with a Series) in a DF
stud_records.dtypes
# stud_records


# In[ ]:


# Get unique value counts
stud_records['Department'].value_counts()
degs = stud_records['DegreeType'].value_counts()
print(degs)
# verify that I got a series object out of our data frame when I select only one Column
type(degs)
l = degs.to_list()
# standard python built-in objects
for val in l:
    print(val)


# In[ ]:


# Generator function for our primary key on data insert
appt_pk = 100
def getPK_appt():
    appt_pk += 1
    yield appt_pk


# In[ ]:


print(getPK_appt())
print(getPK_appt())
print(getPK_appt())


# ## Appointment data
# <!-- Read in the CSV of appointment data into a sqlite database for retrieval and keying to related table -->

# In[ ]:


import sqlite3

try:
#     Create our databsae via a connection (makes it if not exists)
    conn = sqlite3.connect('ccacregdb')
    # From our connection, get a cursor object
    # Use cursor to inject SQL of any kind, and make SELECT queries and 
    # Cursor will give us result set
    cursor = conn.cursor()
    print("Connected")
    appttable_sql='''
                    CREATE TABLE IF NOT EXISTS
                        appts(
                            apptid INTEGER PRIMARY KEY,
                            stud INTEGER NOT NULL,
                            service TEXT NOT NULL,
                            apptdate TEXT NOT NULL,
                            missedappt INTEGER NOT N
                            ULL
                        )
        
                '''
    cursor.execute(appttable_sql)
    conn.commit()
    print("Created APPTS table")
    
    
    
except sqlite3.Error as error:
    print("Error")
    print(error)
# Always close up our resources
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    


# In[ ]:


def close_DB_resources(dbconn, cursor):
    try:
        if dbconn:
            dbconn.close()
        if cursor:
            cursor.close()
        print("closed resources")
    except sqlite3.Error as err:
        ("Error closing resources")


# In[ ]:


import sqlite3
# Utility for handling DB errors
def handle_DB_error(dbconn, cursor):
    if dbconn:
        try:
            dbconn.rollback()
            print("Rolled back transation")
        except sqlite3.Error as error:
            print("Error rolling back transaction")
        finally:
            close_DB_resources(dbconn, cursor)
            dbconn = None
            return dbconn
            


# In[ ]:


# utility DB connection and cursor function to return our access objects
def connect_SQLite():
    try:
        dbconn = sqlite3.connect('ccacregdb')
        cursor = dbconn.cursor()
        print("Connected to ccacregdb")
    except sqlite3.Error as error:
        print("Error opening database")
        dbconn = handle_DB_error(dbconn, cursor)
    return dbconn, cursor
        
        


# In[ ]:


import csv
# SQL setup for inserts
pkid = 101
appts_insert = '''INSERT INTO appts (apptid, stud, service, apptdate, missedappt)
                    VALUES (?,?,?,?,?);
                '''
# retrieve my connection and cursor for use in all my inserts
dbconn, cursor = connect_SQLite()
# Iterate over our CSV file of appointments, convert the missedappt to 0/1
with open('appointments_1000.csv') as file:
    appointments = csv.DictReader(file)
    for appt in appointments:
        # get rowid from generator
        pkid += 1
        # make an integer val reflect missed appt
        missedappt = 0
        if appt['MissedAppointment']=='Y':
            missedappt = 1
        record = (pkid, appt['ExternalID'], appt['ServiceName'], appt['AppointmentDate'], missedappt)
        print("inserting tupple: ", end='')
        print(record)
        cursor.execute(appts_insert, record)
        dbconn.commit()
close_DB_resources(dbconn, cursor)


# In[ ]:


# Verify that we've got data

select_sql = '''
                SELECT *
                    FROM appts
                    WHERE missedappt = 1;
            '''
dbconn, cursor = connect_SQLite()
cursor.execute(select_sql)
recs = cursor.fetchall()
for r in recs:
    print(r)

close_DB_resources(dbconn, cursor)


# In[22]:


# Create our table for student registration data

reg_table_sql= '''CREATE TABLE IF NOT EXISTS reg(
                    regid INTEGER PRIMARY KEY,
                    externalid INTEGER,
                    term TEXT,
                    sectionid TEXT,
                    currentregistrationstatus TEXT,
                    currentregistrationstatusdesc TEXT,
                    sectioncredits INTEGER,
                    sectionsubject TEXT,
                    currentstudentprogram TEXT,
                    degreetype TEXT,
                    locationtype TEXT,
                    department TEXT,
                    metamajor TEXT,
                    finalgrade TEXT,
                    midtermgrade TEXT,
                    graduated INTEGER,
                    creditstart INTEGER );

                '''
dbconn, cursor = connect_SQLite()
cursor.execute(reg_table_sql)
dbconn.commit()
close_DB_resources(dbconn, cursor)


# In[24]:


class _TimesCalled: 
    def __init__(self): 
        self._called = 0 
    def __add__(self, other): 
        self._called = self._called + other 
        return self._called
    def __str__(self):
        return str(self._called)
times_called = _TimesCalled() 
def increment(): 
    return times_called + 1 


# In[46]:


# read in our mongo table of registrations from sp19
import csv

# SQL setup for inserts
pkid = 1000
reg_insert = '''INSERT INTO reg (
                    regid,
                    externalid,
                    term,
                    sectionid,
                    currentregistrationstatus,
                    currentregistrationstatusdesc,
                    sectioncredits,
                    sectionsubject,
                    currentstudentprogram,
                    degreetype,
                    locationtype,
                    department,
                    metamajor,
                    finalgrade,
                    midtermgrade,
                    graduated,
                    creditstart)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
# retrieve my connection and cursor for use in all my inserts
dbconn, cursor = connect_SQLite()

# Iterate over our CSV file of appointments, convert the missedappt to 0/1
with open('19sp_gradestud_only_clean.csv') as file:
    regs = csv.DictReader(file)
    for r in regs:
        # get rowid from generator
        pkid += 1
        # make an integer val reflect missed appt
        grad = 0
        if r['Graduated']=='Yes':
            grad = 1
        record = (pkid, r['ExternalID'],r['Term'],r['SectionID'],r['CurrentRegistrationStatus'],r['CurrentRegistrationStatusDesc'],r['SectionCredits'],r['SectionSubject'],r['CurrentStudentProgram'],r['DegreeType'],r['LocationType'],r['Department'],r['MetaMajor'],r['FinalGrade'],r['MidTermGrade'],grad,r['creditStart'])
        print(record)
        cursor.execute(reg_insert, record)
        dbconn.commit()
close_DB_resources(dbconn, cursor)


# In[45]:


dbconn, cursor = connect_SQLite()
close_DB_resources(dbconn, cursor)


# In[ ]:


# Slice the dataframe to only show rows with ID 56400 through 56408
stud_records.iloc[56400:56408]
recs = stud_records

# Make me a data frame of all records of student registrations in online sections
# our lambda function will be applied to each value in "LocationType column"
# and ask "Is Your Value in this list?". The resulting t/f value is used to 
# by the loc function to choose which rows to "locate" and include in our resulting frame
cyber = recs.loc[lambda recs: recs['LocationType'].isin(['Online',])]
print("Cyber: ", len(cyber))
onsite = recs.loc[lambda recs: recs['LocationType'].isin(['On-site',])]
print("OnSite ", len(onsite))


# In[ ]:


# Visualize the shape of the cred_start variable for each of our sub-groups
plt.pyplot.hist(cyber['creditStart'])
plt.pyplot.hist(onsite['creditStart'])


# In[ ]:


pd.set_option('display.max_rows', None)
appts = pd.read_csv('appointments_1000.csv')
length(appts)


# In[ ]:



# appts.dtypes
# reg_appts = pd.concat([stud_records, appts], axis=1, sort=False)
reg_appts = pd.merge(stud_records, appts, on='ExternalID', how='outer')
reg_apptsd.

