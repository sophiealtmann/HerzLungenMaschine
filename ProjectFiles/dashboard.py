
#%%
from cmath import nan
from ctypes.wintypes import tagSIZE
from tempfile import SpooledTemporaryFile
import dash
from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pytz import UTC
import utilities as ut
import numpy as np
import os
import re
from scipy.signal import find_peaks

app = Dash(__name__)

colors = {
    'background': ' #add8e6',
    'text': ' #00008B',
    "dropdown": "#30D5C8"
}

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
        list_of_subjects.append(ut.Subject(file_name))


df = list_of_subjects[0].subject_data


for i in range(number_of_subjects):
    subj_numbers.append(list_of_subjects[i].subject_id)

data_names = ["SpO2 (%)", "Blood Flow (ml/s)","Temp (C)"]
algorithm_names = ['min','max']
blood_flow_functions = ['CMA','SMA','Mittelwert','Show Limits']


fig0= go.Figure()
fig1= go.Figure()
fig2= go.Figure()
fig3= go.Figure()

fig0 = px.line(df, x="Time (s)", y = "SpO2 (%)")
fig1 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")
fig2 = px.line(df, x="Time (s)", y = "Temp (C)")
fig3 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")

app.layout = html.Div(children=[
    html.H1(children='Cardiopulmonary Bypass Dashboard', style={"textAlign" : "center", 'color': colors['text']}),

    html.Div( children='''
        Hier könnten Informationen zum Patienten stehen....
    '''),

    dcc.Checklist(style={'backgroundColor': colors['background']},
    id= 'checklist-algo',
    options=algorithm_names,
    inline=False
    ),

    html.Div([
        dcc.Dropdown(options = subj_numbers, placeholder='Select a subject', value='1', id='subject-dropdown', style={'backgroundColor': colors['dropdown']}),
    html.Div(id='dd-output-container')
    ],
        style={"width": "15%"}
    ),

    dcc.Graph(
        id='dash-graph0',
        figure=fig0
    ),

    dcc.Graph(
        id='dash-graph1',
        figure=fig1
    ),
    dcc.Graph(
        id='dash-graph2',
        figure=fig2
    ),

    dcc.Checklist(style={'backgroundColor': colors['background']},
        id= 'checklist-bloodflow',
        options=blood_flow_functions,
        inline=False
    ),
    dcc.Graph(
        id='dash-graph3',
        figure=fig3
    )
])
### Callback Functions ###
## Graph Update Callback
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph0', 'figure'),
    Output('dash-graph1', 'figure'),
    Output('dash-graph2', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-algo','value')
)
def update_figure(value, algorithm_checkmarks):
    print("Current Subject: ",value)
    print("current checked checkmarks are: ", algorithm_checkmarks)
    ts = list_of_subjects[int(value)-1].subject_data
    #SpO2
    fig0 = px.line(ts, x="Time (s)", y = data_names[0])
    # Blood Flow
    fig1 = px.line(ts, x="Time (s)", y = data_names[1])
    # Blood Temperature
    fig2 = px.line(ts, x="Time (s)", y = data_names[2])
    

    ### Aufgabe 2: Min / Max ###
    mmspO2= list_of_subjects[int(value)-1].subject_data["SpO2 (%)"].agg(['min','idxmin','max','idxmax'])
    mmblood_flow= list_of_subjects[int(value)-1].subject_data["Blood Flow (ml/s)"].agg(['min','idxmin','max','idxmax'])
    mmtemp= list_of_subjects[int(value)-1].subject_data["Temp (C)"].agg(['min','idxmin','max','idxmax'])
    
    
    # Max hinzugefügt
    if "max" in str(algorithm_checkmarks):
        fig0.add_trace(go.Scatter(x=[mmspO2[3]],y=[mmspO2[2]],marker_size=10, name = 'max'))
        fig1.add_trace(go.Scatter(x=[mmblood_flow[3]],y=[mmblood_flow[2]],marker_size=10, name = 'max'))
        fig2.add_trace(go.Scatter(x=[mmtemp[3]],y=[mmtemp[2]],marker_size=10, name = 'max'))
    
    # Min hinzugefügt
    if "min" in str(algorithm_checkmarks):
        fig0.add_trace(go.Scatter(x=[mmspO2[1]],y=[mmspO2[0]],marker_size=10, name = 'min'))
        fig1.add_trace(go.Scatter(x=[mmblood_flow[1]],y=[mmblood_flow[0]],marker_size=10, name = 'min'))
        fig2.add_trace(go.Scatter(x=[mmtemp[1]],y=[mmtemp[0]],marker_size=10, name = 'min'))
    
    return fig0, fig1, fig2 
 


## Blodflow Simple Moving Average Update
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph3', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-bloodflow','value')
)
def bloodflow_figure(value, bloodflow_checkmarks):
    
    ## Calculate Moving Average: Aufgabe 2
    print(bloodflow_checkmarks)
    bf = list_of_subjects[int(value)-1].subject_data
    fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s)")

    if 'SMA' in str(bloodflow_checkmarks):
        global bloodflow 
        bloodflow = ut.calculate_SMA(bf,3)
        fig3.add_trace(go.Line(y=bloodflow["SMA"],name="SMA"))
    
    if 'CMA' in str(bloodflow_checkmarks):
        bloodflow1 = ut.calculate_CMA(bf)
        fig3.add_trace(go.Line(y=bloodflow1["CMA"],name="CMA"))
    # Aufgabe 3 
    if 'Mittelwert' in str(bloodflow_checkmarks):
        global mean 
        mean = ut.calculate_mean(bf)
        fig3.add_hline(y=mean, line_dash="dot",annotation_text="Mittelwert: "+str(round(mean,2))+ " ml/s")

    if 'Show Limits' in str(bloodflow_checkmarks):
        mean = ut.calculate_mean(bf)
        fig3.add_hrect(y0=mean*1.15, y1=mean*0.85, annotation_text="15% Limit", fillcolor="green", opacity=0.25, line_width=0 )
    
    if 'SMA' in str(bloodflow_checkmarks):                                    
        sma=ut.calculate_SMA(bf,3)          # n=3 da so Ausreißer die kürzer als 3 sec sind geglättet werden.
        mean=ut.calculate_mean(bf)  
        high= mean*1.15
        low = mean*0.85
            
        high_and_low = sma[(sma['SMA'] > high) | (sma['SMA'] < low)] 
        legend = "ACHTUNG! Es wurden für " + str(high_and_low['SMA'].count()) +'s kritische Werte aufgezeichnet!'
        fig3.add_trace(go.Scatter(name = legend, y = high_and_low['SMA'], mode = "markers", marker_color='red'))

    return fig3



if __name__ == '__main__':
    app.run_server(debug=True)
# %%
