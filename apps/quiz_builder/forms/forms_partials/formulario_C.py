import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State, MATCH, ALL
from django_plotly_dash import DjangoDash  
from datetime import date
from dash.dash_table.Format import Group
import pandas as pd
from django.conf import settings
from apps.formularios.forms_partials.forms_dash_partials import (input_text,
                                                                input_dropdown_field,
                                                                input_double_text,
                                                                input_text_area,
                                                                input_drag_drop_select_file,
                                                                button_action,
                                                                input_dash_table)

def form_partials_C(selected_formulario):
    print("Llamada a form_partials_C con el formulario:", selected_formulario)
    return [
        input_text('nombre', 'id_nombre')
    ]

