#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file includes the required Dash callbacks to run the interface.

@author: Lidia Sánchez Mérida
"""
#---------------------------------- LIBRARIES ---------------------------------
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from plotly import graph_objects as go
import plotly.express as px

import pandas as pd 
from datetime import datetime
import sys
sys.path.append("src")

#-------------------------------- AUXILIARY CLASS ------------------------------
class AuxData():
    def __init__(self):
        self.current_page = None
        self.n_clicks = 0
        self.popularity_mode = "best"
        self.sentiment_analysis = "comment_sentiment_analysis"

#-------------------------------- APP ATTRIBUTES ------------------------------
auxdata_attr = AuxData()

from mongodb import MongoDB
mongodb_attr = MongoDB("profiles")

from main_ops import MainOperations
mainops_attr = MainOperations()
#------------------------------- PYTHON FUNCTIONS -----------------------------
def get_avalaible_dates(collection="profiles"):
    """
    Recovers the dates in which the collection received new data in order to plot
    them in the dropdown menus to choose the start date and the end date to perform
    an analysis.

    Parameters
    ----------
    collection : str, optional
        It's the Mongo collection from which the dates will be recovered. 
        The default is "profiles".

    Returns
    -------
    A list of strings whose each item is a date in which there are downloaded data.
    """
    # Set the collection to recover the dates
    mongodb_attr.set_collection(collection)
    # Get the avalaible dates to perform an analysis. Default analysis is Profiles Evolution
    avalaible_dates = mongodb_attr.get_records("get_dates")
    # Format them from datetime to string
    avalaible_string_dates = []
    for date in avalaible_dates:
        avalaible_string_dates.append({"label":datetime.strftime(date["date"], "%d-%m-%Y"), 
                                "value":datetime.strftime(date["date"], "%d-%m-%Y")})
    
    return avalaible_string_dates

def plot_filled_area_chart(analysis_result):
    """
    Plots a filled area chart in order to represent a ProfilesEvolution analysis.
    The data to show are the number of followers, followings and posts over a specific
    period of time. 

    Parameters
    ----------
    analysis_result : dict
        It's the dict which contains the ProfilesEvolution analysis results.

    Returns
    -------
    A filled area chart.
    """
    if (len(analysis_result) > 0):
        # Initialize the plot object
        fig = go.Figure()
        # 1. Add the Followers values
        fig.add_trace(go.Scatter(
            x=analysis_result["date"], y=analysis_result["n_followers"],
            line=dict(width=2.0, color="#330064"), mode="lines+markers",
            stackgroup='one',
            name="Seguidores"
        ))
        # 1. Add the Followings values
        fig.add_trace(go.Scatter(
            x=analysis_result["date"], y=analysis_result["n_followings"],
            line=dict(width=2.0, color="#007cea"), mode="lines+markers",
            stackgroup='one',
            name="Seguidos"
        ))
        # 1. Add the Posts values
        fig.add_trace(go.Scatter(
            x=analysis_result["date"], y=analysis_result["n_medias"],
            line=dict(width=2.0, color="#00d5ea"), mode="lines+markers",
            stackgroup='one',
            name="Publicaciones"
        ))
        # Delete Y axis
        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_layout(title="Evolución del número de seguidores, seguidos y publicaciones.")
        return fig

def plot_waterfall_chart(analysis_result):
    """
    Plots a waterfall chart in order to represent a ProfilesActivity analysis.
    The data to show are the number of uploaded posts during a specific
    period of time as well as the difference of uploaded media between each date.

    Parameters
    ----------
    analysis_result : dict
        It's the dict which contains the ProfilesActivity analysis results.

    Returns
    -------
    A waterfall chart.
    """
    # Compute the differences between each number of posts
    differences = []
    differences.append("")
    for i in range(1, len(analysis_result["n_medias"])):
        diff = analysis_result["n_medias"][i]-analysis_result["n_medias"][i-1]
        if (diff > 0): differences.append("+"+str(diff))
        elif (diff == 0): differences.append(str(diff))
        else: differences.append("-"+str(diff))
    
    fig = go.Figure(go.Waterfall(
        name = "Nº de publicaciones", orientation = "v",
        x=analysis_result["date"],
        textposition = "inside",
        text = differences,
        y = analysis_result["n_medias"],
        increasing = {"marker":{"color":"rgb(169, 131, 227)", "line":{"color":"#6d4e8c", "width":2}}},
        connector = {"line":{"color":"#330064"}},
    ))

    fig.update_layout(
        title = "Evolución del número de publicaciones",
        showlegend = True
    )
    
    return fig

def plot_funnel_chart(analysis_result):
    """
    Plots a funnel chart in order to represent a MediasEvolution analysis.
    The data to show are the number of post interactions during a specific
    period of time.

    Parameters
    ----------
    analysis_result : dict
        It's the dict which contains the MediasEvolution analysis results.

    Returns
    -------
    A funnel chart.
    """    
    fig = go.Figure()
    fig.add_trace(go.Funnel(
        name = 'Me gusta',
        x = analysis_result["like_count"],
        y = analysis_result["date"],
        textinfo = "value")
    )
    fig.add_trace(go.Funnel(
        name = 'Comentarios',
        x = analysis_result["comment_count"],
        y = analysis_result["date"],
        textinfo = "value")
    )
    fig.update_layout(
        title = "Evolución del interés de las publicaciones",
        showlegend = True
    )
    return fig

def plot_bar_chart(analysis_result):
    """
    Plots a bar chart in order to represent a MediasPopularity analysis in order
    to show the ranking of the best/worst posts based on the number of interactions.

    Parameters
    ----------
    analysis_result : dict
        It's the dict which contains the MediasPopularity analysis results.

    Returns
    -------
    A bar chart.
    """
    df = pd.DataFrame()
    df["Posición"] = list(range(1, len(analysis_result)+1))
    df["Interacciones"] = analysis_result
    fig = px.bar(df, x="Posición", y="Interacciones", color='Interacciones',
                 color_continuous_scale=["#00d5ea", "#007cea", "#a983e3", "#8c59d9", "#6f2ed0", "#330064"])
    fig.update_layout(
        title = "Las 10 publicaciones más populares." if auxdata_attr.popularity_mode == "best" else "Las 10 publicaciones menos populares.",
        showlegend = True
    )
    return fig

def plot_pie_chart(analysis_result):
    """
    Plots a pie chart in order to represent a sentiment analysis based on post
    comments or post titles in order to show the number of positive, neutral
    and negative texts as well as their related polarity or confidence degree
    for each different sentiment.

    Parameters
    ----------
    analysis_result : dict
        It's the dict which contains the sentiment analysis results.

    Returns
    -------
    A pie chart.
    """
    df = pd.DataFrame()
    df["Sentimiento"] = ["Positivo", "Neutral", "Negativo"]
    df["Número de textos"] = analysis_result["sentiments"]
    polarity_percentaje = [value*100 for value in analysis_result["degrees"]]
    df["Polaridad"] = polarity_percentaje
    fig = go.Figure(go.Pie(
        name="",
        values = df['Número de textos'],
        labels = df['Sentimiento'],
        customdata=df['Polaridad'],
        hovertemplate = "Sentimiento: %{label} <br>Nº de textos: %{value} </br> Polaridad: %{customdata}%"
    ))
    fig.update_traces(
        marker=dict(colors=["#00d5ea", "#8c59d9", "#330064"])
    )
    fig.update_layout(
        title = "Análisis de sentimientos de los comentarios de las publicaciones." \
            if "comment" in auxdata_attr.sentiment_analysis  else "Análisis de sentimientos de los títulos de las publicaciones.",
        showlegend = True
    )
    
    return fig

def plot_heatmap_chart(analysis_result):
    """
    Plots a funnel-heatmap chart in order to represent the number of identified
    friends and haters based on the sentiment analysis of the post comments of 
    a specific user in a particular period of time.

    Parameters
    ----------
    analysis_result : dict
        It's the dict which contains the user behaviours analysis results.

    Returns
    -------
    A funnel-heatmap chart.
    """
    fig = go.Figure()
    fig.add_trace(go.Funnel(
        name = 'Amigos',
        x = analysis_result["likers"],
        textinfo = "value",
        opacity = 0.65, 
        marker = {"color": ["#007cea"], "line": {"width": [5], "color": ["#00d5ea"]}})
    )
    fig.add_trace(go.Funnel(
        name = 'Haters',
        x = analysis_result["haters"],
        textinfo = "value",
        opacity = 0.65, 
        marker = {"color": ["#330064"], "line": {"width": [5], "color": ["#a983e3"]}})
    )
    fig.update_layout(
        title = "Análisis de los patrones de comportamiento de los miembros de la comunidad.",
        showlegend = True
    )
    fig.update_yaxes(visible=False, showticklabels=False)
    return fig

#---------------------------------- APP SETTINGS ---------------------------------
# Flask application
from flask import Flask
server = Flask(__name__)
app = dash.Dash(
    server=server,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Sistema M&V'

# The style for the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "rgb(255 255 255)",
}

# The style fo the main content
CONTENT_STYLE = {
    "display":"inherit",
    "margin-left": "200px",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#---------------------------------- APP VIEW ---------------------------------
# Sidebar
sidebar = html.Div([
        html.Img(
            src="assets/logo_transparent.png",
            style={"width":"100%", "margin-bottom":"-25%"}
        ),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink("Usuario en estudio", href="/page-1", id="page-1-link"),
            dbc.NavLink("Evolución del perfil", href="/page-2", id="page-2-link"),
            dbc.NavLink("Actividad del usuario", href="/page-3", id="page-3-link"),
            dbc.NavLink("Evolución de las publicaciones", href="/page-4", id="page-4-link"),
            dbc.NavLink("Popularidad de las publicaciones", href="/page-5", id="page-5-link"),
            dbc.NavLink("Análisis de sentimientos", href="/page-6", id="page-6-link"),
            dbc.NavLink("Patrones de comportamiento", href="/page-7", id="page-7-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Prepare the dates to choose for the first and default analysis
dates_to_print = get_avalaible_dates()

# Layout
app.layout = html.Div([
        dcc.Location(id="url"), 
        sidebar,
        # ----------------------- NEW USER TO GET DATA ----------------------- #
        html.Div(
            id="new-user-page",
            style=CONTENT_STYLE,
            children=[
                html.Div([
                    html.H1(
                        children=["Sistema de monitorización y vigilancia de RRSS"],
                        style={"text-align": "left"},
                    ),
                    html.H3(
                        id="new-userpage-title",
                        children=["Recopilación de datos de un usuario"],
                        style={"text-align": "left"},
                    ),
                    html.P(
                        id="new-user-description",
                        children=["En esta vista se puede especificar el nombre de usuario "+
                                  "relativo a la cuenta que se desee estudiar así como las redes "+
                                  "sociales de las que se obtendrá la suficiente información como para "+
                                  "realizar los diversos análisis que se proponen en esta plataforma.\n"+
                                  "La descarga de datos relativos al usuario especificado se realizará en segundo plano "+
                                  "de modo que permita la interacción con la plataforma y la realización de análisis sobre "+
                                  "otros usuarios."],
                    ),
                    html.P(
                        id="new-user-description-2",
                        children=["La descarga de datos relativos al usuario especificado se realizará en segundo plano "+
                                  "de modo que permita la interacción con la plataforma y la realización de análisis sobre "+
                                  "otros usuarios."],
                    ),
                ]),
                html.Div(
                id="new-user-filter-div",
                className="six columns pretty_container",
                style={"width":"60%", "margin-left":"-1px"},
                children=[
                    html.Div(children=[
                        html.P(children="Nuevo usuario", style={"display":"inline-block"}),
                        html.P(children="Redes sociales", style={"display":"inline-block", "margin-left":"270px"}),
                    ]),
                    dcc.Input(id="new-user-input", type="text", placeholder="Nombre del usuario", style={"display":"inline-block"}),
                    dcc.Checklist(
                        options=[
                            {'label': 'Instagram', 'value': 'instagram'},
                        ],
                        inputStyle={"margin":"10px"},
                        value=['instagram'],
                        style={"display":"inline-block", "margin-left":"150px"}
                    ),
                    html.Button('Recopilar datos', id='enable-new-user', 
                    style={'background':'#8c59d9', 'margin-top':'20px', 'color':'white'}),
                    html.P(children="", id="user-result"),
                ]),
        ]),
        
        # --------------------------- ANALYSIS VIEWS -------------------------- #
        html.Div(
            id="analysis-page",
            style=CONTENT_STYLE,
            children=[
                html.Div([
                    html.H1(
                        children=["Sistema de monitorización y vigilancia de RRSS"],
                        style={"text-align": "left"},
                    ),
                    html.H3(
                        id="analysis-title",
                        style={"text-align": "left"},
                    ),
                    html.P(
                        id="analysis-description",
                        children=[""],
                    ),
                    html.P(
                        id="analysis-instructions",
                        children=[""],
                    ),
                ]),
                html.Div(
                    id="analysis-filter-div",
                    className="six columns pretty_container",
                    style={"width":"100%", "margin-left":"-1px"},
                    children=[
                        html.Div(children=[
                            html.P(children="Fecha de inicio", style={"display":"inline-block", "width":"20%", "margin-right":"5%"}),
                            html.P(children="Fecha final", style={"display":"inline-block", "width":"20%", "margin-right":"5%"}),
                            html.P(children="Usuario a estudiar", style={"display":"inline-block", "width":"20%", "margin-right":"5%"}),
                            html.P(children="Red social", style={"display":"inline-block", "width":"20%", "margin-right":"5%"}),
                        ]),
                        dcc.Dropdown(
                            options=dates_to_print,
                            id="analysis-start-date-dropdown",
                            value=dates_to_print[0]["value"],
                            style={"display":"inline-block", "width":"20%", "margin-right":"5%"}
                        ),
                        dcc.Dropdown(
                            options=dates_to_print,
                            id="analysis-end-date-dropdown",
                            value=dates_to_print[0]["value"],
                            style={"display":"inline-block", "width":"20%", "margin-right":"5%"}
                        ),
                        dcc.Dropdown(
                            options=[{"label":"Audi Spain", "value":"audispain"},
                                   {"label":"Carlos Ríos", "value":"carlosriosq"}],
                            id="analysis-users-dropdown",
                            value="audispain",
                            style={"display":"inline-block", "width":"20%", "margin-right":"5%"}
                        ),
                        dcc.Dropdown(
                            options=[{"label":"Instagram", "value":"Instagram"}],
                            id="analysis-social-media-dropdown",
                            value="Instagram",
                            style={"display":"inline-block", "width":"20%", "margin-right":"5%"}
                        ),
                        html.Div(children=[
                            html.P(id="popularity-mode-label", children="Ranking de publicaciones", style={"display":"none"}),
                        ]),
                        dcc.Dropdown(
                            options=[{"label":"Más populares", "value":"best"}, {"label":"Menos populares", "value":"worst"}],
                            id="popularity-mode-dropdown",
                            value="best",
                            style={"display":"inline-block", "width":"20%", "margin-right":"5%"}
                        ),
                        html.Div(children=[
                            html.P(id="text-sentiments-label", children="Textos a analizar", style={"display":"none"}),
                        ]),
                        dcc.Dropdown(
                            options=[{"label":"Comentarios de publicaciones", "value":"comment_sentiment_analysis"}, 
                                     {"label":"Títulos de publicaciones", "value":"title_sentiment_analysis"}],
                            id="text-sentiments-dropdown",
                            value="comment_sentiment_analysis",
                            style={"display":"inline-block", "width":"20%", "margin-right":"5%"}
                        ),
                        html.Button('Analizar', id='perform-analysis-button', 
                        style={'background':'#8c59d9', 'margin-top':'20px', 'margin-right':'45px', 'color':'white', 'float':'right'}),
                ]),
                html.Div(children=[
                    dcc.Graph(
                        id="analysis-results",
                        className="six columns pretty_container",
                        style={"width":"100%"},
                        figure=dict(
                            data=[dict(x=0, y=0)],
                            layout=dict(
                                paper_bgcolor="#f3f3f1",
                                plot_bgcolor="#f3f3f1",
                                autofill=True,
                            ),
                        ),
                    ),
                ]),
                
                html.Div(
                    id="top-3-popularity",
                    className="six columns pretty_container",
                    style={"width":"100%", "margin-left":"-0px"},
                    children=[
                        html.A(id="first-popularity-post", style={"margin-left":"50px"}, children="Primera publicación", href=""),
                        html.A(id="second-popularity-post", style={"margin-left":"200px"}, children="Segunda publicación", href=""),
                        html.A(id="third-popularity-post", style={"margin-left":"200px"}, children="Tercera publicación", href=""),
                ]),
            ],
        ),
    ])

#---------------------------------- APP CALLBACKS ---------------------------------
@app.callback(
    [Output("user-result", "children"),
    Output("user-result", "style")],
    [Input("enable-new-user", "n_clicks"),
     Input("new-user-input", "value")]
)
def set_user_to_study(clicks, user):
    """
    Saves the username of the account to study later by setting the related 
    attributes of the MainOperations class which will be read by the task server
    when the data are going to be download.

    Parameters
    ----------
    clicks : integer
        It's the number of clicks over the button.
    user : str
        It's the username of the account to analyze.

    Returns
    -------
    A string with the related to message to show the status of the process as well
    as its style.
    """
    if (clicks != None):
        if (clicks > 0):
            set_user = mainops_attr.set_user_to_study(user)
            color = "green"
            message = "El usuario a analizar ha sido actualizado correctamente." 
            if (set_user != user):
                color = "red"
                message = "Ha ocurrido un error durante el proceso y no se ha podido establecer el usuario."
            return message, {"display":"inline-block", "color":color, "margin-top":"10px"}
        return "", {"display":"none"}
    return "", {"display":"none"}
    
@app.callback(
    [Output("analysis-results", "figure"),
     Output("top-3-popularity", "style"),
     Output("first-popularity-post", "href"),
     Output("second-popularity-post", "href"),
     Output("third-popularity-post", "href"),],
    [Input("analysis-start-date-dropdown", "value"),
     Input("analysis-end-date-dropdown", "value"),
     Input("analysis-users-dropdown", "value"),
     Input("analysis-social-media-dropdown", "value"),
     Input("perform-analysis-button", "n_clicks"),
     Input("url", "pathname"),
     Input("popularity-mode-dropdown", "value"),
     Input("text-sentiments-dropdown", "value")]
)
def update_analysis_results(start_date, end_date, user, social_media, 
                            clicks, path, popularity, text_analysis):
    """
    Plots the analysis results which are related to the current page and from the
    provided start and end date, as well as the username to study and the social media
    source of the downloaded user data.

    Parameters
    ----------
    start_date : str
        It's the first date of the analysis.
    end_date : str
        It's the end date of the analysis .
    user : str
        It's the username of the account to study.
    social_media : str
        It's the social media source from the user data will be recovered to
        perform the analysis.
    clicks : integer
        It's the number of clicks of the perform analysis button
    path:
    popularity:
    text_analysis

    Returns
    -------
    The related figure to the chosen analysis.
    """
    if (clicks != None):
        if (clicks > 0 and clicks > auxdata_attr.n_clicks):
            auxdata_attr.n_clicks += 1
            if (auxdata_attr.current_page == 'profile-evolution'):
                analysis_result = mainops_attr.perform_analysis(user, 'profile_evolution', social_media, start_date, end_date)
                result = plot_filled_area_chart(analysis_result)
                if (result != None): return result, {"display":"none"}, "", "", ""
            elif (auxdata_attr.current_page == 'profile-activity'):
                analysis_result = mainops_attr.perform_analysis(user, 'profile_activity', social_media, start_date, end_date)
                result = plot_waterfall_chart(analysis_result)
                if (result != None): return result, {"display":"none"}, "", "", ""
            elif (auxdata_attr.current_page == 'medias-evolution'):
                analysis_result = mainops_attr.perform_analysis(user, 'media_evolution', social_media, start_date, end_date)
                result = plot_funnel_chart(analysis_result)
                if (result != None): return result, {"display":"none"}, "", "", "" 
            elif (auxdata_attr.current_page == "medias-popularity"): 
                analysis_result = mainops_attr.perform_analysis(user, 'media_popularity', social_media, start_date, end_date, popularity)
                auxdata_attr.popularity_mode = popularity
                post_popularity = {"best":["https://www.instagram.com/p/CC_UcwgnZJK/?igshid=lpfow838ccqr",
                               "https://www.instagram.com/p/CGK0lf8HjSn/",
                               "https://www.instagram.com/p/CGKXU0nnm5A/"], 
                    "worst":["https://www.instagram.com/p/CHfgiQwix-C/",
                              "https://www.instagram.com/p/CF2WL3ziB7g/",
                              "https://www.instagram.com/p/CIBklUtCoO1/"]}
                link1 = post_popularity["best"][0] if auxdata_attr.popularity_mode == "best" else post_popularity["worst"][0]
                link2 = post_popularity["best"][1] if auxdata_attr.popularity_mode == "best" else post_popularity["worst"][1]
                link3 = post_popularity["best"][2] if auxdata_attr.popularity_mode == "best" else post_popularity["worst"][2]
                result = plot_bar_chart(analysis_result)
                if (result != None): return result, {"display":"block", "width":"100%", "margin-left":"-0px"}, link1, link2, link3
            elif (auxdata_attr.current_page == "text-sentiments"): 
                analysis_result = mainops_attr.perform_analysis(user, text_analysis, social_media, start_date, end_date)
                auxdata_attr.sentiment_analysis = text_analysis
                result = plot_pie_chart(analysis_result)
                if (result != None): return result, {"display":"none"}, "", "", "" 
            elif (auxdata_attr.current_page == "user-behaviours"): 
                analysis_result = mainops_attr.perform_analysis(user, 'user_behaviours', social_media, start_date, end_date)
                result = plot_heatmap_chart(analysis_result)
                if (result != None): return result, {"display":"none"}, "", "", "" 
    
        return go.Figure(), {"display":"none"}, "", "", ""
    return go.Figure(), {"display":"none"}, "", "", ""
    
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 8)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    """
    Changes the active link of the sidebar menu.

    Parameters
    ----------
    pathname : str
        It's the URL to the current page.

    Returns
    -------
    The URL to the page to plot.
    """
    if pathname == "/":
        return True, False, False, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1,8)]

@app.callback([Output("new-user-page", "style"),
               Output("analysis-page", "style"),
                Output("page-1-link", "style"),
                Output("page-2-link", "style"),
                Output("page-3-link", "style"),
                Output("page-4-link", "style"),
                Output("page-5-link", "style"),
                Output("page-6-link", "style"),
                Output("page-7-link", "style"),
                Output("analysis-title", "children"),
                Output("popularity-mode-label", "style"),
                Output("popularity-mode-dropdown", "style"),
                Output("text-sentiments-label", "style"),
                Output("text-sentiments-dropdown", "style"),
                Output("analysis-description", "children"),
                Output("analysis-instructions", "children")], 
              [Input("url", "pathname")])
def render_page_content(pathname):
    """
    Plots the page related to the provided path.

    Parameters
    ----------
    pathname : str
        It's the path to the page to plot.

    Returns
    -------
    A dict to plot the current page and hide the other ones.
    """
    selected_option = {"color":"white", "background":"#8c59d9", "text-decoration":"none", "margin-bottom":"2%"}
    non_selected_option = {"color":"#6d4e8c", "background":"white", "text-decoration":"none", "margin-bottom":"2%"}
    popularity_label = {"display":"inline-block", "width":"20%", "margin-right":"5%"}
    popularity_dropdown = {"display":"inline-block", "width":"20%", "margin-right":"5%"}
    sentiments_dropdown = {"display":"inline-block", "width":"25%", "margin-right":"5%"}
    non_selected_option_style = {"display":"none"}
    
    profiles_evolution_description = "El principal objetivo de este análisis reside en estudiar si existe "\
                                      "una relación directa entre el número de seguidores, seguidos y contenido publicado."\
                                      "De este modo podrá conocer si a mayor número de publicaciones, existe un mayor número de usuarios "\
                                      "que se suscriben a la cuenta para continuar recibiendo el nuevo contenido que se genere. Asimismo "\
                                      "tendrá la oportunidad de observar si existe un equilibrio entre el número de seguidores y el número "\
                                      "de cuentas que sigue con el objetivo de determinar si el uso de la cuenta es exclusivo para dar a conocer "\
                                      "su contenido, o si por el contrario, también la utiliza para conectar con otros miembros de la red social."
    profiles_activity_description = "En este análisis se muestra la evolución del número publicaciones que ha realizado el usuario dentro del período "\
                                    "de tiempo seleccionado. El objetivo de este estudio consiste en visualizar si existen intervalos de tiempo en los "\
                                    "la actividad del usuario aumenta considerablemente mediante la creación y la publicación de mayor contenido. "\
                                    "De este modo, usted podrá concluir si la cuenta analizada dispone de cierta tendencia de mercado y de estrategias "\
                                    "comerciales para estudiar cuáles son las fechas más prolíferas para dar a conocer sus nuevos productos."
    medias_evolution_description = "El análisis de la evolución de las publicaciones muestra una comparativa entre las principales interacciones que "\
                                    "características de la red social seleccionada con el principal objetivo de determinar el interés que muestran los "\
                                    "miembros de una comunidad hacia el contenido publicado de un usuario en particular durante un período de tiempo. "\
                                    "Así, podrá detectar si existe un incremento o decremento de la popularidad de la cuenta en estudio de modo que le permita "\
                                    "detectar el poder de influencia y su capacidad de distribución de los que dispone este ususario en cuestión."
    medias_popularity_description = "Este estudio realiza un análisis acerca de las interacciones que han recibido las publicaciones de un usuario concreto "\
                                    "durante un período de tiempo con el objetivo de presentar las características de las diez publicaciones más o menos populares. "\
                                    "Dependiendo del medio social escogido, las métricas serán diferentes puesto que cada red social dispone de un conjunto de interacciones "\
                                    "comunes pero también contiene algunas que solo aparecen de forma particular."
    sentiment_analysis_description = "El análisis de sentimientos tiene como principal objetivo el estudio de la bondad de los textos disponibles en la cuenta de usuario seleccionada. "\
                                    "En esta plataforma se posibilita la realización de este tipo de investigación sobre los comentarios y los títulos de las publicaciones. "\
                                    "De este modo, podrá conocer el número de textos clasificados como positivos, neutrales y negativos así como su respectiva polaridad o grado de confianza. "\
                                    "Este dato explica cuán seguro está el modelo de que un determinado texto pertenece al tipo de sentimiento que ha identificado."
    users_behaviours_description = "El análisis de los patrones de comportamiento identifica el número de usuarios que se caracterizan por se más amigables con la cuenta en estudio "\
                                    "así como el número de miembros que se muestran más hostiles, los llamados haters, a partir del análisis de sentimientos realizado a los comentarios de las publicaciones del usuario analizado "\
                                    "durante un período de tiempo determinado. De este modo, este estudio posibilita la identificación de etapas temporales en las que hayan aumentado "\
                                    "el número de un tipo u otro de usuarios con el objetivo de poder combinar sus resultados con los de otros análisis que se proporcionan en esta plataforma "\
                                    "y así comprender los motivos de las diversas reacciones del resto de miembros de la comunidad al contenido publicado."
    instructions = "Para ello es necesario que indique la fecha de inicio y de fin entre las que obtener la información necesaria "\
        "para llevar a cabo este análisis sobre el usuario especificado dentro de una red social concreta."
        
    
    if pathname in ["/", "/page-1"]:
        auxdata_attr.current_page = "new-user"
        return CONTENT_STYLE, non_selected_option_style, selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                "", non_selected_option_style, non_selected_option_style \
                , non_selected_option_style, non_selected_option_style, "", "" 
    elif pathname == "/page-2":
        auxdata_attr.current_page = "profile-evolution"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                selected_option, non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, non_selected_option, \
                "Análisis de la evolución del perfil", non_selected_option_style, non_selected_option_style \
                , non_selected_option_style, non_selected_option_style, profiles_evolution_description, instructions
    elif pathname == "/page-3":
        auxdata_attr.current_page = "profile-activity"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                non_selected_option, selected_option, non_selected_option,  \
                non_selected_option, non_selected_option, non_selected_option, \
                "Análisis de la evolución de la actividad", \
                non_selected_option_style, non_selected_option_style \
                , non_selected_option_style, non_selected_option_style, profiles_activity_description, instructions
    elif pathname == "/page-4":
        auxdata_attr.current_page = "medias-evolution"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                non_selected_option, non_selected_option, selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                "Análisis de la evolución del interés de las publicaciones", \
                non_selected_option_style, non_selected_option_style \
                , non_selected_option_style, non_selected_option_style, medias_evolution_description, instructions 
    elif pathname == "/page-5":
        auxdata_attr.current_page = "medias-popularity"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                selected_option, non_selected_option, non_selected_option, \
                "Análisis de la popularidad de las publicaciones" \
                , popularity_label, popularity_dropdown, non_selected_option_style, non_selected_option_style\
                , medias_popularity_description, instructions+" Asimismo, también podrá seleccionar si desea visualizar las diez publicaciones más o menos populares."
    elif pathname == "/page-6":
        auxdata_attr.current_page = "text-sentiments"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, selected_option, non_selected_option, \
                "Análisis de sentimientos basado en texto" \
                , non_selected_option_style, non_selected_option_style, \
                popularity_label, sentiments_dropdown \
                , sentiment_analysis_description, instructions+" Además, deberá elegir a qué tipo de textos se va a aplicar el análisis de sentimientos, a los comentarios o a los títulos de las publicaciones."
    elif pathname == "/page-7":
        auxdata_attr.current_page = "user-behaviours"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, non_selected_option, selected_option, \
                "Análisis de patrones de comportamiento" \
                , non_selected_option_style, non_selected_option_style, \
                non_selected_option_style, non_selected_option_style, users_behaviours_description, instructions

#---------------------------------- FLASK SERVER ---------------------------------
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)