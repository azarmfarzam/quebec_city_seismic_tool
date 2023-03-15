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


import plotly.graph_objects as go
from sqlalchemy import create_engine
import dash_leaflet as dl
import pandas as pd
import numpy as np
#from Authentification import Code_auth

#-----------------app authentification----------------------------------------

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.1"}])
server = app.server

#----------------------Create controls-----------------------------------------

epicentre_options = [ {"label": 'Epicenter '+str(i), "value": str(i)}
                      for i in range(1,21) ]

image= "https://en.clubnaova.ca/static/media/ets.90e12cca.png"

image2= "/assets/ecart.jpg"

image3="/assets/classe.jpg"

image8="/assets/english_legend.png"

legendepi1="/assets/epi_legend_en.png"

#-----------------------------card question-----------------------------------
cardquest = dbc.Card([dbc.CardHeader(html.H3("Scenario selection"), className="text-white"),
                     dbc.CardBody([
                             html.H4("Choose an epicenter", className="card-title text-white"),
                             dcc.Dropdown(
                                id="select_epicentre",
                                options=epicentre_options,
                                multi=False,
                                value='1',
                                className="dcc_control",
                            ),
                            html.H4("Choose a magnitude", className="card-title text-white mt-5"), 
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
get_info=[html.H4("Legend")]+ [html.Img(srcSet=legendepi1, height="60px")]

info = html.Div(children=get_info, id="info", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
#-------------------------card epicenter--------------------------------------
cardepi = dbc.Card([dbc.CardHeader(html.H3("Epicenters and Bridges"), className="text-white"),
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
get_info=[html.H4("Legend")]+ [html.Img(srcSet=image8, height="180px")]

info1 = html.Div(children=get_info, id="info1", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
#-------------------------------card median-----------------------------------
cardmedian= dbc.Card([dbc.CardHeader(html.H3("Scenario for the Median of Ground Motion Prediction Equation"), className="text-white"),
                     dbc.CardBody(html.Div([
                             dl.Map(children=[dl.TileLayer(), 
#                     dl.LayerGroup(circle), dl.LayerGroup(epi), 
                                     info1, html.Div(dl.LayersControl(id="my-output")) 
                                     ],
                                     style={'width': "100%", 'height': "100%"}, center=[46.83, -71.3], zoom=11, id="map1"),
                                     ], style={'width': '963px', 'height': '700px'})
                                     ) ], color="primary")

#-------------------------------legend cartes dommages-------------------------
get_info=[html.H4("Legend")]+ [html.Img(srcSet=image8, height="180px")]

info2 = html.Div(children=get_info, id="info2", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
#--------------------------------card low-------------------------------------
cardlow= dbc.Card([dbc.CardHeader(html.H3("Scenario for Lower Bound of Ground Motion Prediction Equation"), className="text-white"),
                     dbc.CardBody(html.Div([
                             dl.Map(children=[dl.TileLayer(), 
#                     dl.LayerGroup(circle), dl.LayerGroup(epi), 
                                     info2, html.Div(dl.LayersControl(id="my-output2")) 
                                     ],
                                     style={'width': "100%", 'height': "100%"}, center=[46.83, -71.3], zoom=11, id="map2"),
                                     ], style={'width': '963px', 'height': '700px'}))
                             ], color="primary")         

#-------------------------------legend cartes dommages-------------------------
get_info=[html.H4("Legend")]+ [html.Img(srcSet=image8, height="180px")]

info3 = html.Div(children=get_info, id="info3", className="info",
                style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
#--------------------------------card high-------------------------------------
cardhigh= dbc.Card([dbc.CardHeader(html.H3("Scenario for Upper Bound of Ground Motion Prediction Equation"), className="text-white"),
                     dbc.CardBody(html.Div([
                             dl.Map(children=[dl.TileLayer(), 
#                     dl.LayerGroup(circle), dl.LayerGroup(epi), 
                                     info3, html.Div(dl.LayersControl(id="my-output3")) 
                                     ],
                                     style={'width': "100%", 'height': "100%"}, center=[46.83, -71.3], zoom=11, id="map3"),
                                     ], style={'width': '963px', 'height': '700px'}))
                             ], color="primary")           
#-------------------------------histogramm median-----------------------------
cardhism= dbc.Card([dbc.CardHeader(html.H3("Statement of the Median Hazard Scenario"), className="text-white"),
                        dbc.CardBody([html.Div([html.H4(id="perte_médian")],
                                        id="perte-med",className="text-white")],style={"marginTop": 20}),
                                      dcc.Graph(id="histo1")
        
        ], body=True, color="primary")  


#-------------------------------histogramm low-----------------------------
cardhisl= dbc.Card([dbc.CardHeader(html.H3("Statement of the Low Hazard Scenario"), className="text-white"),
                        dbc.CardBody([html.Div([html.H4(id="perte_faible")],
                                        id="perte-faib",className="text-white")],style={"marginTop": 20}),
                                      dcc.Graph(id="histo2")
        
        ], body=True, color="primary")  

#-------------------------------histogramm high-----------------------------
cardhish= dbc.Card([dbc.CardHeader(html.H3("Statement of the High Hazard Scenario"), className="text-white"),
                        dbc.CardBody([html.Div([html.H4(id="perte_élévé")],
                                        id="perte-élév",className="text-white")],style={"marginTop": 20}),
                                      dcc.Graph(id="histo3")
        
        ], body=True, color="primary")  
#-----------------------------------modal etats de dommage--------------------
image4="/assets/leger.jpg"
image5="/assets/modere.jpg"
image6="/assets/etendu.jpg"
image7="/assets/complet.jpg"
immod2="/assets/mode2.png"
immod3="/assets/mod3.png"
imete2="/assets/etendu2.png"
imcomp2="/assets/complet2.png"
imcomp3="/assets/complet3.png"
imcomp4="/assets/complet4.png"

modetat=dbc.Modal(
                    [
                        dbc.ModalHeader("Damage State Description:"),
                        dbc.ModalBody(children=[
                                html.H5("Slight Damage State(in green):", className="text-center"), 
                                html.H6("Slight:Minor cracking and spalling to the abutment, cracks in shear keys at abutments, minor \
                                        spalling and cracks at hinges, minor spalling at the column (damage requires no more than\
                                        cosmetic repair) or minor cracking to the deck. ", className="text-center"),
                                html.Img(srcSet=image4, height="240px", style={"marginLeft": 310}),
                                html.H6("Image tirée de (https://intrans.iastate.edu/app/uploads/2019/11/MAPbriefNovember2016.pdf)", className="text-center"),
                                html.H5("Moderate Damage State: (in yellow)", className="text-center"),
                                html.H6('Moderate: Any column experiencing moderate (shear cracks) cracking and spalling (column \
                                        structurally still sound), moderate movement of the abutment (<2"), extensive cracking and \
                                        spalling of shear keys, any connection having cracked shear keys or bent bolts, keeper bar \
                                        failure without unseating, rocker bearing failure or moderate settlement of the approach.', className="text-center"),
                                html.Img(srcSet=image5, height="240px", style={"marginLeft": 450}),
                                html.H6("Image tirée de (Misra et al., 2018)", className="text-center"),
                                html.Img(srcSet=immod2, height="240px", style={"marginLeft": 450}),
                                html.H6("Image tirée de (Mitchell et al. 2012)", className="text-center"),
                                html.Img(srcSet=immod3, height="240px", style={"marginLeft": 390}),
                                html.H6("Image tirée de (Mitchell et al. 2012)", className="text-center"),
                                html.H5("Extensive Damage State: (in orange)",  className="text-center"),
                                html.H6("Extensive: Any column degrading without collapse – shear failure - (column structurally unsafe), \
                                        significant residual movement at connections, or major settlement approach, vertical offset of the \
                                        abutment, differential settlement at connections, shear key failure at abutments.", className="text-center"),
                                html.Img(srcSet=image6, height="240px", style={"marginLeft": 390}),
                                html.H6("Image tirée de (Misra et al., 2018)", className="text-center"),
                                html.Img(srcSet=imete2, height="240px", style={"marginLeft": 390}),
                                html.H6("Image tirée de (Misra et al., 2018)", className="text-center"),
                                html.H5("Complete Damage State (in red):", className="text-center"),
                                html.H6("Complete: Any column collapsing and connection losing all bearing support, \
                                        which may lead to imminent deck collapse, tilting of substructure due to foundation failure.", className="text-center"),
                                html.Img(srcSet=image7, height="240px", style={"marginLeft": 315}),
                                html.H6("Image tirée de Yashinsky et al. (2010)", className="text-center"),
                                html.Img(srcSet=imcomp2, height="240px", style={"marginLeft": 460}),
                                html.H6("Image tirée de (Misra et al., 2018)", className="text-center"),
                                html.Img(srcSet=imcomp3, height="240px", style={"marginLeft": 390}),
                                html.H6("Image tirée de Yashinsky et al. (2010)", className="text-center"),
                                html.Img(srcSet=imcomp4, height="240px", style={"marginLeft": 340}),
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
soil="/assets/EN_tableCNBC.png"
soil2="/assets/EN_Legendtable.png"
soil3="/assets/soil.png"
modeclass=dbc.Modal(
                    [
                        dbc.ModalHeader("Seismic Site Classes Description:"),
                        dbc.ModalBody(children=[
                            html.H4("Seismic site classes", className="text-center"),     
                            html.H6("Site classification describes the potential for amplification or de-amplification of seismic \
                                    waves at the local scale. The National Building Code of Canada (NBC) describes seismic site \
                                    class categories as shown in Table 1.", className= "text-justify"),
                            html.H6("Table 1. Description of site classification from NBCC", className="text-center"),
                            html.Img(srcSet=soil, height="360px", style={"marginLeft": 200}),
                            html.Img(srcSet=soil2, height="120px", style={"marginLeft": 250}),
                            html.Img(srcSet=soil3, height="300px", style={"marginLeft": 350}),
                            html.H6("(Hunter et al. 2012)", className="text-center")
                            ]
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
                    fade=True, 
                    className="text-justify"
                )
                        
#-------------modal classe pont------------------------------
table1="/assets/bridge_class.png"
table2="/assets/MTQpontcorres.png"

modebridge=dbc.Modal(
                    [
                        dbc.ModalHeader("Bridge classification description:"),
                        dbc.ModalBody(children=[
                            html.H4("Bridge classification description", className="text-center"),    
                            html.H6("Bridges information were obtained from the following website:", className="text-justify"),
                            html.H6("https://www.transports.gouv.qc.ca/fr/projets-infrastructures/structures/Pages/inventaires-structures.aspx", className="text-justify"),
                            html.H6("The bridge information was used to estimate the corresponding fragility-based \
                                    class to identify for each bridge the corresponding fragility function for damage \
                                        assessment. The bridge fragility classes are: (SS - Concrete, SS - Steel, MSC - \
                                        Steel, MSC - Concrete, MSC - Slab, MSSS - Steel, MSSS – Concrete, Others) according \
                                        to the following references (Nielson, 2005; Tavares, 2012; Hazus 2012). Once the bridge \
                                        class is determined, the fragility function corresponding to each state of damage for this \
                                        bridge class is used to determine the probability of being in each damage state (Figure 1). \
                                        Details of the methodology used to establish the fragility-based classes are presented in Fezai (2020).", className= "text-justify"),
                                        html.Img(srcSet=table1, height="420px", style={"marginLeft": 275}),
                                        html.H6("References:", className="text-justify"),
                                        html.H6("Fezai, H (2020). Scénarios de risque sismique d’un réseau municipal de ponts pour l’évaluation des impacts économiques. Master Thesis. École de technologie supérieure.", className="text-justify"),
                                        html.H6("Nielson, B. G. (2005). Analytical fragility curves for highway bridges in moderate seismic zones. PhD. Thesis, Georgia Institute of Technology.", className="text-justify"),
                                        html.H6("HAZUS-MH. (2011). Multi-hazard loss estimation methodology: Earthquake model Hazus-MH MR5 technical manual: Federal Emergency Management Agency Washington DC.", className="text-justify"),
                                        html.H6("Tavares, D. H. (2012). Évaluation de la vulnérabilité sismique des ponts routiers au Québec à l'aide des courbes de fragilité. PhD. Thesis, Université de Sherbrooke.", className="text-justify")
                                        ]
                               ),
                        dbc.ModalFooter(
                                dbc.Button("Close", id="close", className="ml-auto")
                                ),
                        ],
                    id="modal",
                    is_open=False,    # True, False
                    size="xl",        # "sm", "lg", "xl"
                    backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                    scrollable=True,  # False or True if modal has a lot of text
                    centered=True,    # True, False
                    fade=True, 
                    className="text-justify"
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
                    dbc.Col(dbc.NavbarBrand(html.H1("POST-EARTHQUAKE DAMAGE CALCULATOR FOR BRIDGE NETWORK"), className="ml-2"), width={'size': 9, 'offset': 0}),
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
                    "Damage State Description"), id="open-xl", color="secondary"
                ),
                modetat,
                        dbc.Button(html.H4(
                    "Seismic Site Classes Description"), id="open-lg", color="secondary"
                ), modeclass,
            
                        dbc.Button(html.H4(
                    "Bridge Classification"), id="open", color="secondary"
                ), modebridge
                
                
            
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
                                                      "xxxxx",
                                                      "localhost",
                                                      "quebec2")

        engine1= create_engine(params_sqlalchemy1)
       
        file_name = 'epi'+selected_epicenter+'_M'+selected_magnitude+'_high'
        df = pd.read_sql_table(file_name, engine1)

#---------------------------------color------------------------
      

        lats = df.lat
        lons = df.long
        bridge = df.Class
        pic = list(df["Pictures"])
        fiches=list(df["fiches2"]) 

        df = pd.DataFrame(columns=["lat", "lon", "fi", "pic", "bri"], data=np.column_stack((lats, lons, fiches, pic, bridge)))
        df["chemin"]=df["bri"]

        for i in range(0,len(df.chemin)):
            if df.fi[i] !=0:
                df["chemin"][i]='/assets/inventaire_structure/' +str(df.fi[i])+'.JPG'
            else:
                df["chemin"][i]=='/assets/inventaire_structure/' +str(df.fi[i])+'.jpg'

# Create markers from data frame.

        
        circle = [dl.Circle(center=[row["lat"], row["lon"]],radius=200, color="blue",children=[
            dl.Tooltip("Bridge"),
            dl.Popup([
              html.Img(src= row["pic"], height="180px"),
              html.A("Link to the MTQ technical file ", href=row["chemin"], target="_blank", className= "text-center"),
              html.H6("Bridge class: " + str(row["bri"]))  
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
                    dl.Tooltip("epicenter "+str(ind))]))
            ind+=1
            
##create one epicenter

        df2 = pd.read_sql_table('epicentre', engine1)
        lat=df2.at[float(selected_epicenter)-1,'lat']
        long=df2.at[float(selected_epicenter)-1,'long']

        epione=dl.Marker(position=[lat, long], icon={
                "iconUrl": "/assets/Image3.png",
                "iconSize": [50, 50],
                "iconAnchor": [20, 36]
            }
                , children=[
                dl.Tooltip("selected epicentre")])
#
        epiover=dl.Overlay(dl.LayerGroup(epi), name="épicentre", checked=True)
        circleover=dl.Overlay(dl.LayerGroup(circle), name="ponts", checked=True)
        epicell=dl.Overlay(dl.LayerGroup(epione), name="selected epicentre", checked=True)
        a=[epiover, circleover, epicell]
#                
           

    return a

@app.callback(
                 [Output(component_id='my-output', component_property='children'),
                 Output('histo1', 'figure'),
 #                Output("perte_médian", "children")
                 ],
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_median(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------
        #---------------------------------SQL------------------------
#connection sql
        params_sqlalchemy1= "postgresql+psycopg2://%s:%s@%s:5432/%s" % ("postgres",
                                                      "xxxxx",
                                                      "localhost",
                                                      "quebec2")

        engine1= create_engine(params_sqlalchemy1)
        
        file_name = 'epi'+selected_epicenter+'_M'+selected_magnitude+'_med'
        

        df = pd.read_sql_table(file_name, engine1)

#---------------------------------color------------------------
        col = []
        for row in df['Damage_State']:
                if row=="None" :    col.append('blue')
                elif row=="Slight":   col.append('green')
                elif row=="Moderate":  col.append('yellow')
                elif row=="Extensive":  col.append('orange')
                elif row=="Complete":  col.append('red')
        
        df["col"]= col   
        
        sol = []
        for row in df['Classe_Sismique']:
                if row=="A" :    sol.append('Hard rock')
                elif row=="B":   sol.append('Rock')
                elif row=="C":  sol.append('Very dense soil and soft rock')
                elif row=="D":  sol.append('Stiff soil')
                elif row=="E":  sol.append('Soft soil')
        
        df["sol"]= sol

        traf = []
        for row in df['Damage_State']:
                if row=="None" :    traf.append('Open to normal traffic - no restrictions')
                elif row=="Slight":   traf.append('Open to normal traffic- no restrictions')
                elif row=="Moderate":  traf.append('Open to limited traffic - speed/weight/lane restrictions')
                elif row=="Extensive":  traf.append('Emergency vehicles only - speed/weight/lane restrictions')
                elif row=="Complete":  traf.append('Closed until shored/braced - potential for collapse')
        
        df["traf"]= traf 

        lats = df.lat
        lons = df.long
        cl = df.Classe_Sismique
        bridge = df.Class
        pic = list(df["Pictures"])
        Ins_pri=list(df["Inspection_Priority"])
        temp=list(df["Damage_State"])
        mdf=list(df["MRD_pour"])
        p_r=list(df["Priority_Rank"])
        St_dev=list(df["St_Dev_DR"])
        
#        remp=np.round(np.array(df["Replacement_cost"])/1000)
#        Loss=np.round(np.array(df["Economic_Loss"])/1000)
        
        pga=list(df["PGA"])
        fiches=list(df["fiches2"]) 

        df = pd.DataFrame(columns=["lat", "lon", "cla", "col","ip","tp","mdf","pr","st","pga", "fi", "pic", "bri", "sol", "tra"], data=np.column_stack((lats, lons, cl, col, Ins_pri,temp,mdf,p_r,St_dev,pga,fiches, pic, bridge, sol, traf)))
        df["chemin"]=df["col"]

        for i in range(0,len(df.chemin)):
            if df.fi[i] !=0:
                df["chemin"][i]='/assets/inventaire_structure/' +str(df.fi[i])+'.JPG'
            else:
                df["chemin"][i]=='/assets/inventaire_structure/' +str(df.fi[i])+'.jpg'

# Create markers from data frame.


        circle = [dl.Circle(center=[row["lat"], row["lon"]],radius=200, color=row["col"],children=[
            dl.Tooltip("Bridge"),
            dl.Popup([
                html.Img(src= row["pic"], width="300px"),
                html.A("Link to the MTQ technical file ", href=row["chemin"], target="_blank", className= "text-center"),
                html.H5("Soil characteristics" ,className= "text-center  font-weight-bold" ),
                html.H6(["Peak ground acceleration: " + str(row["pga"]) + " m/s", html.Sup("2")],className= "text-center" ), 
                html.H6("Ground profil name: " + row["sol"], className= "text-center" ),
                html.H5("Bridge characteristics",className= "text-center  font-weight-bold" ),
                html.H6("Bridge class: " + str(row["bri"]),className= "text-center" ),
                html.H6("Damage state: " + row["tp"],className= "text-center" ),
                html.H6("Likely post-event traffic state: " + row["tra"],className= "text-center" ),
                html.H6("Inspection priority: " + row["ip"],className= "text-center" ),
                html.H6("Priority rank: " + str(row["pr"]),className= "text-center" ),
                html.H6("Mean damage factor in %: " + str(row["mdf"]),className= "text-center" ),
                html.H6("Standard deviation: " + str(row["st"]), className= "text-center"),
#                html.H6("Economic loss: " + str(row["ls"])+" k$",className= "text-center" ),
#                html.H6("Replacement cost: " + str(row["rmp"])+" k$", className= "text-center"),
#               
                
                
            ], maxWidth="400px", autoPan=True)]) for i, row in df.iterrows()]
            
         

#create epicentre

        df2 = pd.read_sql_table('epicentre', engine1)
        lat=df2.at[float(selected_epicenter)-1,'lat']
        long=df2.at[float(selected_epicenter)-1,'long']

        epi=dl.Marker(position=[lat, long], icon={
                "iconUrl": "/assets/epicentre.png",
                "iconSize": [50, 50],
                "iconAnchor": [20, 36]
            }, children=[
                dl.Tooltip("epicenter")])


        epiover=dl.Overlay(dl.LayerGroup(epi), name="épicentre", checked=True)
        circleover=dl.Overlay(dl.LayerGroup(circle), name="ponts", checked=True)
        a=[epiover,circleover]

    
                     
#----------------CREATE THE COLOR CODE----------------------------------------
        for i in range(0, len(df)):

                df["cla"][i]="Pont" +str(int(i+1))
                
        df.sort_values(by="mdf")

#-----------------------CREATE BAR PLOT----------------------------------------
        type_etat_dommage=["None", "Slight", "Moderate", "Extensive", "Complete"]


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

        fig1.update_layout(title_text='Number of Bridges by Damage State',
                       xaxis_tickangle=-45,yaxis_title="Number of Bridges")

#        pertes=np.round(int(sum(df["ls"])),0)

    return  a, fig1 #html.P("Economic losses: " +str(pertes) +" K$")



@app.callback(
                [Output(component_id='my-output2', component_property='children'),
                 Output('histo2', 'figure'),
#                 Output("perte_faible", "children")
                 ],
                [Input('select_epicentre', 'value'),
                 Input('select_magnitude', 'value')]
)

def update_graph_low(selected_epicenter,selected_magnitude):

    if selected_epicenter is not None and selected_magnitude is not None:

#---------------SELECT DATAFRAME BASED ON EPICENTER AND MAGNITUDE--------------
        params_sqlalchemy1= "postgresql+psycopg2://%s:%s@%s:5432/%s" % ("postgres",
                                                      "xxxxx",
                                                      "localhost",
                                                      "quebec2")

        engine1= create_engine(params_sqlalchemy1)
        
        file_name = 'epi'+selected_epicenter+'_M'+selected_magnitude+'_low'
        

        df = pd.read_sql_table(file_name, engine1)

#---------------------------------color------------------------
        col = []
        for row in df['Damage_State']:
                if row=="None" :    col.append('blue')
                elif row=="Slight":   col.append('green')
                elif row=="Moderate":  col.append('yellow')
                elif row=="Extensive":  col.append('orange')
                elif row=="Complete":  col.append('red')
        
        df["col"]= col    

        sol = []
        for row in df['Classe_Sismique']:
                if row=="A" :    sol.append('Hard rock')
                elif row=="B":   sol.append('Rock')
                elif row=="C":  sol.append('Very dense soil and soft rock')
                elif row=="D":  sol.append('Stiff soil')
                elif row=="E":  sol.append('Soft soil')
        
        df["sol"]= sol        

        traf = []
        for row in df['Damage_State']:
                if row=="None" :    traf.append('Open to normal traffic - no restrictions')
                elif row=="Slight":   traf.append('Open to normal traffic- no restrictions')
                elif row=="Moderate":  traf.append('Open to limited traffic - speed/weight/lane restrictions')
                elif row=="Extensive":  traf.append('Emergency vehicles only - speed/weight/lane restrictions')
                elif row=="Complete":  traf.append('Closed until shored/braced - potential for collapse')
        
        df["traf"]= traf 

        lats = df.lat
        lons = df.long
        cl = df.Classe_Sismique
        bridge = df.Class
        pic = list(df["Pictures"])        
        Ins_pri=list(df["Inspection_Priority"])
        temp=list(df["Damage_State"])
        mdf=list(df["MRD_pour"])
        p_r=list(df["Priority_Rank"])
        St_dev=list(df["St_Dev_DR"])
        
#        remp=np.round(np.array(df["Replacement_cost"])/1000)
#        Loss=np.round(np.array(df["Economic_Loss"])/1000)

        pga=list(df["PGA"])
        fiches=list(df["fiches2"]) 

        df = pd.DataFrame(columns=["lat", "lon", "cla", "col","ip","tp","mdf","pr","st","pga", "fi", "pic", "bri", "sol", "tra"], data=np.column_stack((lats, lons, cl, col, Ins_pri,temp,mdf,p_r,St_dev,pga,fiches, pic, bridge, sol, traf)))
        df["chemin"]=df["col"]

        for i in range(0,len(df.chemin)):
            if df.fi[i] !=0:
                df["chemin"][i]='/assets/inventaire_structure/' +str(df.fi[i])+'.JPG'
            else:
                df["chemin"][i]=='/assets/inventaire_structure/' +str(df.fi[i])+'.jpg'

# Create markers from data frame.


        circle = [dl.Circle(center=[row["lat"], row["lon"]],radius=200, color=row["col"],children=[
            dl.Tooltip("Bridge"),
            dl.Popup([
                html.Img(src= row["pic"], width="300px"),
                html.A("Link to the MTQ technical file ", href=row["chemin"], target="_blank", className= "text-center"),
                html.H5("Soil characteristics" ,className= "text-center  font-weight-bold" ),
                html.H6(["Peak ground acceleration: " + str(row["pga"]) + " m/s", html.Sup("2")],className= "text-center" ), 
                html.H6("Ground profil name: " + row["sol"], className= "text-center" ),
                html.H5("Bridge characteristics",className= "text-center  font-weight-bold" ),
                html.H6("Bridge class: " + str(row["bri"]),className= "text-center" ),
                html.H6("Damage state: " + row["tp"],className= "text-center" ),
                html.H6("Likely post-event traffic state: " + row["tra"],className= "text-center" ),
                html.H6("Inspection priority: " + row["ip"],className= "text-center" ),
                html.H6("Priority rank: " + str(row["pr"]),className= "text-center" ),
                html.H6("Mean damage factor in %: " + str(row["mdf"]),className= "text-center" ),
                html.H6("Standard deviation: " + str(row["st"]), className= "text-center"),
#                html.H6("Economic loss: " + str(row["ls"])+" k$",className= "text-center" ),
#                html.H6("Replacement cost: " + str(row["rmp"])+" k$", className= "text-center"),
                
            ], maxWidth="300px", autoPan=True)]) for i, row in df.iterrows()]



#create epicenter

        df2 = pd.read_sql_table('epicentre', engine1)
        lat=df2.at[float(selected_epicenter)-1,'lat']
        long=df2.at[float(selected_epicenter)-1,'long']

        epi=dl.Marker(position=[lat, long], icon={
                "iconUrl": "/assets/epicentre.png",
                "iconSize": [50, 50],
                "iconAnchor": [20, 36]
            }, children=[
                dl.Tooltip("epicenter")])


        epiover=dl.Overlay(dl.LayerGroup(epi), name="épicentre", checked=True)
        circleover=dl.Overlay(dl.LayerGroup(circle), name="ponts", checked=True)
        a=[epiover,circleover]

    
                     
#----------------CREATE THE COLOR CODE----------------------------------------
        for i in range(0, len(df)):

                df["cla"][i]="Pont" +str(int(i+1))
                
        df.sort_values(by="mdf")

#-----------------------CREATE BAR PLOT----------------------------------------
        type_etat_dommage=["None", "Slight", "Moderate", "Extensive", "Complete"]


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

        fig1.update_layout(title_text='Number of Bridges by Damage State',
                       xaxis_tickangle=-45,yaxis_title="Number of Bridges")

#        pertes=np.round(int(sum(df["ls"])),0)

    return  a, fig1 #html.P("Economic Losses: " +str(pertes) +" K$")


@app.callback(
                [Output(component_id='my-output3', component_property='children'),
                 Output('histo3', 'figure'),
#                 Output("perte_élévé", "children")
                 ],

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
                if row=="None" :    col.append('blue')
                elif row=="Slight":   col.append('green')
                elif row=="Moderate":  col.append('yellow')
                elif row=="Extensive":  col.append('orange')
                elif row=="Complete":  col.append('red')
        
        df["col"]= col        

        sol = []
        for row in df['Classe_Sismique']:
                if row=="A" :    sol.append('Hard rock')
                elif row=="B":   sol.append('Rock')
                elif row=="C":  sol.append('Very dense soil and soft rock')
                elif row=="D":  sol.append('Stiff soil')
                elif row=="E":  sol.append('Soft soil')
        
        df["sol"]= sol

        traf = []
        for row in df['Damage_State']:
                if row=="None" :    traf.append('Open to normal traffic - no restrictions')
                elif row=="Slight":   traf.append('Open to normal traffic- no restrictions')
                elif row=="Moderate":  traf.append('Open to limited traffic - speed/weight/lane restrictions')
                elif row=="Extensive":  traf.append('Emergency vehicles only - speed/weight/lane restrictions')
                elif row=="Complete":  traf.append('Closed until shored/braced - potential for collapse')
        
        df["traf"]= traf 
        
        lats = df.lat
        lons = df.long
        cl = df.Classe_Sismique
        bridge = df.Class
        pic = list(df["Pictures"])        
        Ins_pri=list(df["Inspection_Priority"])
        temp=list(df["Damage_State"])
        mdf=list(df["MRD_pour"])
        p_r=list(df["Priority_Rank"])
        St_dev=list(df["St_Dev_DR"])
        
#        remp=np.round(np.array(df["Replacement_cost"])/1000)
#        Loss=np.round(np.array(df["Economic_Loss"])/1000)

        pga=list(df["PGA"])
        fiches=list(df["fiches2"]) 

        df = pd.DataFrame(columns=["lat", "lon", "cla", "col","ip","tp","mdf","pr","st","pga", "fi", "pic", "bri", "sol", "tra"], data=np.column_stack((lats, lons, cl, col, Ins_pri,temp,mdf,p_r,St_dev,pga,fiches, pic, bridge, sol, traf)))
        df["chemin"]=df["col"]

        for i in range(0,len(df.chemin)):
            if df.fi[i] !=0:
                df["chemin"][i]='/assets/inventaire_structure/' +str(df.fi[i])+'.JPG'
            else:
                df["chemin"][i]=='/assets/inventaire_structure/' +str(df.fi[i])+'.jpg'

# Create markers from data frame.


        circle = [dl.Circle(center=[row["lat"], row["lon"]],radius=200, color=row["col"],children=[
            dl.Tooltip("Bridge"),
            dl.Popup([
                html.Img(src= row["pic"], width="300px"),
                html.A("Link to the MTQ technical file ", href=row["chemin"], target="_blank", className= "text-center"),
                html.H5("Soil characteristics" ,className= "text-center  font-weight-bold" ),
                html.H6(["Peak ground acceleration: " + str(row["pga"]) + " m/s", html.Sup("2")],className= "text-center" ), 
                html.H6("Ground profil name: " + row["sol"], className= "text-center" ),
                html.H5("Bridge characteristics",className= "text-center  font-weight-bold" ),
                html.H6("Bridge class: " + str(row["bri"]),className= "text-center" ),
                html.H6("Damage state: " + row["tp"],className= "text-center" ),
                html.H6("Likely post-event traffic state: " + row["tra"],className= "text-center" ),
                html.H6("Inspection priority: " + row["ip"],className= "text-center" ),
                html.H6("Priority rank: " + str(row["pr"]),className= "text-center" ),
                html.H6("Mean damage factor in %: " + str(row["mdf"]),className= "text-center" ),
                html.H6("Standard deviation: " + str(row["st"]), className= "text-center"),
 #               html.H6("Economic loss: " + str(row["ls"])+" k$",className= "text-center" ),
 #               html.H6("Replacement cost: " + str(row["rmp"])+" k$", className= "text-center"),
                
            ], maxWidth="300px", autoPan=True)]) for i, row in df.iterrows()]



#create epicenter

        df2 = pd.read_sql_table('epicentre', engine1)
        lat=df2.at[float(selected_epicenter)-1,'lat']
        long=df2.at[float(selected_epicenter)-1,'long']

        epi=dl.Marker(position=[lat, long], icon={
                "iconUrl": "/assets/epicentre.png",
                "iconSize": [50, 50],
                "iconAnchor": [20, 36]
            }, children=[
                dl.Tooltip("epicenter")])


        epiover=dl.Overlay(dl.LayerGroup(epi), name="épicentre", checked=True)
        circleover=dl.Overlay(dl.LayerGroup(circle), name="ponts", checked=True)
        a=[epiover,circleover]

    
                     
#----------------CREATE THE COLOR CODE----------------------------------------
        for i in range(0, len(df)):

                df["cla"][i]="Pont" +str(int(i+1))
                
        df.sort_values(by="mdf")

#-----------------------CREATE BAR PLOT----------------------------------------
        type_etat_dommage=["None", "Slight", "Moderate", "Extensive", "Complete"]


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

        fig1.update_layout(title_text='Number of Bridges by Damage State',
                       xaxis_tickangle=-45,yaxis_title="Number of Bridges")

#        pertes=np.round(int(sum(df["ls"])),0)

    return  a, fig1 #html.P("Economic Losses: " +str(pertes) +" K$")
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

app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)(toggle_modal)
#--------------final-------------------------------------------
            
if __name__ == "__main__":
    app.run_server(debug=False)