#%%
# Import external packages

from multiprocessing.connection import wait
import pandas as pd
from datetime import datetime
import numpy as np
import re


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
        self.temp = self.subject_data["Temp (C)"]
        self.max_temp = self.temp.max()
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        self.max_blood_flow = self.blood_flow.max()
        print('Subject ' + self.subject_id + ' initialized')



        

### Aufgabe 2: Datenverarbeitung ###






def calculate_CMA(df,n):
    pass
    

def calculate_SMA(df,n):
    pass
# %%


list_of_subjects = []
subj_numbers = []
number_of_subjects = 0

folder_current = os.path.dirname(__file__) 
print(folder_current)
folder_input_data = os.path.join(folder_current, "input_data")
for file in os.listdir(folder_input_data):
    
    if file.endswith(".csv"):
        number_of_subjects += 1
        file_name = os.path.join(folder_input_data, file)
        print(file_name)
        list_of_subjects.append(Subject(file_name))
# %%
