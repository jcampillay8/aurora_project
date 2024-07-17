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
from apps.formularios.forms_partials.forms_dash_partials import input_text,input_dropdown_field, input_double_text, input_text_area, input_drag_drop_select_file, button_action


def form_partials_B(selected_formulario):
    return[
    html.Br(),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((
            dcc.Markdown(f''' ##### Formulario B ''', className="text-center"),
        ),width=10),
        dbc.Col((),width=1),
    ]),
    dbc.Row([
            dbc.Col((),width=1),
            dbc.Col(input_text('Fecha Factura','id_Fecha_Factura')),
            dbc.Col((),width=1),
        ]),
    dbc.Row([
            dbc.Col((),width=1),
            dbc.Col(input_text('Número Factura','id_Factura_Num')),
            dbc.Col((),width=1),
        ]),
    dbc.Row([
        dbc.Col((),width=1),
        dbc.Col((button_action('submit','id_submit_button')),width=10),
        dbc.Col((),width=1),
    ]),
    html.Br(),
    html.Div(id='output-message')
    ]







