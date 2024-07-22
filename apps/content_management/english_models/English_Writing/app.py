import random
import os
import dash
from gtts import gTTS
import requests
from sentence_transformers import SentenceTransformer, util
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
import nltk
from django_plotly_dash import DjangoDash
from django.conf import settings
from django.db import models  # Importar models de django.db
from apps.quiz_builder.models import CourseLessonQuiz, QuizContent, UserAnswerScore
from openai import OpenAI
from .utils import highlight_differences
import environ  # Importar environ

# Cargar el archivo .env
env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, 'core/assets/.env'))

client = OpenAI(api_key=env('OPENAI_API_KEY'))

# Cargar el modelo de BERT preentrenado
model = SentenceTransformer('all-MiniLM-L6-v2')

# Crear la aplicación Dash
app = DjangoDash('EnglishWriting', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Inicializar los contadores
total_preguntas = 1  # Comienza en 1
respuestas_correctas = 0
respuestas_incorrectas = 0

# Crear el layout de la aplicación
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([], width=12, lg=1),  # Columna vacía a la izquierda
        dbc.Col([
            html.H2("Práctica de Inglés", className="text-center my-4"),
            html.Div(id='stats-row', className='d-flex justify-content-between flex-wrap'),
            html.Br(),
            dbc.Row([
                dbc.Col(html.Div("Filtro Puntaje Mayor", className="font-weight-bold text-right mr-1"), width="auto"),
                dbc.Col(dcc.Dropdown(
                    id='threshold-dropdown',
                    options=[{'label': str(i), 'value': i} for i in range(1, 11)],
                    value=6,
                    clearable=False,
                    style={'width': '100px'}
                ), width="auto"),
                dbc.Col(html.Div(className='flex-fill')),  # Espacio flexible
                dbc.Col(html.Audio(id='audio-feedback', controls=True, className='audio-feedback'))
            ], align="center", className='my-3'),  # Añadir margen vertical
            html.Br(),
            html.H4(id='spanish-sentence', **{"data-key": "1"}),
            dcc.Textarea(
                id='student-input',
                style={'width': '100%', 'height': 100},
            ),
            html.Br(),
            dbc.Row([
                dbc.Col(dbc.Button("Enviar", id='submit-button', color='primary'), width='auto', className='my-2'),  # Añadir margen vertical
                dbc.Col(dbc.Button("Next", id='next-button', color='secondary'), width='auto', className='my-2'),  # Añadir margen vertical
                dbc.Col(html.Div(style={'width': '10px'}), className='my-2'),  # Espacio entre los botones con margen vertical
                dbc.Col(
                    dbc.Row([
                        dbc.Col(html.Div("Puntaje", className="font-weight-bold text-right mr-1"), width="auto", className='my-2'),  # Añadir margen vertical
                        dbc.Col(daq.LEDDisplay(
                            id='score-display',
                            value="5",
                            size=20,
                            color="#1E90FF"  # Azul oscuro
                        ), width="auto", className='my-2')  # Añadir margen vertical
                    ], align="center"),
                    width="auto", className='my-2'  # Añadir margen vertical
                ),
                dbc.Col(html.Div(style={'width': '10px'}), className='my-2'),  # Espacio entre los botones con margen vertical
                dbc.Col(daq.GraduatedBar(
                    id='accuracy-bar',
                    color={"gradient": True, "ranges": {"red": [0, 4], "yellow": [4, 7], "green": [7, 10]}},
                    showCurrentValue=True,
                    value=0,
                    className='accuracy-bar'
                ), width=True, className='d-flex justify-content-end my-2')  # Añadir margen vertical
            ]),
            html.Br(),
            html.Div(id='feedback-message', className='text-center font-weight-bold my-2'),  # Añadir margen vertical
            html.Div(id='correction-output', className='my-2'),  # Añadir margen vertical
            html.Div(id='evaluation-output', className='my-2'),  # Añadir margen vertical
            html.Div(id='user_id', style={'display': 'none'}),
            html.Div(id='username', style={'display': 'none'}),
            html.Div(id='email', style={'display': 'none'}),
        ], width=12, lg=10),  # Contenedor principal
        dbc.Col([], width=12, lg=1)  # Columna vacía a la derecha
        
    ], justify="center", className='my-3')  # Añadir margen vertical
], fluid=True)

# Añadir CSS personalizado para ajustar tamaños en móviles
app.css.append_css({
    'external_url': '/assets/styles.css'
})

# Callback unificado para manejar tanto "Enviar" como "Next"
@app.callback(
    [Output('spanish-sentence', 'children'),
     Output('spanish-sentence', 'data-key'),
     Output('student-input', 'value'),
     Output('feedback-message', 'children'),
     Output('correction-output', 'children'),
     Output('evaluation-output', 'children'),
     Output('accuracy-bar', 'value'),
     Output('stats-row', 'children'),
     Output('score-display', 'value'),
     Output('audio-feedback', 'src'),
     Output('audio-feedback', 'style')],
    [Input('submit-button', 'n_clicks'),
     Input('next-button', 'n_clicks')],
    [State('threshold-dropdown', 'value'),
     State('spanish-sentence', 'data-key'),
     State('student-input', 'value'),
     State('feedback-message', 'children'),
     State('correction-output', 'children'),
     State('evaluation-output', 'children'),
     State('user_id', 'children')]
)
def handle_interactions(n_clicks_submit, n_clicks_next, threshold, sentence_key, student_input, feedback_message, correction_output, evaluation_output, user_id, request):
    global total_preguntas, respuestas_correctas, respuestas_incorrectas
    ctx = dash.callback_context
    user = request.user
    id = request.session.get('id')  # Obtiene el id de la sesión
    user_id = user.id

    selected_sentence = None

    if not ctx.triggered:
        selected_content = QuizContent.objects.filter(FK_Course_Lesson_Quiz__id=1).order_by('?').first()
        if not selected_content:
            return dash.no_update, '', dash.no_update, dash.no_update, dash.no_update, 0, dash.no_update, '5', None, {'display': 'none'}
        return selected_content.Spanish, selected_content.id, '', '', '', '', 0, [
            html.Span(f"Total Preguntas: {total_preguntas}", className='mr-4 font-weight-bold'),
            html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
            html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
        ], '5', None, {'display': 'none'}

    # Lógica para el botón "Next"
    if 'next-button' in ctx.triggered[0]['prop_id']:
        if not student_input.strip() and not feedback_message and not correction_output and not evaluation_output:
            feedback = dbc.Alert("No se ha ingresado respuesta.", color="warning", style={"font-size": "15px", "margin-top": '10px', 'textAlign': 'center', 'fontWeight': 'bold'})
            return dash.no_update, dash.no_update, student_input, feedback, dash.no_update, dash.no_update, 0, [
                html.Span(f"Total Preguntas: {total_preguntas}", className='mr-4 font-weight-bold'),
                html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
                html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
            ], '5', None, {'display': 'none'}
        total_preguntas += 1

        eligible_questions = QuizContent.objects.filter(FK_Course_Lesson_Quiz__id=1)
        if not eligible_questions.exists():
            feedback = dbc.Alert("No hay preguntas disponibles.", color="danger", style={"font-size": "15px", "margin-top": '10px', 'textAlign': 'center', 'fontWeight': 'bold'})
            return dash.no_update, '', feedback, '', '', 0, [
                html.Span(f"Total Preguntas: {total_preguntas - 1}", className='mr-4 font-weight-bold'),
                html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
                html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
            ], '0', None, {'display': 'none'}

        selected_questions = random.sample(list(eligible_questions), min(5, eligible_questions.count()))
        selected_sentence = min(selected_questions, key=lambda x: UserAnswerScore.objects.filter(FK_Quiz_Content=x).aggregate(models.Min('Score'))['Score__min'])

        return selected_sentence.Spanish, selected_sentence.id, '', '', '', '', 0, [
            html.Span(f"Total Preguntas: {total_preguntas}", className='mr-4 font-weight-bold'),
            html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
            html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
        ], '5', None, {'display': 'none'}

    # Lógica para el botón "Enviar"
    if 'submit-button' in ctx.triggered[0]['prop_id']:
        correct_sentence = QuizContent.objects.get(id=sentence_key).English

        student_embedding = model.encode(student_input, convert_to_tensor=True)
        correct_embedding = model.encode(correct_sentence, convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(student_embedding, correct_embedding).item() * 100

        accuracy = similarity_score

        messages = [
            {"role": "system", "content": "You are an English tutor"},
            {"role": "user", "content": f"Correct the following sentence: {student_input}. The correct sentence is: {correct_sentence}."}
        ]
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100
        )
        suggestions = completion.choices[0].message.content

        highlighted_differences = highlight_differences(student_input, correct_sentence)

        corrections_output = html.Div([
        html.Div([
            dcc.Markdown("**Sugerencias IA para Mejorar:**", style={'whiteSpace': 'nowrap', 'display': 'inline'}),
            html.Div(suggestions, className='d-block d-lg-inline')
            ]),
            html.Br(),
            dcc.Markdown(f"**Oración del estudiante:** {student_input}"),
            dcc.Markdown(f"**Oración correcta:** {correct_sentence}"),
            html.Div([
                dcc.Markdown("**Diferencias resaltadas:**"),
                html.Div(highlighted_differences, className='d-block d-lg-inline')
            ]),
            html.Br(),
            dcc.Markdown(f"**Similaridad semántica:** {similarity_score:.2f}%")
        ])

        evaluation_output = f"Evaluación: Tu oración es {accuracy:.2f}% correcta."

        audio_text = f"Here is how you pronounce it: {correct_sentence}."
        tts = gTTS(audio_text)
        audio_file_path = os.path.join(settings.BASE_DIR, 'static', 'correct_answer.mp3')
        tts.save(audio_file_path)
        audio_link = f'/static/correct_answer.mp3'

        user_score, created = UserAnswerScore.objects.get_or_create(
            FK_Table_Quiz_Course_Level=QuizContent.objects.get(id=sentence_key).FK_Course_Lesson_Quiz,
            Usuario_id=user_id,
            FK_Quiz_Content=QuizContent.objects.get(id=sentence_key),
        )
        if accuracy > 85:
            feedback = dbc.Alert("Correcto!", color="success", style={"font-size": "15px", "margin-top": '10px', 'textAlign': 'center', 'fontWeight': 'bold'})
            respuestas_correctas += 1
            user_score.Score += 1
        else:
            feedback = dbc.Alert("Incorrecto!", color="danger", style={"font-size": "15px", "margin-top": '10px', 'textAlign': 'center', 'fontWeight': 'bold'})
            respuestas_incorrectas += 1
            user_score.Score -= 1
        user_score.save()

        return '', '', '', feedback, corrections_output, evaluation_output, accuracy / 10, [
            html.Span(f"Total Preguntas: {total_preguntas}", className='mr-4 font-weight-bold'),
            html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
            html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
        ], str(user_score.Score), audio_link, {'display': 'block'}

if __name__ == '__main__':
    nltk.download("punkt")
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'static')):
        os.makedirs(os.path.join(settings.BASE_DIR, 'static'))
    app.run_server(debug=True)
