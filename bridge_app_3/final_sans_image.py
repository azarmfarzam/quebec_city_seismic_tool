# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:37:27 2021

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
#from Authentification import Code_auth

#-----------------app authentification----------------------------------------

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.3"}])
server = app.server

#----------------------Create controls-----------------------------------------

epicentre_options = [ {"label": 'Épicentre '+str(i), "value": str(i)}
                      for i in range(1,21) ]

image= "https://en.clubnaova.ca/static/media/ets.90e12cca.png"

image2= "/assets/ecart.jpg"

image3="/assets/classe.jpg"

image8="/assets/Capture.jpg"

legendepi1="/assets/legendepi1.jpg"

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
#-------------------------------legend cartes dommages-------------------------
get_info=[html.H4("Légende")]+ [html.Img(srcSet=legendepi1, height="60px")]

info = html.Div(children=get_info, id="info", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
#-------------------------card epicenter--------------------------------------
cardepi = dbc.Card([dbc.CardHeader(html.H3("Emplacement des épicentres"), className="text-white"),
                     dbc.CardBody(html.Div([
                             dl.Map(children=[dl.TileLayer(), 
#                     dl.LayerGroup(circle), dl.LayerGroup(epi), 
                                     info, html.Div(dl.LayersControl(id="my-output0")) 
                                     ],
                                     style={'width': "100%", 'height': "100%"}, center=[46.81, -71.3], zoom=11, id="map0"),
                                     ], style={'width': '1090px', 'height': '700px'})
                                ),
                             
                            ], color="primary")

#-------------------------------legend cartes dommages-------------------------
get_info=[html.H4("Légende")]+ [html.Img(srcSet=image8, height="180px")]

info1 = html.Div(children=get_info, id="info1", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
#-------------------------------card median-----------------------------------
cardmedian= dbc.Card([dbc.CardHeader(html.H3("Scénario pour le niveau d'aléa médian"), className="text-white"),
                     dbc.CardBody(html.Div([
                             dl.Map(children=[dl.TileLayer(), 
#                     dl.LayerGroup(circle), dl.LayerGroup(epi), 
                                     info1, html.Div(dl.LayersControl(id="my-output")) 
                                     ],
                                     style={'width': "100%", 'height': "100%"}, center=[46.83, -71.3], zoom=11, id="map1"),
                                     ], style={'width': '963px', 'height': '700px'})
                                     ) ], color="primary")

#-------------------------------legend cartes dommages-------------------------
get_info=[html.H4("Légende")]+ [html.Img(srcSet=image8, height="180px")]

info2 = html.Div(children=get_info, id="info2", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
#--------------------------------card low-------------------------------------
cardlow= dbc.Card([dbc.CardHeader(html.H3("Scénario pour le niveau d'aléa bas"), className="text-white"),
                     dbc.CardBody(html.Div([
                             dl.Map(children=[dl.TileLayer(), 
#                     dl.LayerGroup(circle), dl.LayerGroup(epi), 
                                     info2, html.Div(dl.LayersControl(id="my-output2")) 
                                     ],
                                     style={'width': "100%", 'height': "100%"}, center=[46.83, -71.3], zoom=11, id="map2"),
                                     ], style={'width': '963px', 'height': '700px'}))
                             ], color="primary")         

#-------------------------------legend cartes dommages-------------------------
get_info=[html.H4("Légende")]+ [html.Img(srcSet=image8, height="180px")]

info3 = html.Div(children=get_info, id="info3", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
#--------------------------------card high-------------------------------------
cardhigh= dbc.Card([dbc.CardHeader(html.H3("Scénario pour le niveau d'aléa élevé"), className="text-white"),
                     dbc.CardBody(html.Div([
                             dl.Map(children=[dl.TileLayer(), 
#                     dl.LayerGroup(circle), dl.LayerGroup(epi), 
                                     info3, html.Div(dl.LayersControl(id="my-output3")) 
                                     ],
                                     style={'width': "100%", 'height': "100%"}, center=[46.83, -71.3], zoom=11, id="map3"),
                                     ], style={'width': '963px', 'height': '700px'}))
                             ], color="primary")           
#-------------------------------histogramm median-----------------------------
cardhism= dbc.Card([dbc.CardHeader(html.H3("Bilan du scénario d'aléa médian"), className="text-white"),
                        dbc.CardBody([html.Div([html.H4(id="perte_médian")],
                                        id="perte-med",className="text-white")],style={"marginTop": 20}),
                                      dcc.Graph(id="histo1")
        
        ], body=True, color="primary")  


#-------------------------------histogramm low-----------------------------
cardhisl= dbc.Card([dbc.CardHeader(html.H3("Bilan du scénario d'aléa bas"), className="text-white"),
                        dbc.CardBody([html.Div([html.H4(id="perte_faible")],
                                        id="perte-faib",className="text-white")],style={"marginTop": 20}),
                                      dcc.Graph(id="histo2")
        
        ], body=True, color="primary")  

#-------------------------------histogramm high-----------------------------
cardhish= dbc.Card([dbc.CardHeader(html.H3("Bilan du scénario d'aléa élevé"), className="text-white"),
                        dbc.CardBody([html.Div([html.H4(id="perte_élévé")],
                                        id="perte-élév",className="text-white")],style={"marginTop": 20}),
                                      dcc.Graph(id="histo3")
        
        ], body=True, color="primary")  
#-----------------------------------modal etats de dommage--------------------
image4="/assets/leger.jpg"
image5="/assets/modere.jpg"
image6="/assets/etendu.jpg"
image7="/assets/complet.jpg"

modetat=dbc.Modal(
                    [
                        dbc.ModalHeader("Description des états de dommage:"),
                        dbc.ModalBody(children=[
                                html.H5("État de dommage Léger (en vert):", className="text-center"), 
                                html.H6("Légères fissures et écaillages au niveau des culées et de joints de discontinuité des poutres, léger écaillage de la colonne et légères fissures au niveau du tablier.", className="text-center"),
                                html.Img(srcSet=image4, height="240px", style={"marginLeft": 310}),
                                html.H6("Image tirée de (https://intrans.iastate.edu/app/uploads/2019/11/MAPbriefNovember2016.pdf)", className="text-center"),
                                html.H5("État de dommage Modéré: (en jaune)", className="text-center"),
                                html.H6("Modéré: Petit affaissement des culées, dégradation des murs caches au niveau des culées, colonne avec une fissuration et écaillage modérés (sans rupture), une rupture des appareils d’appuis à pendule ou un tassement modéré de la dalle. ", className="text-center"),
                                html.Img(srcSet=image5, height="240px", style={"marginLeft": 450}),
                                html.H6("Image tirée de (Misra et al., 2018)", className="text-center"),
                                html.H5("État de dommage Étendu: (en orange)",  className="text-center"),
                                html.H6("Étendu: Dégradation des colonnes, rupture en cisaillement sans perte d'intégrité, tassement différentiel au niveau des connexions, rupture des murs caches des culées, translation verticale de la culée.", className="text-center"),
                                html.Img(srcSet=image6, height="240px", style={"marginLeft": 390}),
                                html.H6("Image tirée de (Misra et al., 2018)", className="text-center"),
                                html.H5("État de dommage Complet (en rouge):", className="text-center"),
                                html.H6("Déchaussement du tablier, rupture des piles, affaissement de la structure.", className="text-center"),
                                html.Img(srcSet=image7, height="240px", style={"marginLeft": 315}),
                                html.H6("Image tirée de Yashinsky et al. (2010)", className="text-center")]),
                                dbc.ModalFooter(
                                        dbc.Button("Close", id="close-xl", className="ml-auto")
                                        ),
                    ],
                        
                    id="modal-xl",
                    is_open=False,    # True, False
                    size="xl",        # "sm", "lg", "xl"
                    backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                    scrollable=True,  # False or True if modal has a lot of text
                    centered=True,    # True, False
                    fade=True ,
                    className="text-justify"
                )
                    
                    
                    
#-------------modal classe sismique------------------------------
modeclass=dbc.Modal(
                    [
                        dbc.ModalHeader("Description des classes sismiques selon le CNBC:"),
                        dbc.ModalBody(html.Img(srcSet=image3, height="360px")
                               ),
                        dbc.ModalFooter(
                                dbc.Button("Close", id="close-lg", className="ml-auto")
                                ),
                        ],
                    id="modal-lg",
                    is_open=False,    # True, False
                    size="xl",        # "sm", "lg", "xl"
                    backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                    scrollable=True,  # False or True if modal has a lot of text
                    centered=True,    # True, False
                    fade=True 
                )



#------------------------ Create app layout-----------------------------------

app.layout = html.Div([
        dbc.Row([
                dbc.Navbar(
  [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=image, height="120px"), width={'size': 3, 'offset': 0}),
                    dbc.Col(dbc.NavbarBrand(html.H1("ÉVALUATION DU RISQUE SISMIQUE D'UN RÉSEAU DE PONTS"), className="ml-2"), width={'size': 9, 'offset': 0}),
                ],
                align="center",
                no_gutters=True
             )
        )
    ],
    color="primary",
    dark=True,
    fixed="top",
 #   sticky="top",
    )
    ],
    ),
        
            
              dbc.Row([
                      dbc.Col(cardepi, width=9),
                      dbc.Col(cardquest, width= 3)
                       ], style={"marginTop": 200}),
                
            dbc.Row([ dbc.Col(cardmedian, width=8),
                      dbc.Col(cardhism, width= 4)
                    ], style={"marginTop": 100}),  
            
            dbc.Row([ dbc.Col(cardlow, width=8),
                      dbc.Col(cardhisl, width= 4)
                    ], style={"marginTop": 100}), 
            
            dbc.Row([ dbc.Col(cardhigh, width=8),
                      dbc.Col(cardhish, width= 4)
                    ], style={"marginTop": 100}), 
            dbc.Row([ dbc.Button(html.H4(
                    "Description des états de dommage"), id="open-xl", color="secondary"
                ),
                modetat,
                        dbc.Button(html.H4(
                    "Description des catégories d'emplacement sismique"), id="open-lg", color="secondary"
                ), modeclass
                
                
            
                    ], className="ml-2", no_gutters=True, style={"marginTop": 50}, justify="around")
                
 
 
])
#       -------- call back 1er graphique---------------
@app.callback(
                Output(component_id='my-output0', component_property='children'),
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_epicentre(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

        params_sqlalchemy1= "postgresql+psycopg2://%s:%s@%s:5432/%s" % ("postgres",
                                                      "Gres!1978",
                                                      "localhost",
                                                      "quebec2")

        engine1= create_engine(params_sqlalchemy1)
       
        file_name = 'epi'+selected_epicenter+'_M'+selected_magnitude+'_high'
        df = pd.read_sql_table(file_name, engine1)

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

        fiches=list(df["fiches2"]) 

        df = pd.DataFrame(columns=["lat", "lon", "col", "fi"], data=np.column_stack((lats, lons, col, fiches)))
        df["chemin"]=df["col"]

        for i in range(0,len(df.chemin)):
            if df.fi[i] !=0:
                df["chemin"][i]='/assets/inventaire_structure/' +str(df.fi[i])+'.JPG'
            else:
                df["chemin"][i]=='/assets/inventaire_structure/' +str(df.fi[i])+'.jpg'

# Create markers from data frame.

        
        circle = [dl.Circle(center=[row["lat"], row["lon"]],radius=200, color="blue",children=[
            dl.Tooltip("Ponts"),
            dl.Popup([
                html.Img(src=row["chemin"], height="400px")
                
            ], maxWidth="300px")]) for i, row in df.iterrows()]



#create epicenter

        dfepi = pd.read_sql_table('epicentre', engine1)
        lats = dfepi["lat"]
        lons = dfepi["long"]
        epi = []
        ind=1
        for lt,ln in zip(lats,lons):
#        dfepi = pd.DataFrame(columns=["lat", "lon"], data=np.column_stack((lats, lons)))
            epi.append(dl.Marker(position=[lt, ln], icon={
                "iconUrl": "/assets/epicentre.png",
                "iconSize": [50, 50],
                "iconAnchor": [20, 36]
                }, children=[
                    dl.Tooltip("épicentre "+str(ind))]))
            ind+=1
#
#
        epiover=dl.Overlay(dl.LayerGroup(epi), name="épicentre", checked=True)
        circleover=dl.Overlay(dl.LayerGroup(circle), name="ponts", checked=True)
        a=[epiover, circleover]
#                
           

    return a

@app.callback(
                 [Output(component_id='my-output', component_property='children'),
                 Output('histo1', 'figure'),
                 Output("perte_médian", "children")],
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
                html.H3("Caractéristiques reliées au sol" ,className= "text-center  font-weight-bold" ),
                html.H4("Accélération maximale au sol: " + str(row["pga"]),className= "text-center" ),
                html.H4("Coefficient d'AMS: " + str(row["fpga"]),className= "text-center" ),
                html.H4("Classe sismique: " + row["cla"],className= "text-center" ),
                html.H3("Caractéristiques reliées aux ponts sous sollicitations",className= "text-center  font-weight-bold" ),
                html.H4("État de dommage: " + row["tp"],className= "text-center" ),
                html.H4("Priorité d'inspection: " + row["ip"],className= "text-center" ),
                html.H4("Ordre de priorité: " + str(row["pr"]),className= "text-center" ),
                html.H4("MDF: " + str(row["mdf"]),className= "text-center" ),
                html.H4("Écart-type: " + str(row["st"]), className= "text-center"),
                html.H4("Perte économique: " + str(row["ls"])+" k$",className= "text-center" ),
                html.H4("Coût de remplacement: " + str(row["rmp"])+" k$", className= "text-center"),
#               
                
                
            ], maxWidth="300px", autoPan=False)]) for i, row in df.iterrows()]
            
         

#create epicentre

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

    
                     
#----------------CREATE THE COLOR CODE----------------------------------------
        for i in range(0, len(df)):

                df["cla"][i]="Pont" +str(int(i+1))
                
        df.sort_values(by="mdf")

#-----------------------CREATE BAR PLOT----------------------------------------
        type_etat_dommage=["Aucun", "Leger", "Modere", "Etendu", "Complet"]

        count_etat_dommage = []

        for i in type_etat_dommage:

            indice= df["tp"]==i

            nombre=[len(df["tp"][indice])]

            if nombre is not None and len(nombre) > 0:

             count_etat_dommage=np.append(count_etat_dommage,nombre)

            else:
             count_etat_dommage=np.append(count_etat_dommage,[0])

        fig1 = go.Figure(data=[go.Bar(x=type_etat_dommage, y=count_etat_dommage,)])

        fig1.update_traces(marker_color=['blue','green','yellow','orange','red'],
                       marker_line_color=['blue','green','yellow','orange','red'],
                       marker_line_width=1.5, opacity=1)

        fig1.update_layout(title_text='Nombre de ponts par état de dommage',
                       xaxis_tickangle=-45,yaxis_title="Nombre de ponts")

        pertes=np.round(int(sum(df["ls"])/1000),0)

    return  a, fig1,html.P("Pertes Économiques: " +str(pertes) +" K$")



@app.callback(
                [Output(component_id='my-output2', component_property='children'),
                 Output('histo2', 'figure'),
                 Output("perte_faible", "children")],
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_low(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------
        params_sqlalchemy1= "postgresql+psycopg2://%s:%s@%s:5432/%s" % ("postgres",
                                                      "Gres!1978",
                                                      "localhost",
                                                      "quebec2")

        engine1= create_engine(params_sqlalchemy1)
        
        file_name = 'epi'+selected_epicenter+'_M'+selected_magnitude+'_low'
        

        df = pd.read_sql_table(file_name, engine1)

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
                html.H3("Caractéristiques reliées au sol" ,className= "text-center  font-weight-bold" ),
                html.H4("Accélération maximale au sol: " + str(row["pga"]),className= "text-center" ),
                html.H4("Coefficient d'AMS: " + str(row["fpga"]),className= "text-center" ),
                html.H4("Classe sismique: " + row["cla"],className= "text-center" ),
                html.H3("Caractéristiques reliées aux ponts sous sollicitations",className= "text-center  font-weight-bold" ),
                html.H4("État de dommage: " + row["tp"],className= "text-center" ),
                html.H4("Priorité d'inspection: " + row["ip"],className= "text-center" ),
                html.H4("Ordre de priorité: " + str(row["pr"]),className= "text-center" ),
                html.H4("MDF: " + str(row["mdf"]),className= "text-center" ),
                html.H4("Écart-type: " + str(row["st"]), className= "text-center"),
                html.H4("Perte économique: " + str(row["ls"])+" k$",className= "text-center" ),
                html.H4("Coût de remplacement: " + str(row["rmp"])+" k$", className= "text-center"),
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

    
                     
#----------------CREATE THE COLOR CODE----------------------------------------
        for i in range(0, len(df)):

                df["cla"][i]="Pont" +str(int(i+1))
                
        df.sort_values(by="mdf")

#-----------------------CREATE BAR PLOT----------------------------------------
        type_etat_dommage=["Aucun", "Leger", "Modere", "Etendu", "Complet"]

        count_etat_dommage = []

        for i in type_etat_dommage:

            indice= df["tp"]==i

            nombre=[len(df["tp"][indice])]

            if nombre is not None and len(nombre) > 0:

             count_etat_dommage=np.append(count_etat_dommage,nombre)

            else:
             count_etat_dommage=np.append(count_etat_dommage,[0])

        fig1 = go.Figure(data=[go.Bar(x=type_etat_dommage, y=count_etat_dommage,)])

        fig1.update_traces(marker_color=['blue','green','yellow','orange','red'],
                       marker_line_color=['blue','green','yellow','orange','red'],
                       marker_line_width=1.5, opacity=1)

        fig1.update_layout(title_text='Nombre de ponts par état de dommage',
                       xaxis_tickangle=-45,yaxis_title="Nombre de ponts")

        pertes=np.round(int(sum(df["ls"])/1000),0)

    return  a, fig1,html.P("Pertes Économiques: " +str(pertes) +" K$")


@app.callback(
                [Output(component_id='my-output3', component_property='children'),
                 Output('histo3', 'figure'),
                 Output("perte_élévé", "children")],

                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
             )

def update_graph_high(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------

        params_sqlalchemy1= "postgresql+psycopg2://%s:%s@%s:5432/%s" % ("postgres",
                                                      "Gres!1978",
                                                      "localhost",
                                                      "quebec2")

        engine1= create_engine(params_sqlalchemy1)
       
        file_name = 'epi'+selected_epicenter+'_M'+selected_magnitude+'_high'
        df = pd.read_sql_table(file_name, engine1)

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
                html.H3("Caractéristiques reliées au sol" ,className= "text-center  font-weight-bold" ),
                html.H4("Accélération maximale au sol: " + str(row["pga"]),className= "text-center" ),
                html.H4("Coefficient d'AMS: " + str(row["fpga"]),className= "text-center" ),
                html.H4("Classe sismique: " + row["cla"],className= "text-center" ),
                html.H3("Caractéristiques reliées aux ponts sous sollicitations",className= "text-center  font-weight-bold" ),
                html.H4("État de dommage: " + row["tp"],className= "text-center" ),
                html.H4("Priorité d'inspection: " + row["ip"],className= "text-center" ),
                html.H4("Ordre de priorité: " + str(row["pr"]),className= "text-center" ),
                html.H4("MDF: " + str(row["mdf"]),className= "text-center" ),
                html.H4("Écart-type: " + str(row["st"]), className= "text-center"),
                html.H4("Perte économique: " + str(row["ls"])+" k$",className= "text-center" ),
                html.H4("Coût de remplacement: " + str(row["rmp"])+" k$", className= "text-center"),
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

    
                     
#----------------CREATE THE COLOR CODE----------------------------------------
        for i in range(0, len(df)):

                df["cla"][i]="Pont" +str(int(i+1))
                
        df.sort_values(by="mdf")

#-----------------------CREATE BAR PLOT----------------------------------------
        type_etat_dommage=["Aucun", "Leger", "Modere", "Etendu", "Complet"]

        count_etat_dommage = []

        for i in type_etat_dommage:

            indice= df["tp"]==i

            nombre=[len(df["tp"][indice])]

            if nombre is not None and len(nombre) > 0:

             count_etat_dommage=np.append(count_etat_dommage,nombre)

            else:
             count_etat_dommage=np.append(count_etat_dommage,[0])

        fig1 = go.Figure(data=[go.Bar(x=type_etat_dommage, y=count_etat_dommage,)])

        fig1.update_traces(marker_color=['blue','green','yellow','orange','red'],
                       marker_line_color=['blue','green','yellow','orange','red'],
                       marker_line_width=1.5, opacity=1)

        fig1.update_layout(title_text='Nombre de ponts par état de dommage',
                       xaxis_tickangle=-45,yaxis_title="Nombre de ponts")

        pertes=np.round(int(sum(df["ls"])/1000),0)

    return  a, fig1,html.P("Pertes Économiques: " +str(pertes) +" K$")
#-------------popover état de dommage------------------------------
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


app.callback(
    Output("modal-xl", "is_open"),
    [Input("open-xl", "n_clicks"), Input("close-xl", "n_clicks")],
    [State("modal-xl", "is_open")],
)(toggle_modal)

app.callback(
    Output("modal-lg", "is_open"),
    [Input("open-lg", "n_clicks"), Input("close-lg", "n_clicks")],
    [State("modal-lg", "is_open")],
)(toggle_modal)
#--------------final-------------------------------------------
            
if __name__ == "__main__":
    app.run_server(debug=False)