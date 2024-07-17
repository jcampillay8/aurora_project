import dash
import dash_bootstrap_components as dbc
from dash import Dash, dash_table, html, dcc, callback, Input, Output, State, callback
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
import dash_daq as daq
from datetime import date
from django_pandas.io import read_frame
from django.contrib.auth.decorators import login_required
import plotly.graph_objects as go
from django.utils import timezone
import base64
import datetime    
import io
import os

import pandas as pd





def input_five_cards(input_card1,input_card2,input_card3,input_card4,input_card5,id_status_card1,id_status_card2,id_status_card3,id_status_card4,id_status_card5,label_card1,label_card2,label_card3,label_card4,label_card5):
    fig1 = go.Figure(go.Indicator(
        value = input_card1,
        title = {"text": f"{label_card1}"},
    ))

    fig2 = go.Figure(go.Indicator(
        value = input_card2,
        title = {"text": f"{label_card2}"},
    ))

    fig3 = go.Figure(go.Indicator(
        value = input_card3,
        title = {"text": f"{label_card3}"},
    ))

    fig4 = go.Figure(go.Indicator(
        value = input_card4,
        title = {"text": f"{label_card4}"},
    ))

    fig5 = go.Figure(go.Indicator(
        value = input_card5,
        title = {"text": f"{label_card5}"},
    ))

    card1 = dbc.Card(
        dcc.Graph(figure=fig1, style={"height": "100%", "width": "100%"}),
        style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
    )

    card2 = dbc.Card(
        dcc.Graph(figure=fig2, style={"height": "100%", "width": "100%"}),
        style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
    )

    card3 = dbc.Card(
        dcc.Graph(figure=fig3, style={"height": "100%", "width": "100%"}),
        style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
    )

    card4 = dbc.Card(
        dcc.Graph(figure=fig4, style={"height": "100%", "width": "100%"}),
        style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
    )

    card5 = dbc.Card(
        dcc.Graph(figure=fig5, style={"height": "100%", "width": "100%"}),
        style={"height": "300px", "width":"250px", "margin-left":"20px","margin-right":"20px"}
    )
    return[
        dbc.Row([
            dbc.Col(html.Div(style={'height': '40px'}), width=12)
        ]),
        dbc.Row([
            dbc.Col((html.Div(style={'height': '20px'})),md=12, lg=1),
            dbc.Col((dbc.Row([
                dbc.Col((html.Div(style={'height': '20px'})),md=12, lg=1),
                dbc.Col((html.Div(card1 ,id='id_status_card1')),md=12, lg=2),
                dbc.Col((html.Div(card2 ,id='id_status_card2')),md=12, lg=2),
                dbc.Col((html.Div(card3 ,id='id_status_card3')),md=12, lg=2),
                dbc.Col((html.Div(card4 ,id='id_status_card4')),md=12, lg=2),
                dbc.Col((html.Div(card5 ,id='id_status_card5')),md=12, lg=2),
                dbc.Col((html.Div(style={'height': '20px'})),md=12, lg=1),
            ])),md=12, lg=12),
            dbc.Col((html.Div(style={'height': '20px'})),md=12, lg=1),
        ])
    ]