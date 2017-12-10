#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 12:31:35 2017

@content: Explorys Most Interesting Patient
@author: yuchenli
"""

import pandas as pd

admission = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/admission",
                        dtype = str)
            
demographic = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/demographic",
                          dtype = str)    

medical_history = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/medical_history",
                              dtype = str)

observation = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/observation.csv",
                          dtype = str)

surgical_history = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/surgical_history",
                               dtype = str)

# Exploratory Analysis
## Admission
admission['std_discharge_disposition'].value_counts()
admission['std_admission_type'].value_counts()

## Add "Standard Discharge Disposition" 
Definition = []
for i in range(len(admission)):
    if (admission.iloc[i,7] == '306689006'):
        Definition.append('Discharge to home (procedure)')
    elif (admission.iloc[i,7] == '429202003'):
        Definition.append('Transfer of care to hospital (procedure)')
    elif (admission.iloc[i,7]== '429202003'):
        Definition.append('Patient transfer to skilled nursing facility (procedure)')
    elif (admission.iloc[i,7] == '306689006'):
        Definition.append('Discharge to establishment (procedure)')
    elif (admission.iloc[i,7] == '416237000'):
        Definition.append('nan')
    else:
        Definition.append('nan')
        
admission['Definition'] = Definition
    
## Surgical and medical history
   
## Observation
test_name = pd.DataFrame(observation['long_common_name'].value_counts())
#test_name.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/observation_1.csv', sep = ',', encoding = 'utf-8')
observation['std_value_status'].value_counts()
observation_1 = observation[['observation_date', 'long_common_name', 'std_value', 'std_value_txt', 'std_value_status', 'observation_high_ref', 'observation_low_ref', 'std_uom', ]]
value_status = {'0':'Unknown',
                '1':'Normal',
                '2':'Abnormal',
                '4':'Low',
                '8':'High', 
                '16':'Panic',
                '32':'Positive', 
                '64':'Negative', 
                '128':'Off-scale'}

for i in range(len(observation_1)):
    try:
        observation_1.set_value(i,'std_value_status', value_status[observation_1.iloc[i,4]])
    except KeyError:
        observation_1.set_value(i,'std_value_status', 'nan')
        
def test_name(column, test_name):
    return observation_1.loc[observation_1[str(column)] == test_name]

observation_calcium = test_name('long_common_name', 'Calcium [Mass/volume] in Blood')
observation_BMI = test_name('long_common_name', 'Body mass index (BMI) [Ratio]')
observation_height = test_name('long_common_name', 'Body height')
observation_hematocrit = test_name('long_common_name', 'Hematocrit [Volume Fraction] of Blood')
observation_bacteria = test_name('long_common_name', 'Bacteria identified in Urine by Culture')
observation_heart = test_name('long_common_name', 'Heart rate')
observation_respiratory = test_name('long_common_name', 'Respiratory rate')
observation_pressure = test_name('long_common_name', 'Systolic blood pressure')
observation_pressure_dia = test_name('long_common_name', 'Diastolic blood pressure')
observation_oxygen = test_name('long_common_name','Fractional oxyhemoglobin in Blood')

observation_abnormal = test_name('std_value_status', 'Abnormal')

## Observation_abnormal
import datetime as dt
observation_abnormal.loc[:,'observation_date'] = pd.to_datetime(observation_abnormal.loc[:,'observation_date'])
observation_abnormal.loc[:,'observation_date'] = observation_abnormal.loc[:,'observation_date'].apply(lambda x: dt.datetime.strftime(x, '%m/%Y'))
abnormal = pd.DataFrame(observation_abnormal.loc[:,'observation_date'].value_counts())
       
## Plot heart rate
import numpy as np
observation_heart.loc[:,'observation_date'] = pd.to_datetime(observation_heart.loc[:,'observation_date'])
observation_heart.loc[:,'observation_date'] = observation_heart.loc[:,'observation_date'].apply(lambda x: dt.datetime.strftime(x, '%m/%d/%Y'))
import csv
"""
with open("/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/heart_range.csv", "w") as csvfile:
    fieldnames = ['Date', "High", "Low"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    date_set = set(observation_heart['observation_date'])
    for i in date_set:
        date_set_df = observation_heart[observation_heart['observation_date'] == i]
        daily_heart_rate = list(map(float, date_set_df.std_value))       
        writer.writerow({'Date': i, "High": np.nanmax(daily_heart_rate), "Low": np.nanmin(daily_heart_rate)})
"""       
## Respiratory rate
observation_respiratory.loc[:,'observation_date'] = pd.to_datetime(observation_respiratory.loc[:,'observation_date'])

## Blood pressure
observation_pressure.loc[:,'observation_date'] = pd.to_datetime(observation_pressure.loc[:,'observation_date'])
observation_pressure.loc[:,'observation_date'] = observation_pressure.loc[:,'observation_date'].apply(lambda x: dt.datetime.strftime(x, '%m/%d/%Y'))

observation_pressure.loc[:,'observation_date'] = pd.to_datetime(observation_pressure_dia.loc[:,'observation_date'])
observation_pressure_dia.loc[:,'observation_date'] = observation_pressure_dia.loc[:,'observation_date'].apply(lambda x: dt.datetime.strftime(x, '%m/%d/%Y'))

with open("/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/blood_pressure_range.csv", "w") as csvfile:
    fieldnames = ['Date', "High", "Low"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    date_set_sys = set(observation_pressure['observation_date'])
    date_set_dia = set(observation_pressure_dia['observation_date'])
    date_set = date_set_sys|date_set_dia
    for i in date_set:
        date_set_df_sys = observation_pressure[observation_pressure['observation_date'] == i]
        date_set_df_dia = observation_pressure_dia[observation_pressure_dia['observation_date'] == i]

        daily_heart_rate = list(map(float, date_set_df_sys.std_value)) + list(map(float, date_set_df_dia.std_value))      
        writer.writerow({'Date': i, "High": np.nanmax(daily_heart_rate), "Low": np.nanmin(daily_heart_rate)})


## Write to csv
abnormal.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/abnormal.csv', sep = ',', encoding = 'utf-8')
observation_heart.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/heart_rate.csv', sep = ',', encoding = 'utf-8', index = 0)
observation_respiratory.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/respiratory.csv', sep = ',', encoding = 'utf-8', index = 0)
observation_pressure.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/systolic.csv', sep = ',', encoding = 'utf-8', index = 0)
observation_pressure_dia.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/Explorys_interesting_patient/Data/diastolic.csv', sep = ',', encoding = 'utf-8', index = 0)
