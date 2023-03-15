# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 14:14:23 2021

@author: azarm
"""

import dash
#import dash_auth
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import dash_leaflet as dl
import pandas as pd
import numpy as np

#-----------------app authentification----------------------------------------
image8="/assets/Capture.jpg"
app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.3"}])
server = app.server

epicentre_options = [ {"label": 'Épicentre '+str(i), "value": str(i)}
                      for i in range(1,21) ]
params_sqlalchemy1= "postgresql+psycopg2://%s:%s@%s:5432/%s" % ("postgres",
                                                      "Gres!1978",
                                                      "localhost",
                                                      "quebec2")

engine1= create_engine(params_sqlalchemy1)
#-----------------------------card question-----------------------------------
cardquest = dbc.Card([dbc.CardHeader(html.H3("Sélection du scénario"), className="text-white"),
                     dbc.CardBody([
                             html.H4("Choisir épicentres", className="card-title text-white"),
                             dcc.Dropdown(
                                id="select_epicentre",
                                options=epicentre_options,
                                multi=False,
                                value='1',
                                className="dcc_control",
                            ),
                            html.H4("Choisir magnitudes", className="card-title text-white mt-5"), 
                            dcc.Dropdown(
                                id="select_magnitude",
                                options=[
                                    {"label": "Magnitude 5 ", "value": "5"},
                                    {"label": "Magnitude 6", "value": "6"},
                                    {"label": "Magnitude 7", "value": "7"},
                                ],multi=False,
                                value='5',
                                className="dcc_control")
                            
                        ])
                        ],
                    
                     color="primary")
#-------------------------------card median-----------------------------------
get_info=[html.H4("Légende")]+ [html.Img(srcSet=image8, height="180px")]

info = html.Div(children=get_info, id="info", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})

app.layout = html.Div([
        dbc.Row([dbc.Col(cardquest, width= 3),dbc.Col(dbc.Card([dbc.CardHeader(html.H3("Scénario pour le niveau d'aléa médian"), className="text-white"),
                     dbc.CardBody(html.Div([
                             dl.Map(children=[dl.TileLayer(), 
#                     dl.LayerGroup(circle), dl.LayerGroup(epi), 
                                     info, html.Div(dl.LayersControl(id="my-output")) 
                                     ],
                                     style={'width': "100%", 'height': "100%"}, center=[46.85, -71.3], zoom=11, id="map1"),
                                     ], style={'width': '963px', 'height': '700px'})
                                     ) ], color="primary")
                                     , width=8)
                    ], style={"marginTop": 100})]) 


@app.callback(
                 Output(component_id='my-output', component_property='children'), #   Output('histo1', 'figure'),Output("perte_médian", "children")
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_median(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------
        #---------------------------------SQL------------------------
#connection sql
        params_sqlalchemy1= "postgresql+psycopg2://%s:%s@%s:5432/%s" % ("postgres",
                                                      "Gres!1978",
                                                      "localhost",
                                                      "quebec2")

        engine1= create_engine(params_sqlalchemy1)

        file_name = 'epi'+selected_epicenter+'_M'+selected_magnitude+'_med'


        df = pd.read_sql_table(file_name, engine1)

        #---------------------------------legend------------------------


#---------------------------------color------------------------
        col = []
        for row in df['Damage_State']:
                if row=="Aucun" :    col.append('blue')
                elif row=="Leger":   col.append('green')
                elif row=="Modere":  col.append('yellow')
                elif row=="Etendu":  col.append('orange')
                elif row=="Complet":  col.append('red')
        
        df["col"]= col        

        lats = df.lat
        lons = df.long
        cl = df.Classe_Sismique
        
        Ins_pri=list(df["Inspection_Priority"])
        temp=list(df["Damage_State"])
        mdf=list(df["MRD_pour"])
        p_r=list(df["Priority_Rank"])
        St_dev=list(df["St_Dev_DR"])
        
        remp=np.round(np.array(df["Replacement_cost"])/1000)
        Loss=np.round(np.array(df["Economic_Loss"])/1000)

        pga=list(df["PGA"])
        fpga=list(df["F_PGA"])
        fiches=list(df["fiches2"]) 

        df = pd.DataFrame(columns=["lat", "lon", "cla", "col","ip","tp","mdf","pr","st","rmp","ls","pga","fpga", "fi"], data=np.column_stack((lats, lons, cl, col, Ins_pri,temp,mdf,p_r,St_dev,remp,Loss,pga,fpga,fiches)))
        df["chemin"]=df["col"]

        for i in range(0,len(df.chemin)):
            if df.fi[i] !=0:
                df["chemin"][i]='/assets/inventaire_structure/' +str(df.fi[i])+'.JPG'
            else:
                df["chemin"][i]=='/assets/inventaire_structure/' +str(df.fi[i])+'.jpg'

# Create markers from data frame.


        circle = [dl.Circle(center=[row["lat"], row["lon"]],radius=200, color=row["col"],children=[
            dl.Tooltip("Ponts"),
            dl.Popup([
                html.Img(src=row["chemin"], height="400px"),
                html.H5("Caractéristiques reliées au sol" ,className= "text-center  font-weight-bold" ),
                html.H6("Accélération maximale au sol: " + str(row["pga"]),className= "text-center" ),
                html.H6("Coefficient d'AMS: " + str(row["fpga"]),className= "text-center" ),
                html.H6("Classe sismique: " + row["cla"],className= "text-center" ),
                html.H5("Caractéristiques reliées aux ponts sous sollicitations",className= "text-center  font-weight-bold" ),
                html.H6("État de dommage: " + row["tp"],className= "text-center" ),
                html.H6("Priorité d'inspection: " + row["ip"],className= "text-center" ),
                html.H6("Ordre de priorité: " + str(row["pr"]),className= "text-center" ),
                html.H6("MDF: " + str(row["mdf"]),className= "text-center" ),
                html.H6("Écart-type: " + str(row["st"]), className= "text-center"),
                html.H6("Perte économique: " + str(row["ls"])+" k$",className= "text-center" ),
                html.H6("Coût de remplacement: " + str(row["rmp"])+" k$", className= "text-center"),
#               
                
                
            ], maxWidth="300px", autoPan=False)]) for i, row in df.iterrows()]



#create epicenter
        df2 = pd.read_sql_table('epicentre', engine1)
        lat=df2.at[float(selected_epicenter)-1,'lat']
        long=df2.at[float(selected_epicenter)-1,'long']

        epi=dl.Marker(position=[lat, long], icon={
                "iconUrl": "/assets/epicentre.png",
                "iconSize": [50, 50],
                "iconAnchor": [20, 36]
            }, children=[
                dl.Tooltip("épicentre")])


        epiover=dl.Overlay(dl.LayerGroup(epi), name="épicentre", checked=True)
        circleover=dl.Overlay(dl.LayerGroup(circle), name="ponts", checked=True)
        a=[epiover,circleover]

    return  a

                                     
#--------------final-------------------------------------------
            
if __name__ == "__main__":
    app.run_server(debug=False)