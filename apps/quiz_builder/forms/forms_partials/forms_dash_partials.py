import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, State, dash_table
from django_plotly_dash import DjangoDash  
from datetime import date, datetime
#import pandas as pd
import base64
import os
import sys

# Definición global para almacenar datos de archivos
file_data = []

def create_modal_validation(message_modal, id_modal_message):
    modal_content = html.Div([
        html.Div(style={'height': '100px', 'padding-left':'300px'}),
        dbc.Button("Enviar", id="open-centered", className="ms-auto", n_clicks=0),
        dbc.Modal([
            dbc.ModalBody(f"{message_modal}"),
            dbc.ModalFooter([
                dbc.Button(
                    "Cancelar",
                    id="close-centered",
                    className="ms-auto btn-danger",  # Clase para el color rojo
                    n_clicks=0,
                ),
                dbc.Button(
                    "Aceptar",
                    id="aceptar-centered",
                    className="ml-2 btn-success",  # Clase para el color verde y moverlo a la derecha
                    n_clicks=0,
                ),
            ]),
        ],
        id=f"{id_modal_message}",
        centered=True,
        is_open=False,
        ),
        dcc.Store(id='click-store', data=0),  # Añade un almacenamiento para guardar el estado del clic
    ])
    return modal_content


def create_modal_confirm():
    modal_content = html.Div([
        dbc.Button("Confirmar", style={'display': 'None'}, id="open-centered-confirm"),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirmar"), close_button=True),
            dbc.ModalBody("¿Está seguro que desea enviar y guardar 'Formulario Requerimientos DTS'?"),
            dbc.ModalFooter([
                dbc.Button(
                    "Cancelar",
                    id="close-centered-confirm",
                    className="ms-auto btn-danger",
                    n_clicks=0,
                ),
                dbc.Button(
                    "Aceptar",
                    id="aceptar-centered-confirm",
                    className="ml-2 btn-success", 
                    n_clicks=0,
                ),
            ]),
        ],
        id="id_modal_confirm",
        centered=True,
        is_open=False,
        ),
    ])
    return modal_content

def format_text(content_text, font_size, font_family):
    return html.Div([
        f'{content_text}'
    ],
    className="text-center",
    style={'font-size': f'{font_size}px', 'font-family': f'{font_family}'})

def input_text(name_field, type_field, id_name_field, disabled=False):
    """Crea un campo de entrada de texto.

    Args:
        type_field (str): El tipo de campo de entrada (e.g., 'text', 'number', etc.).
        id_name_field (str): El identificador único del campo.

    Returns:
        list: Una lista con el diseño del campo de entrada de texto.
    """
    return [
        html.Div(style={'height': '20px'}),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                    dbc.Col(format_text(name_field, 22, 'Source Sans Pro'), md=12, lg=3),
                    dbc.Col(html.Div([
                        dcc.Input(
                            id=f'{id_name_field}',
                            placeholder='Enter a value...',
                            type=f'{type_field}',
                            value='',
                            style={'width': '100%'},
                            disabled=disabled
                        ),
                    ], className='pl-0 d-flex align-items-center'), md=12, lg=9),
                ])
            ), width=10),
            dbc.Col(width=1),
        ]),
    ]


def get_single_date_picker(name_field, id_single_date_picker):
    return [
        html.Div(style={'height': '20px'}),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                    dbc.Col(format_text(name_field, 22, 'Source Sans Pro'), md=12, lg=3),
                    dbc.Col(html.Div([
                        dcc.DatePickerSingle(
                            id=f'{id_single_date_picker}',
                            initial_visible_month=datetime(datetime.today().year, 1, 1).date(),
                            show_outside_days=True,
                            day_size=32,
                            display_format='DD/MM/YYYY',
                            clearable=True,
                            style={'z-index': '2000 !important;'}
                        ),
                    ], className='pl-0 d-flex align-items-center'), md=12, lg=9),
                ])
            ), width=10),
            dbc.Col(width=1),
        ]),
    ]


def input_dropdown_field(name_dropdown, list_value_dropdown_field, id_dropdown_field):
    return [
        html.Div(style={'height': '20px'}),
        dbc.Row([                
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                    dbc.Col(format_text(name_dropdown, 22, 'Source Sans Pro'), md=12, lg=3),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id=id_dropdown_field,
                            options=[{'label': i, 'value': i} for i in list_value_dropdown_field]
                        )
                    ]), md=12, lg=9),
                ])
            ), width=10),
            dbc.Col(width=1),
        ]), 
    ]


def input_double_text(input_title_left, input_title_right, id_input_left, id_input_right):
    """Crea dos campos de entrada de texto.

    Args:
        input_title_left (str): Título del primer campo de entrada de texto.
        input_title_right (str): Título del segundo campo de entrada de texto.
        id_input_left (str): Identificador único del primer campo de entrada de texto.
        id_input_right (str): Identificador único del segundo campo de entrada de texto.

    Returns:
        list: Una lista con el diseño de los dos campos de entrada de texto.
    """
    return [
        html.Div(style={'height': '40px'}), 
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                    dbc.Col(html.Div([
                        html.Br(),
                        dcc.Markdown(f''' ##### {input_title_left}: '''),
                    ]), md=12, lg=2),
                    dbc.Col(html.Div([
                        html.Br(),
                        dcc.Input(
                            id=f'{id_input_left}',
                            placeholder='Enter a value...',
                            type='text',
                            value='',
                            style={'width': '100%'}
                        ),
                    ], className='pl-0'), md=12, lg=6),
                    dbc.Col(html.Div([
                        html.Br(),
                        dcc.Markdown(f''' ##### {input_title_right}: '''),
                    ]), md=12, lg=2),
                    dbc.Col(html.Div([
                        html.Br(),
                        dcc.Input(
                            id=f'{id_input_right}',
                            placeholder='Enter a value...',
                            type='number',
                            value='',
                            style={'width': '100%'}
                        ),
                    ], className='pl-0'), md=12, lg=2),
                ])
            ), width=10),
            dbc.Col(width=1),
        ])
    ]


def input_text_area(input_title_text_area, id_input_text_area):
    """Crea un área de texto.

    Args:
        input_title_text_area (str): Título del área de texto.
        id_input_text_area (str): Identificador único del área de texto.

    Returns:
        list: Una lista con el diseño del área de texto.
    """
    return [
        html.Div(style={'height': '40px'}),  # Add a space
        dbc.Row([                
            dbc.Col(width=1),
            dbc.Col((
                dbc.Row([
                    dbc.Col(format_text(input_title_text_area, 22, 'Source Sans Pro'), md=12, lg=3),
                    dbc.Col(html.Div([
                        dcc.Textarea(
                            id=f'{id_input_text_area}',
                            placeholder='Describa el ítem...',
                            style={'width': '100%'}
                        )
                    ]), md=12, lg=9),
                ])
            ), width=10),
            dbc.Col(width=1),
        ]), 
    ]


def button_action(button_action_name, id_button_action):
    """Crea un botón de acción.

    Args:
        button_action_name (str): El nombre del botón.
        id_button_action (str): El identificador único del botón.

    Returns:
        list: Una lista con el diseño del botón de acción.
    """
    return [
        html.Div(style={'height': '40px'}),  
        dbc.Row([
            dbc.Col(width=2),
            dbc.Col((dbc.Button(button_action_name, id=f'{id_button_action}', style={'display': 'block'}, n_clicks=0),), width=8),
            dbc.Col(width=2)
        ]), 
    ]


def ask_confirm_action(n_clicks, message_confirm_action):
    """Verifica si se ha hecho clic en un botón de confirmación.

    Args:
        n_clicks (int): El número de clics en el botón de confirmación.
        message_confirm_action (str): El mensaje de confirmación.

    Returns:
        tuple: Una tupla que indica si se ha hecho clic en el botón de confirmación y el mensaje de confirmación.
    """
    if n_clicks is not None and n_clicks > 0:
        return True, message_confirm_action
    return False, ""


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    file_type = os.path.splitext(filename)[1][1:]
    file_size = sys.getsizeof(decoded)  # obtener el tamaño del archivo
    return {
        'File Number': len(file_data) + 1,
        'File Name': filename,
        'File Type': file_type,
        'File Size': file_size,  # agregar el tamaño del archivo
        'Content': decoded
    }


def update_upload_logic(list_of_contents, list_of_names, list_of_dates):
    global file_data
    if list_of_contents is not None:
        data = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        
        # Verificar el tamaño del archivo
        for file in data:
            print('Tamaño: ' + str(file['File Size']))
            if file['File Size'] > 5242880:
                return dash.no_update, "Archivo excede tamaño máximo"
        
        file_data.extend(data)
        return [{'File Number': f['File Number'], 'File Name': f['File Name'], 'File Type': f['File Type']} for f in file_data], ''
    else:
        raise dash.exceptions.PreventUpdate


def update_table_logic(data):
    if data is not None:
        df = pd.DataFrame(data)
        return df.to_dict('records')


def input_drag_drop_select_file(id_upload_file, id_file_table):
    """Crea una sección para arrastrar y soltar archivos.

    Returns:
        list: Una lista con el diseño de la sección de arrastrar y soltar archivos.
    """
    return [
        html.Div(style={'height': '40px'}),  # Add a space
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dcc.Markdown(f''' ##### ADJUNTAR DOCUMENTOS  ''', className="text-center"),
            ), width=10),
            dbc.Col(width=1),
        ]),
        dbc.Row([    
            dbc.Col(width=1),
            dbc.Col((html.Div([
                html.Div(style={'height': '20px'}),  
                dbc.Row([
                    dbc.Col(html.Div([
                        dcc.Upload(
                            id=f'{id_upload_file}',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            multiple=True
                        ),
                        dcc.Store(id='store-data-upload'),
                        html.Div(id='output-data-upload', children=dash_table.DataTable(id=f'{id_file_table}', row_deletable=True)),
                    ]), width=12),
                ]),
            ])), width=10),
            dbc.Col(width=1)
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='file-size-error'), width=12),  # Nuevo Div para mostrar el mensaje de error
        ]),       
    ]


def input_dash_table(df_table, id_table):
    """Crea una tabla dinámica.

    Args:
        df_table (DataFrame): El DataFrame para mostrar en la tabla.

    Returns:
        list: Una lista con el diseño de la tabla dinámica.
    """
    return [
        html.Div(style={'height': '20px'}), 
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col((
                dash_table.DataTable(
                    id=f'{id_table}',
                    columns=[{"name": i, "id": i} for i in df_table.columns],
                    data=df_table.to_dict('records'),
                    editable=True,
                    row_deletable=True,
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'textAlign': 'center',
                        'font-style': 'normal',
                        'fontWeight': '450',
                        'font-family': 'Courier',
                    },
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'Descripción Producto'},
                            'textAlign': 'left',
                        },
                        {
                            'if': {'column_id': 'Nombre Producto'},
                            'textAlign': 'center',
                        },
                        {
                            'if': {'column_id': 'Cantidad'},
                            'textAlign': 'center',
                        }
                    ],
                    style_data_conditional=[
                        {
                            'if': {'column_id': 'Descripción Producto'},
                            'textAlign': 'left',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'font-family': 'Courier',
                        },
                        {
                            'if': {'column_id': 'Nombre Producto'},
                            'textAlign': 'center',
                            'font-family': 'Courier',
                        },
                        {
                            'if': {'column_id': 'Cantidad'},
                            'textAlign': 'center',
                            'font-family': 'Courier',
                        }
                    ]
                ),
            ), width=10),
            dbc.Col(width=1),
        ])
    ]
