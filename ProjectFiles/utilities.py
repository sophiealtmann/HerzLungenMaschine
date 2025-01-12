#%%
# Import external packages

from multiprocessing.connection import wait
import pandas as pd
from datetime import datetime
import numpy as np
import re
import os

# Classes 

class Subject():
    def __init__(self, file_name):

        ### Aufgabe 1: Interpolation ###

        __f = open(file_name)
        self.subject_data = pd.read_csv(__f)
        self.subject_data = self.subject_data.interpolate(method='quadratic', axis=0)
        __splited_id = re.findall(r'\d+',file_name)      
        self.subject_id = ''.join(__splited_id)
        self.names = self.subject_data.columns.values.tolist()
        self.time = self.subject_data["Time (s)"] 
        self.spO2 = self.subject_data["SpO2 (%)"]
        self.max_spO2 =  self.spO2.max() 
        self.idxmax_spO2 = self.subject_data["SpO2 (%)"].idxmax()
        self.temp = self.subject_data["Temp (C)"]
        self.max_temp = self.temp.max()
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        self.max_blood_flow = self.blood_flow.max()
        self.minandmax = self.subject_data["SpO2 (%)"].agg(['min','idxmin','max','idxmax'])
        
        print('Subject ' + self.subject_id + ' initialized')

        

### Aufgabe 2: Datenverarbeitung ###

def calculate_CMA(df):
    bloodflow = df["Blood Flow (ml/s)"].to_frame()
    bloodflow['CMA'] = bloodflow["Blood Flow (ml/s)"].expanding().mean()
    
    return bloodflow
    

def calculate_SMA(df,n):
    bloodflow = df["Blood Flow (ml/s)"].to_frame()
    bloodflow['SMA'] = bloodflow["Blood Flow (ml/s)"].rolling(n).mean()

    return bloodflow

def calculate_mean(df):
    mean=df["Blood Flow (ml/s)"].mean()
    
    return mean

# SMA ist sinnvoll bei Signalen die mit der Zeit zusammenhängen. 
# Weiters ist er bei Signalen sinnvoll, bei denen häufig unerwünschte Ausreißer vorkommen.
# Er ist ungeeignet, wennn es darum geht ein Signal detailreich aufzuzeichnen.
# Weiters ist er ungeeignet, wenn Lücken im Datensatz vorhanden sind, da diese die Werte verfälschen.
    
# Der Wert n gibt das Datenfenster an, über das der Moving Average berechnet wird.
# Die Kurve verliert an Details, je höher der Wert für n ist.
# %%


# %%
