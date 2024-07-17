import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from django_plotly_dash import DjangoDash  
from dash import dash_table
import pandas as pd
import requests
import base64
import io
import json
from apps.quiz_builder.forms.forms_partials.forms_dash_partials import (
    input_text, input_dropdown_field, create_modal_validation, create_modal_confirm
)
from apps.quiz_builder.forms.get_data_functions.get_data_from_db import get_courses_names, get_lesson_content, get_categoria_lesson, get_list_topic_father
from django.db import transaction
from datetime import datetime
from apps.quiz_builder.models import CourseLessonQuiz, QuizContent, UserAnswerScore
from django.contrib.auth.models import User

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
theme = dbc.themes.BOOTSTRAP

app = DjangoDash('Formulario_Quiz_Builder', add_bootstrap_links=True, external_stylesheets=[theme, dbc.icons.BOOTSTRAP])

def serve_layout():
    courses_names = get_courses_names()
    topics_father = get_list_topic_father()
    return dbc.Container([
        html.Br(),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col(dcc.Markdown('##### Formulario Quiz Builder', className="text-center"), width=10),
            dbc.Col(width=1),
        ]),
        dbc.Container([
            dbc.Tabs([
                dbc.Tab(
                    label="Formulario",
                    children=[
                        dbc.Row([
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(input_dropdown_field(name_dropdown='Course Level: ', list_value_dropdown_field=courses_names, id_dropdown_field='id_course_level_dropdown'), width=10),
                                    dbc.Col(width=1),
                                ]),
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(input_dropdown_field(name_dropdown='Categoria Lesson: ', list_value_dropdown_field=[], id_dropdown_field='id_categoria_lesson_dropdown'), width=10),
                                    dbc.Col(width=1),
                                ]),
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(input_dropdown_field(name_dropdown='Lesson content: ', list_value_dropdown_field=[], id_dropdown_field='id_lesson_content_dropdown'), width=10),
                                    dbc.Col(width=1),
                                ]),
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(input_dropdown_field(name_dropdown='Topic Father: ', list_value_dropdown_field=topics_father, id_dropdown_field='id_list_topic_father_dropdown'), width=10),
                                    dbc.Col(width=1),
                                ]),
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(input_text(name_field='Quiz Name: ', type_field='text', id_name_field='id_quiz_name', disabled=False), width=10),
                                    dbc.Col(width=1),
                                ]),
                                html.Div(style={'height': '40px'}),  # Add a space
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(dcc.Markdown('##### ADJUNTAR DOCUMENTO QUIZ', className="text-center"), width=10),
                                    dbc.Col(width=1),
                                ]),
                                dbc.Row([    
                                    dbc.Col(width=1),
                                    dbc.Col(html.Div([
                                        html.Div(style={'height': '40px'}),
                                        dbc.Row([
                                            dbc.Col(html.Div([
                                                dcc.Upload(
                                                    id='upload-data',
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
                                                    multiple=False  # Change to single file upload
                                                ),
                                                dcc.Store(id='store-data-upload'),
                                                html.Div(id='output-data-upload')
                                            ]), width=12),
                                        ]),
                                    ]), width=10),
                                    dbc.Col(width=1)
                                ]),
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(create_modal_validation(message_modal='message', id_modal_message='id_modal_message_validation'), width=10),
                                    dbc.Col(width=1),
                                ]),
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(create_modal_confirm(), width=10),
                                    dbc.Col(width=1),
                                ]),
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(dbc.Button("Enviar", id='submit-button', color="primary"), width=10),
                                    dbc.Col(width=1),
                                ]),
                                dbc.Row([
                                    dbc.Col(width=1),
                                    dbc.Col(dbc.Button("Guardar Contenido", id='save-content-button', color="secondary"), width=10),
                                    dbc.Col(width=1),
                                ]),
                            ])
                        ]),
                    ]
                ),
            ]),
        ], style={'display': 'block', 'max-width': '100%', 'margin': 'auto'}, id='id_row_block'),
        dcc.ConfirmDialog(id='confirm', message=''),
        html.Br(),
        html.Div(id='output-message'),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col(html.Div(id='output_quiz_creado'), width=10),
            dbc.Col(width=1),
        ]),
        html.Div(id='user_id', style={'display': 'none'}),
        html.Div(id='username', style={'display': 'none'}),
        html.Div(id='email', style={'display': 'none'}),
    ], fluid=True, style={'padding-bottom':'200px'})

app.layout = serve_layout

@app.callback(
    Output('id_categoria_lesson_dropdown', 'options'),
    Input('id_course_level_dropdown', 'value')
)
def update_categoria_lesson_dropdown(selected_course):
    if selected_course:
        categorias = get_categoria_lesson(selected_course)
        return [{'label': i, 'value': i} for i in categorias]
    else:
        return []

@app.callback(
    Output('id_lesson_content_dropdown', 'options'),
    Input('id_categoria_lesson_dropdown', 'value')
)
def update_lesson_content_dropdown(selected_lesson):
    if selected_lesson:
        contenidos = get_lesson_content(selected_lesson)
        return [{'label': i, 'value': i} for i in contenidos]
    else:
        return []

@app.callback(
    Output('id_list_topic_father_dropdown', 'options'),
    Input('id_course_level_dropdown', 'value')
)
def update_topic_father_dropdown(_):
    topics = get_list_topic_father()
    return [{'label': i, 'value': i} for i in topics]

@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_output(contents, filename, last_modified):
    if contents is not None:
        return parse_contents(contents, filename, last_modified)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.DataFrame()

    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'json' in filename:
            data = json.loads(decoded.decode('utf-8'))
            df = pd.DataFrame(data).reset_index().rename(columns={"index": "ID"})
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.fromtimestamp(date)),

        dash_table.DataTable(
            id='quiz-table',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            editable=True,
            row_deletable=True,
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                'minWidth': '0px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            }
        ),

        html.Hr(),

        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(
    Output('output_quiz_creado', 'children'),
    Input('submit-button', 'n_clicks'),
    [State('id_course_level_dropdown', 'value'),
     State('id_categoria_lesson_dropdown', 'value'),
     State('id_lesson_content_dropdown', 'value'),
     State('id_list_topic_father_dropdown', 'value'),
     State('id_quiz_name', 'value'),
     State('output-data-upload', 'children'),
     State('quiz-table', 'data'),
     State('quiz-table', 'columns'),
     State('user_id', 'children')
     ],
    prevent_initial_call=True
)
def submit_and_save_quiz(n_clicks, course_level, categoria_lesson, lesson_content, topic_father, quiz_name, contents, rows, columns, user_id,request):
    user = request.user
    id = request.session.get('id')  # Obtiene el id de la sesión
    user_id = user.id
    print(user_id)
    if n_clicks > 0:
        try:
            user_id = int(user_id) if user_id else None
            print(f"User ID: {user_id}")

            if user_id is None:
                return "Error: Usuario no autenticado."

            with transaction.atomic():
                course_lesson_quiz = CourseLessonQuiz.objects.create(
                    Course_Level=course_level,
                    Categoria_Lesson=categoria_lesson,
                    Lesson_Content=lesson_content,
                    Topic_Father=topic_father,
                    Topic_Son="Generico",
                    Quiz_Name=quiz_name
                )
                course_lesson_quiz.save()

                if rows is not None and len(rows) > 0:
                    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])

                    if 'Spanish' in df.columns and 'English' in df.columns:
                        for index, row in df.iterrows():
                            quiz_content = QuizContent.objects.create(
                                FK_Course_Lesson_Quiz=course_lesson_quiz,
                                Spanish=row['Spanish'],
                                English=row['English']
                            )
                            quiz_content.save()

                            UserAnswerScore.objects.create(
                                FK_Table_Quiz_Course_Level=course_lesson_quiz,
                                Usuario_id=user_id,
                                FK_Quiz_Content=quiz_content,
                                Score=5
                            ).save()
                    else:
                        return "La tabla debe contener las columnas 'Spanish' y 'English'."

                return "Quiz creado y datos almacenados correctamente."
        except Exception as e:
            print(e)
            return f"Ocurrió un error al crear el quiz: {str(e)}"

    return ""


