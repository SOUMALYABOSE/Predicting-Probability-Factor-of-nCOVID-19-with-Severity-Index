import pandas as pd
import numpy as np


import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import math
import random

test_data=pd.read_csv("C:\\Users\\Ankush\\Desktop\\covid\\Data\\Test\\Test dataset for positivity factor calculation.csv",delimiter=',',index_col=0)
test_data=test_data.dropna(subset=['Country'])

global_fact=pd.read_csv("C:\\Users\\Ankush\\Desktop\\covid\\Data\\Test\\global.csv",delimiter=',',index_col=1)
local_fact=pd.read_csv("C:\\Users\\Ankush\\Desktop\\covid\\Data\\Test\\local.csv",delimiter=',',index_col=0)
country_fact=pd.read_csv("C:\\Users\\Ankush\\Desktop\\covid\\Data\\Test\\AllAffectedNations.csv",encoding = 'unicode_escape',delimiter=',',index_col=1)
country_fact=country_fact[['Nationality Factor = Tot case/Popu']]
#print(country_fact)

total_factor=[]
def symptom_check(disease):
    if 'fever' in disease:
        return 'fever'
    if 'cough' in disease:
        return 'cough'
    if 'pneumonitis' in disease:
        return 'severe pneumonia'
    if 'breath' in disease:
        return 'difficulty breathing'
    else:
        return disease
stop_words = set(stopwords.words("english"))


symptoms=np.array(test_data[['Symptoms']])
country=np.array(test_data[['Country']])
travel=test_data[['Travel_country']].fillna('ss')
#print(travel)
for i in range(0,len(symptoms)):
    str_="".join(symptoms[i])
    count="".join(country[i])
    cumulf=0
    travf=0
    #checking if valid country
    if "".join(travel.iloc[i]) is 'ss':
        travf=0
    else:
        trav="".join(travel.iloc[i])
        travf=country_fact.ix[trav,'Nationality Factor = Tot case/Popu']+country_fact.ix['World','Nationality Factor = Tot case/Popu']
    words=str_.split(",")
    for wd in words:
        totalf=0
        word1=wd.split(";")
        for wd1 in word1:
            wx=wd1.split(":")
            for wwx in wx:
                word2=wwx.split("and")
                for wd2 in word2:
                    word3=wd2.split("with")
                    for wd3 in word3:
                        wd3=wd3.strip()
                        wd3=wd3.lower()
                        wd3=symptom_check(wd3)
                        if wd3 in stop_words:
                            continue
                        if wd3 in string.punctuation:
                            continue
                        if wd3 is ',':
                            continue
                        else:
                            #print("disease: "+wd3+" country: "+count)
                            globalf=global_fact.ix[wd3,'global_factor']
                            if count not in local_fact.index:
                                localf=globalf #if country information is not available
                            else:
                                localf=local_fact.ix[count,wd3]
                            
                            totalf=localf+globalf
                            duration=random.randrange(1,6)/10+1
                            totalf=totalf*duration
                            cumulf+=totalf
                            #print(localf,globalf,totalf)

    #print(travf)
    #print(cumulf)
    var=2*travf+6.5*cumulf+1.5*(random.randrange(5,8)/100)
    total_factor.append(var)
    print(i," total factor: ",var)


test_data['total factor']=total_factor
test_data.to_csv('test_result.csv')
