import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State
from dash.dependencies import Input, Output, State

def message_alert(message_alert):
    """Crea una alerta de mensaje de color rojo.

    Args:
        message_alert (str): El mensaje de alerta a mostrar.

    Returns:
        list: Una lista con el diseño de la alerta.
    """
    return [
        dbc.Row([
            dbc.Col((), width=1),
            dbc.Col((
                html.Div(style={'height': '20px'}),
                dbc.Alert([
                    html.I(className="bi bi-x-octagon-fill me-2"), 
                    "Información incompleta, por favor ingresar: ", html.Strong(f"{message_alert}")
                ], color="danger", className="d-flex align-items-center", ),
                html.Div(style={'height': '20px'}),
            ), width=10),
            dbc.Col((), width=1),
        ]),
    ]


def message_success(message_success):
    """Crea una alerta de mensaje de color verde.

    Args:
        message_success (str): El mensaje de éxito a mostrar.

    Returns:
        list: Una lista con el diseño de la alerta.
    """
    return [
        dbc.Row([
            dbc.Col((), width=1),
            dbc.Col((
                html.Div(style={'height': '20px'}),
                dbc.Alert([html.I(className="bi bi-check-circle-fill me-2"), message_success, ],
                          color="success", className="d-flex align-items-center", ),
                html.Div(style={'height': '20px'}),
            ), width=10),
            dbc.Col((), width=1),
        ]),
    ]

def validation_not_none(value, value_name):
    """Valida si un valor no es nulo.

    Args:
        value (any): El valor a validar.
        value_name (str): El nombre del valor para mostrar en el mensaje de alerta.

    Returns:
        tuple: Una tupla con un booleano indicando si el valor no es nulo y un mensaje de alerta opcional.
    """
    if not value:
        return False, message_alert(f'Información incompleta - Agregar {value_name}')
    else:
        return True, None


def validation_datatable_not_none(value_table, table_name):
    """Valida si una tabla de datos no está vacía.

    Args:
        value_table (pandas.DataFrame): La tabla de datos a validar.
        table_name (str): El nombre de la tabla para mostrar en el mensaje de alerta.

    Returns:
        tuple: Una tupla con un booleano indicando si la tabla no está vacía y un mensaje de alerta opcional.
    """
    if not value_table or len(value_table) == 0:
        return False, message_alert(f'Información incompleta - Agregar {table_name}')
    else:
        return True, None

def validation_drag_drop_select_file_not_none(file_table, table_file_name):
    """Valida si una tabla de archivos no está vacía.

    Args:
        file_table (pandas.DataFrame): La tabla de archivos a validar.
        table_file_name (str): El nombre de la tabla de archivos para mostrar en el mensaje de alerta.

    Returns:
        tuple: Una tupla con un booleano indicando si la tabla de archivos no está vacía y un mensaje de alerta opcional.
    """
    if not file_table or len(file_table) == 0:
        return False, message_alert(f'Información incompleta - Agregar {table_file_name}')
    else:
        return True, None


def check_file_size(file):
    if file['File Size'] > 5242880:
        return True
    return False

def process_files(list_of_contents, list_of_names, list_of_dates):
    return [parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]