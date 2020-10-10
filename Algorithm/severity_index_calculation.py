import pandas as pd
import numpy as np

import string
import math
import random
from matplotlib import pyplot as plt

data=pd.read_csv("C:\\Users\\Ankush\\Desktop\\ML Assignment\\arko\\Data for severity calculation.csv",delimiter=',',index_col=0).fillna('not')
comor_data=pd.read_csv("C:\\Users\\Ankush\\Desktop\\ML Assignment\\arko\\comorbidity_factor.csv",delimiter=',',index_col=0).fillna('not')
treat_data=pd.read_csv("C:\\Users\\Ankush\\Desktop\\ML Assignment\\arko\\Treatment.csv",delimiter=',',index_col=0).fillna('not')
severity_val=[]
def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))
def modify_treat(treat)->int:
    if treat=='not':
        return 0
    val=0
    tr=treat.split("+")
    for trs in tr:
        trs=trs.strip()
        if trs=='Azi':
            trs='Azithromycin'
        val=val+pow(2,int(treat_data.ix[trs,'value'])-1)
                    
    return val
def mod_age(age):
    aged=int(age)
    if age<=20:
        return 9
    elif age>20 and age<=40:
        return 41
    elif age>40 and age<=60:
        return 33
    else:
        return 17
def modify_comor(comor):
    if comor=='not':
        return 0
    val=0
    como=comor.split("+")
    for cms in como:
        cms=cms.strip()
        val=val+comor_data.ix[cms,'value']

    return val

def modify_symp(symptoms):
    if symptoms=='not':
        return 0
    val=0
    symp_dict=dict({'Fever':0.5250852411105699,'Breathlessness':0.021919142717973697,'Cough':0.28981977593765224})
    symp=symptoms.split("+")
    for syms in symp:
        syms=syms.strip()
        val=val+symp_dict.get(syms)*2

    return val
def symp_count(symptoms):
    if symptoms=='not':
        return 0
    val=0
    symp=symptoms.split("+")
    for syms in symp:
        val=val+1

    return val
def modify_spo(spo):
    if spo=='not':
        return 0
    sp=spo.split("%")
    for sps in sp:
        sps=sps.strip()
        sps=int(sps)
        return abs(sps-97)
def actual_spo(spo):
    if spo=='not':
        return 97
    sp=spo.split("%")
    for sps in sp:
        sps=sps.strip()
        sps=int(sps)
        return sps


for i in range(1,len(data)+1):
    if data.ix[i,'Gender'] == 'Male':
        data.ix[i,'Gender']=4.7
    else:
        data.ix[i,'Gender']=2.8

    if data.ix[i,'Duration of Symptoms Before Hospitalisation'] == '1 to 3 days':
        data.ix[i,'Duration of Symptoms Before Hospitalisation']=2
    elif data.ix[i,'Duration of Symptoms Before Hospitalisation'] == '3 to 5 days':
        data.ix[i,'Duration of Symptoms Before Hospitalisation']=4
        
    elif data.ix[i,'Duration of Symptoms Before Hospitalisation'] == 'More than 5 days':
        data.ix[i,'Duration of Symptoms Before Hospitalisation']=5.1
        
    else :
        data.ix[i,'Duration of Symptoms Before Hospitalisation']=1

    if data.ix[i,'Interval between day of admission and patient put on ventilator']=='Within 24 hours':
       data.ix[i,'Interval between day of admission and patient put on ventilator']=1
    else:
        data.ix[i,'Interval between day of admission and patient put on ventilator']=0

    data.ix[i,'Age']=mod_age(data.ix[i,'Age'])
    spo2=actual_spo(data.ix[i,'SpO2 at time of admission'])
    data.ix[i,'SpO2 at time of admission']=modify_spo(data.ix[i,'SpO2 at time of admission'])
    data.ix[i,'Treatment Given']=modify_treat(data.ix[i,'Treatment Given'])
    data.ix[i,'Co-morbidity Status']=modify_comor(data.ix[i,'Co-morbidity Status'])
    
    symp=symp_count(data.ix[i,'Symptoms present at the time of admission'])
    data.ix[i,'Symptoms present at the time of admission']=modify_symp(data.ix[i,'Symptoms present at the time of admission'])

    sev=(data.ix[i,'Symptoms present at the time of admission']*data.ix[i,'Duration of Symptoms Before Hospitalisation'])+data.ix[i,'Gender']+2*data.ix[i,'SpO2 at time of admission']+data.ix[i,'Age']+2*data.ix[i,'Co-morbidity Status']
    sev=sev*2.637711157
    #print(i+1,sev)
    severity_val.append(sev)
    plt.scatter(spo2,sev,color='b',marker='.',s=50)

data['Severity Value']=severity_val
data.to_csv('severity_cal.csv')
plt.xlabel('SpO2 level')
plt.ylabel('Severity_value')
plt.show()
               

