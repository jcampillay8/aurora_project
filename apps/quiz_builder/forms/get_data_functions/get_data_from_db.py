# apps/quiz_builder/forms/get_data_functions/get_data_from_db.py

from apps.content_management.models import StructuredEnglishGrammarCourse, ListTopicFather

def get_courses_names():
    # Obtener todos los cursos únicos de la base de datos
    courses = StructuredEnglishGrammarCourse.objects.values_list('courses', flat=True).distinct()
    return list(courses)

def get_categoria_lesson(selected_course):
    # Obtener todas las lecciones para un curso específico
    categorias = StructuredEnglishGrammarCourse.objects.filter(courses=selected_course).values_list('lesson', flat=True).distinct()
    return list(categorias)

def get_lesson_content(selected_lesson):
    # Obtener el contenido de una lección específica
    contenidos = StructuredEnglishGrammarCourse.objects.filter(lesson=selected_lesson).values_list('lesson_content', flat=True).distinct()
    return list(contenidos)

def get_list_topic_father():
    # Obtener todos los valores de list_topic_father
    topics = ListTopicFather.objects.values_list('topic_father', flat=True).distinct()
    return list(topics)
