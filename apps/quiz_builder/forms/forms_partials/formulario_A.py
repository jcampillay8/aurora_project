import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, callback, dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash  
import dash_daq as daq
from datetime import date
from dash.dash_table.Format import Group
import pandas as pd
from django.conf import settings
from apps.formularios.forms_partials.forms_dash_partials import input_text,input_dropdown_field, input_double_text, input_text_area, input_drag_drop_select_file


lista_opciones_drowpdown = ['New York','Seattle',"San Francisco"]



def form_partials_A(selected_formulario):
    return[
    html.Br(),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((
            dcc.Markdown(f''' ##### Formulario A ''', className="text-center"),
        ),width=10),
        dbc.Col((),width=1),
    ]),
    dbc.Row([
            dbc.Col((),width=1),
            dbc.Col(input_text('Nombre Trabajador','id_first_name_worker')),
            dbc.Col((),width=1),
        ]),
    dbc.Row([
            dbc.Col((),width=1),
            dbc.Col(input_text('Apellido Trabajador','id_last_name_worker')),
            dbc.Col((),width=1),
        ]),
    dbc.Row([
            dbc.Col((),width=1),
            dbc.Col((input_dropdown_field('Ciudades',lista_opciones_drowpdown,'id_lista_dropdown')),width=10),
            dbc.Col((),width=1),
        ]),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((input_double_text('Nombre Producto','Cantidad','id_input_double_text_left','id_input_double_text_right')),width=10),
        dbc.Col((),width=1),
    ]),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((input_text_area('Descripción Producto','id_text_area')),width=10),
        dbc.Col((),width=1),
    ]),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((input_drag_drop_select_file()),width=10),
        dbc.Col((),width=1),
    ])
        
    ]


