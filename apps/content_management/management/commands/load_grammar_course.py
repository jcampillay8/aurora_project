# apps/content_management/management/commands/load_grammar_course.py

import csv
import os
from django.core.management.base import BaseCommand
from apps.content_management.models import StructuredEnglishGrammarCourse
class Command(BaseCommand):
    help = 'Load grammar course data from CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'grammar_course.csv')
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StructuredEnglishGrammarCourse.objects.create(
                    id=row['ID'],
                    courses=row['Courses'],
                    lesson=row['Lesson'],
                    lesson_content=row['Lesson_Content']
                )
        
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))


