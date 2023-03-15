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

import pathlib
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
                            
#-------------------------card epicenter--------------------------------------
cardepi = dbc.Card([dbc.CardHeader(html.H3("Emplacement des épicentres"), className="text-white"),
                     dbc.CardBody([
                                     dcc.Graph(id="map0",config={'displayModeBar': False, 'scrollZoom': True},
                                  style={'background':'#00FC87','width': '100%','height':'100%'}),
                                             ],
      #                             id="countGraphContainer",
     #                               className="pretty_container",
                                ),
                             
                            ], color="primary")
#-------------------------------card median-----------------------------------
cardmedian= dbc.Card([dbc.CardHeader(html.H3("Scénario pour le niveau d'aléa médian"), className="text-white"),
                     dbc.CardBody([dcc.Graph(id="map1",config={'displayModeBar': False, 'scrollZoom': True},
                                  style={'width': '100%','height':'100%'}
                          )
                             
                             ])
                             ], color="primary")

#--------------------------------card low-------------------------------------
cardlow= dbc.Card([dbc.CardHeader(html.H3("Scénario pour le niveau d'aléa bas"), className="text-white"),
                     dbc.CardBody([dcc.Graph(id="map2", config={'displayModeBar': False, 'scrollZoom': True},
                                  style={'width': '100%','height':'100%'})
                             
                              ])
                             ], color="primary")         

#--------------------------------card high-------------------------------------
cardhigh= dbc.Card([dbc.CardHeader(html.H3("Scénario pour le niveau d'aléa élevé"), className="text-white"),
                     dbc.CardBody([dcc.Graph(id="map3",config={'displayModeBar': False, 'scrollZoom': True},
                                  style={'width': '100%','height':'100%'})
                             
                              ])
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
#-----------------------------------popover etats de dommage--------------------
popetat=dbc.Popover(
                    [
                        dbc.PopoverHeader("Description des états de dommage:"),
                        dbc.PopoverBody(children=[
                                html.H6("Léger: Légères fissures et écaillages au niveau des culées et de joints de discontinuité des poutres, léger écaillage de la colonne et légères fissures au niveau du tablier."),
                                html.H6("Modéré: Petit affaissement des culées, dégradation des murs caches au niveau des culées, colonne avec une fissuration et écaillage modérés (sans rupture), une rupture des appareils d’appuis à pendule ou un tassement modéré de la dalle."),
                                html.H6("Étendu: Dégradation des colonnes, rupture en cisaillement sans perte d'intégrité, tassement différentiel au niveau des connexions, rupture des murs caches des culées, translation verticale de la culée."),
                                html.H6("Complet: Déchaussement du tablier, rupture des piles, affaissement de la structure.")])
                    ],
                    id="popover-bottom",
                    target="popover-bottom-target",  # needs to be the same as dbc.Button id
                    placement="top",
                    is_open=False,
                    className="text-justify"
                )
                    
                    
                    
#-------------popover classe sismique------------------------------
popclass=dbc.Popover(
                    [
                        dbc.PopoverHeader("Description des classes sismiques selon le CNBC:"),
                        dbc.PopoverBody(html.Img(srcSet=image3, height="360px")
                               ) ],
                    id="popover-top",
                    target="popover-top-target",  # needs to be the same as dbc.Button id
                    placement="top",
                    is_open=False
                    , style={"width": 570}
                )

#-------------popover écart-type------------------------------
popmdf=dbc.Popover(
                    [
                        dbc.PopoverHeader("Description du facteur de dommage moyen et de son écart-type"),
                        dbc.PopoverBody(html.Img(srcSet=image2, height="360px")
                               ) ],
                    id="popover-left",
                    target="popover-left-target",  # needs to be the same as dbc.Button id
                    placement="left",
                    is_open=False
                    , style={"width": 540}
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
                    "Description des états de dommage"), id="popover-bottom-target", color="secondary"
                ),
                popetat,
                        dbc.Button(html.H4(
                    "Description des classes sismiques"), id="popover-top-target", color="secondary"
                ),
                popclass,
                        dbc.Button(html.H4(
                    "Description du FDM et de son écart-type"), id="popover-left-target", color="secondary"
                ),
                popmdf
            
                    ], className="ml-2", no_gutters=True, style={"marginTop": 50}, justify="around")
                
 
 
])
#       -------- call back 1er graphique---------------
@app.callback(
                Output('map0', 'figure'),
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_epicentre(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

        #PATH = pathlib.Path(__file__).parent
        #DATA_PATH = PATH.joinpath("data").resolve()
        file_name='epicentre.xlsx'
        #df=pd.read_excel(DATA_PATH.joinpath(file_name))

        chemin = 'C:/Users/azarm/Documents/bridgetest/data/'
        file_name1 = chemin + file_name
        df = pd.read_excel(file_name1)

        df['latitude']=np.round(df['latitude'],2)
        df['longitude']=np.round(df['longitude'],2)
#        titre='CARTE DES ÉPICENTRES'

#---------------CREATE THE MAP-------------------------------------------------

    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="Nom", height=500,
   #                  title=titre 
                     )

    fig.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=46.85, lon=-71.3),
                                  zoom=9),margin={"r":1,"t":40,"l":1,"b":1})

    fig.update_traces(mode='markers', marker_size=20,marker_color='red',
                      )

    return fig

@app.callback(
                [Output('map1', 'figure'),Output('histo1', 'figure'),
                 Output("perte_médian", "children")],
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_median(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------

        #PATH = pathlib.Path(__file__).parent
        #DATA_PATH = PATH.joinpath("data").resolve()
        file_name = 'epi'+selected_epicenter+'_M'+selected_magnitude+'_med.xlsx'
        #df = pd.read_excel(DATA_PATH.joinpath(file_name))

        chemin = 'C:/Users/azarm/Documents/bridgetest/data/'
        file_name1 = chemin + file_name
        df = pd.read_excel(file_name1)

        df['lat'] = np.round(df['lat'],2)
        df['long'] = np.round(df['long'],2)
        df["Etat de Dommage"]=df["Damage_State"]
        df["Nom"] = df["Classe_Sismique"]

        for i in range(0, len(df)):

            df["Nom"][i]="Pont" +str(int(i+1))

        df.sort_values(by='MRD_pour')

#----------------CREATE THE COLOR CODE----------------------------------------

        damage_color_code=dict(Aucun='blue',Leger='green',Modere='yellow',Etendu='orange',
                        Complet='red')

        titre="  (" +'ÉPICENTRE ' +selected_epicenter+ ','+'MAGNITUDE '+selected_magnitude+")"

#---------------CREATE THE MAP------------------------------------------------

    fig = px.scatter_mapbox(df, lat="lat", lon="long",
                            hover_data=['Classe_Sismique',"Etat de Dommage", "PGA", "St_Dev_DR", "Inspection_Priority", "Priority_Rank", "Replacement_cost", "Economic_Loss", "MRD_pour", "F_PGA"],
                        color_discrete_map=damage_color_code, color="Etat de Dommage",
                        zoom=9.8, height=550,title=titre)

    fig.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=46.85, lon=-71.3),
                                  zoom=9.8),margin={"r":1,"t":40,"l":1,"b":1})

    fig.update_traces(mode='markers', marker_size=15)

#-----------------------CREATE BAR PLOT----------------------------------------

    type_etat_dommage=list(damage_color_code.keys())

    count_etat_dommage = []

    for i in type_etat_dommage:

        indice= df['Etat de Dommage']==i

        nombre=[len(df['Etat de Dommage'][indice])]

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

    pertes=np.round(int(sum(df["Economic_Loss"])/1000),0)

    return fig,fig1,html.P("Pertes Économiques: " +str(pertes) +" K$")


@app.callback(
                [Output('map2', 'figure'),Output('histo2', 'figure'),
                 Output("perte_faible", "children")],
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_low(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------
        chemin='C:/Users/azarm/Documents/bridgetest/data/'
        #PATH = pathlib.Path(__file__).parent
        #DATA_PATH = PATH.joinpath("data").resolve()
        file_name='epi'+selected_epicenter+'_M'+selected_magnitude+'_low.xlsx'
        #df=pd.read_excel(DATA_PATH.joinpath(file_name))
        file_name1=chemin+file_name
        df=pd.read_excel(file_name1)
        df['lat']=np.round(df['lat'],2)
        df['long']=np.round(df['long'],2)
        df["Etat de Dommage"]=df["Damage_State"]
        df["Nom"]=df["Classe_Sismique"]

        df["tri"]=df["lat"]

        for i in range(0,len(df)):

            df["Nom"][i]="Pont" +str(int(i+1))

        df.sort_values(by='MRD_pour')

#----------------CREATE THE COLOR CODE----------------------------------------

        damage_color_code=dict(Aucun='blue',Leger='green',Modere='yellow',Etendu='orange',
                        Complet='red')

        titre=" (" + 'ÉPICENTRE ' + selected_epicenter + ',' + 'MAGNITUDE ' + selected_magnitude +")"

#---------------CREATE THE MAP------------------------------------------------

    fig = px.scatter_mapbox(df, lat="lat", lon="long",
                            hover_data=['Classe_Sismique',"Etat de Dommage", "PGA", "St_Dev_DR", "Inspection_Priority", "Priority_Rank", "Replacement_cost", "Economic_Loss", "MRD_pour", "F_PGA"],

                            color_discrete_map=damage_color_code, color="Etat de Dommage",
                            zoom=9.8, height=550)

    fig.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=46.85, lon=-71.3),
                    zoom=9.8),margin={"r":1,"t":40,"l":1,"b":1},title=titre)

    fig.update_traces(mode='markers', marker_size=15)

#-----------------------CREATE BAR PLOT----------------------------------------

    type_etat_dommage=list(damage_color_code.keys())

    count_etat_dommage = []

    for i in type_etat_dommage:

        indice= df['Etat de Dommage']==i

        nombre=[len(df['Etat de Dommage'][indice])]

        if nombre is not None and len(nombre) > 0:

             count_etat_dommage=np.append(count_etat_dommage,nombre)

        else:
             count_etat_dommage=np.append(count_etat_dommage,[np.nan])

#    print(count_etat_dommage)

    fig1 = go.Figure(data=[go.Bar(x=type_etat_dommage, y=count_etat_dommage,)])

    fig1.update_traces(marker_color=['blue','green','yellow','orange','red'],
                       marker_line_color=['blue','green','yellow','orange','red'],
                       marker_line_width=1.5, opacity=1)

    fig1.update_layout(title_text='Nombre de ponts par état de dommage',
                       xaxis_tickangle=-45,yaxis_title="Nombre de ponts")

    pertes=np.round(int(sum(df["Economic_Loss"])/1000),0)

    return fig, fig1,html.P("Pertes Économiques: " +str(pertes) +" K$")


@app.callback(
                [Output('map3', 'figure'),Output('histo3', 'figure'),
                 Output("perte_élévé", "children")],

                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
             )

def update_graph_high(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------

        chemin='C:/Users/azarm/Documents/bridgetest/data/'
        #PATH = pathlib.Path(__file__).parent
        #DATA_PATH = PATH.joinpath("data").resolve()
        file_name='epi'+selected_epicenter+'_M'+selected_magnitude+'_high.xlsx'
        file_name1=chemin+file_name
        #df=pd.read_excel(DATA_PATH.joinpath(file_name))
        df=pd.read_excel(file_name1)
        df['lat']=np.round(df['lat'],2)
        df['long']=np.round(df['long'],2)

        df["Etat de Dommage"]=df["Damage_State"]
        df["Nom"]=df["Damage_State"]

        df["tri"]=df["lat"]

        for i in range(0,len(df)):

            df["Nom"][i]="Pont" +str(int(i+1))

        df.sort_values(by='MRD_pour')

#----------------CREATE THE COLOR CODE----------------------------------------

        damage_color_code=dict(Aucun='blue',Leger='green',Modere='yellow',Etendu='orange',Complet='red')

        titre=" (" +'ÉPICENTRE ' +selected_epicenter+ ','+'MAGNITUDE '+selected_magnitude+")"


#---------------CREATE THE MAP------------------------------------------------

    fig = px.scatter_mapbox(df, lat="lat", lon="long",
                            hover_data=['Classe_Sismique',"Etat de Dommage","PGA", "St_Dev_DR", "Inspection_Priority", "Priority_Rank", "Replacement_cost", "Economic_Loss", "MRD_pour", "F_PGA"],
                        color_discrete_map=damage_color_code, color="Etat de Dommage",
                        zoom=9.8, height=550,title=titre)

    fig.update_layout(mapbox=dict(style='open-street-map',center=dict(lat=46.85, lon=-71.3),
                                  zoom=9.8),margin={"r":1,"t":40,"l":1,"b":0})

    fig.update_traces(mode='markers', marker_size=15)

#-----------------------CREATE BAR PLOT----------------------------------------

    type_etat_dommage=list(damage_color_code.keys())

    count_etat_dommage = []

    for i in type_etat_dommage:

        indice= df['Etat de Dommage']==i

        nombre=[len(df['Etat de Dommage'][indice])]

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

    pertes=np.round(int(sum(df["Economic_Loss"])/1000),0)

    return fig,fig1, html.P("Pertes Économiques: " +str(pertes) +" K$")
#-------------popover état de dommage------------------------------
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


for p in ["bottom", "top", "left"]:
    app.callback(
        Output(f"popover-{p}", "is_open"),
        [Input(f"popover-{p}-target", "n_clicks")],
        [State(f"popover-{p}", "is_open")],
    )(toggle_popover)


#--------------final-------------------------------------------
            
if __name__ == "__main__":
    app.run_server(debug=False)