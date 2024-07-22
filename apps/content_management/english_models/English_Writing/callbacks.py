import json
import os
import random
import dash
from gtts import gTTS
from sentence_transformers import SentenceTransformer, util
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
from difflib import ndiff
from openai import OpenAI
from .utils import highlight_differences
import environ  # Importar environ

# Cargar el archivo .env
env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, 'core/assets/.env'))

client = OpenAI(api_key=env('OPENAI_API_KEY'))
model = SentenceTransformer('all-MiniLM-L6-v2')

# Cargar el archivo JSON
with open('data/language_b1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Inicializar los contadores
total_preguntas = 1
respuestas_correctas = 0
respuestas_incorrectas = 0

def highlight_differences(user_answer, correct_answer):
    diff = list(ndiff(user_answer.split(), correct_answer.split()))
    diff_html = []
    for part in diff:
        if part.startswith('-'):
            diff_html.append(html.Span(part[2:] + ' ', style={'color': 'red', 'text-decoration': 'line-through'}))
        elif part.startswith('+'):
            diff_html.append(html.Span(part[2:] + ' ', style={'color': 'green', 'font-weight': 'bold'}))
        else:
            diff_html.append(html.Span(part[2:] + ' '))
    return diff_html

def register_callbacks(app):
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
         State('evaluation-output', 'children')]
    )
    def handle_interactions(n_clicks_submit, n_clicks_next, threshold, sentence_key, student_input, feedback_message, correction_output, evaluation_output):
        global total_preguntas, respuestas_correctas, respuestas_incorrectas
        ctx = dash.callback_context

        if not ctx.triggered:
            selected_sentence = str(random.choice(list(data['Spanish'].keys())))
            return data['Spanish'][selected_sentence], selected_sentence, '', '', '', '', 0, [
                html.Span(f"Total Preguntas: {total_preguntas}", className='mr-4 font-weight-bold'),
                html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
                html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
            ], str(data['Score'][selected_sentence]), None, {'display': 'none'}

        # Lógica para el botón "Next"
        if 'next-button' in ctx.triggered[0]['prop_id']:
            if not student_input.strip() and not feedback_message and not correction_output and not evaluation_output:
                feedback = dbc.Alert("No se ha ingresado respuesta.", color="warning", style={"font-size": "15px", "margin-top": '10px', 'textAlign': 'center', 'fontWeight': 'bold'})
                return data['Spanish'][sentence_key], sentence_key, student_input, feedback, '', '', 0, [
                    html.Span(f"Total Preguntas: {total_preguntas}", className='mr-4 font-weight-bold'),
                    html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
                    html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
                ], str(data['Score'][sentence_key]), None, {'display': 'none'}
            total_preguntas += 1

            # Filtrar preguntas elegibles según el umbral
            eligible_questions = [k for k, v in data['Score'].items() if v <= threshold]
            if not eligible_questions:
                feedback = dbc.Alert("No hay preguntas disponibles para el umbral seleccionado.", color="danger", style={"font-size": "15px", "margin-top": '10px', 'textAlign': 'center', 'fontWeight': 'bold'})
                return dash.no_update, dash.no_update, '', feedback, '', '', 0, [
                    html.Span(f"Total Preguntas: {total_preguntas - 1}", className='mr-4 font-weight-bold'),
                    html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
                    html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
                ], '0', None, {'display': 'none'}

            # Seleccionar 5 oraciones al azar de las preguntas elegibles y elegir la con el puntaje más bajo
            selected_questions = random.sample(eligible_questions, min(5, len(eligible_questions)))
            selected_sentence = min(selected_questions, key=lambda k: data['Score'][k])
            
            return data['Spanish'][selected_sentence], selected_sentence, '', '', '', '', 0, [
                html.Span(f"Total Preguntas: {total_preguntas}", className='mr-4 font-weight-bold'),
                html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
                html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
            ], str(data['Score'][selected_sentence]), None, {'display': 'none'}

        # Lógica para el botón "Enviar"
        correct_sentence = data['English'][sentence_key]
        
        # Calcular la similitud semántica utilizando BERT
        student_embedding = model.encode(student_input, convert_to_tensor=True)
        correct_embedding = model.encode(correct_sentence, convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(student_embedding, correct_embedding).item() * 100

        # Evaluar la oración del estudiante
        accuracy = similarity_score

        # Obtener feedback y sugerencias específicas usando la API de OpenAI
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

        # Resaltar diferencias entre la respuesta del usuario y la correcta
        highlighted_differences = highlight_differences(student_input, correct_sentence)

        corrections_output = html.Div([
            html.Div([
                dcc.Markdown("**Sugerencias IA para Mejorar:**", style={'whiteSpace': 'nowrap', 'display': 'inline'}),
                html.Div(suggestions, className='d-block d-lg-inline')
            ], className='d-flex flex-column flex-lg-row align-items-start'),
            html.Br(),
            dcc.Markdown(f"**Oración del estudiante:** {student_input}"),
            dcc.Markdown(f"**Oración correcta:** {correct_sentence}"),
            html.Div([
                dcc.Markdown("**Diferencias resaltadas:**"),
                html.Div(highlighted_differences, className='d-block d-lg-inline')
            ], className='d-flex flex-column flex-lg-row align-items-start'),
            html.Br(),
            dcc.Markdown(f"**Similaridad semántica:** {similarity_score:.2f}%")
        ])

        evaluation_output = f"Evaluación: Tu oración es {accuracy:.2f}% correcta."

        # Generar feedback de audio usando gTTS
        audio_text = f"Here is how you pronounce it: {correct_sentence}."
        tts = gTTS(audio_text)
        audio_file_path = os.path.join('static', 'correct_answer.mp3')
        tts.save(audio_file_path)
        audio_link = f'/static/correct_answer.mp3'

        # Actualizar el puntaje basado en la respuesta del estudiante
        if accuracy > 85:
            feedback = dbc.Alert("Correcto!", color="success", style={"font-size": "15px", "margin-top": '10px', 'textAlign': 'center', 'fontWeight': 'bold'})
            respuestas_correctas += 1
            data['Score'][sentence_key] += 1
        else:
            feedback = dbc.Alert("Incorrecto!", color="danger", style={"font-size": "15px", "margin-top": '10px', 'textAlign': 'center', 'fontWeight': 'bold'})
            respuestas_incorrectas += 1
            data['Score'][sentence_key] -= 1

        return data['Spanish'][sentence_key], sentence_key, '', feedback, corrections_output, evaluation_output, accuracy / 10, [
            html.Span(f"Total Preguntas: {total_preguntas}", className='mr-4 font-weight-bold'),
            html.Span(f"Respuestas Correctas: {respuestas_correctas}", className='mr-4 font-weight-bold'),
            html.Span(f"Respuestas Incorrectas: {respuestas_incorrectas}", className='font-weight-bold')
        ], str(data['Score'][sentence_key]), audio_link, {'display': 'block'}
