#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 22:49:06 2020

@author: lidia
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

def plot_heatmap_chart(analysis_result):
    """
    Plots a heatmap chart in order to represent a MediasEvolution analysis.
    The data to show are the number of post interactions during a specific
    period of time.

    Parameters
    ----------
    analysis_result : dict
        It's the dict which contains the MediasEvolution analysis results.

    Returns
    -------
    A heatmap chart.
    """
    fig = px.imshow([analysis_result["like_count"], analysis_result["comment_count"]],
                    labels=dict(color="Nº de interacciones"),
                    color_continuous_scale=["#00d5ea", "#007cea", "#a983e3", "#8c59d9", "#6f2ed0", "#330064"],
                    x=analysis_result["date"],
                    y=["Me gusta", "Comentarios"]
                   )
    fig.update_xaxes(side="top")
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
            dbc.NavLink("Ayuda", href="/page-8", id="page-8-link"),
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
        # ----------------------- NEW USER TO GET DATA -----------------------
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
                        children=["Descripción para obtener los datos de un nuevo usuario"],
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
        
        # --------------------- PROFILE EVOLUTION ANALYSIS --------------------
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
                        children=["Descripción del primer análisis"],
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
    Output("analysis-results", "figure"),
    [Input("analysis-start-date-dropdown", "value"),
     Input("analysis-end-date-dropdown", "value"),
     Input("analysis-users-dropdown", "value"),
     Input("analysis-social-media-dropdown", "value"),
     Input("perform-analysis-button", "n_clicks"),
     Input("url", "pathname"),
     Input("popularity-mode-dropdown", "value")]
)
def update_analysis_results(start_date, end_date, user, social_media, clicks, path, popularity):
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
        It's the number of clicks of the perform analysis button .

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
                if (result != None): return result 
            elif (auxdata_attr.current_page == 'profile-activity'):
                analysis_result = mainops_attr.perform_analysis(user, 'profile_activity', social_media, start_date, end_date)
                result = plot_waterfall_chart(analysis_result)
                if (result != None): return result 
            elif (auxdata_attr.current_page == 'medias-evolution'):
                analysis_result = mainops_attr.perform_analysis(user, 'media_evolution', social_media, start_date, end_date)
                result = plot_heatmap_chart(analysis_result)
                if (result != None): return result 
            elif (auxdata_attr.current_page == "medias-popularity"): 
                analysis_result = mainops_attr.perform_analysis(user, 'media_popularity', social_media, start_date, end_date, popularity)
                result = plot_bar_chart(analysis_result)
                if (result != None): return result 
    
        return go.Figure()
    return go.Figure()
    
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 9)],
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
        return True, False, False, False, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1,9)]

@app.callback([Output("new-user-page", "style"),
               Output("analysis-page", "style"),
                Output("page-1-link", "style"),
                Output("page-2-link", "style"),
                Output("page-3-link", "style"),
                Output("page-4-link", "style"),
                Output("page-5-link", "style"),
                Output("page-6-link", "style"),
                Output("page-7-link", "style"),
                Output("page-8-link", "style"),
                Output("analysis-title", "children"),
                Output("popularity-mode-label", "style"),
                Output("popularity-mode-dropdown", "style")], 
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
    non_selected_option_style = {"display":"none"}
    if pathname in ["/", "/page-1"]:
        auxdata_attr.current_page = "new-user"
        return CONTENT_STYLE, non_selected_option_style, selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, "", non_selected_option_style, non_selected_option_style
    elif pathname == "/page-2":
        auxdata_attr.current_page = "profile-evolution"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                selected_option, non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                "Análisis de la evolución del perfil", non_selected_option_style, non_selected_option_style
    elif pathname == "/page-3":
        auxdata_attr.current_page = "profile-activity"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                non_selected_option, selected_option, non_selected_option,  \
                non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, "Análisis de la evolución de la actividad", \
                non_selected_option_style, non_selected_option_style
    elif pathname == "/page-4":
        auxdata_attr.current_page = "medias-evolution"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                non_selected_option, non_selected_option, selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                non_selected_option, "Análisis de la evolución del interés de las publicaciones", \
                non_selected_option_style, non_selected_option_style
    elif pathname == "/page-5":
        auxdata_attr.current_page = "medias-popularity"
        return non_selected_option_style, CONTENT_STYLE, non_selected_option, \
                non_selected_option, non_selected_option, non_selected_option, \
                selected_option, non_selected_option, non_selected_option, \
                non_selected_option, "Análisis de la popularidad de las publicaciones" \
                , popularity_label, popularity_dropdown


#---------------------------------- FLASK SERVER ---------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)