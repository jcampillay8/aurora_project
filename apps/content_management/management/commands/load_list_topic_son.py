# apps/content_management/management/commands/load_list_topic_son.py

import csv
import os
from django.core.management.base import BaseCommand
from apps.content_management.models import ListTopicSon, ListTopicFather

class Command(BaseCommand):
    help = 'Load list topic son from CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'list_topic_son.csv')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    father = ListTopicFather.objects.get(topic_father=row['Topic_Father'].strip().lower())
                except ListTopicFather.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Topic father not found: {row["Topic_Father"]}'))
                    continue
                
                obj, created = ListTopicSon.objects.update_or_create(
                    id=row['ID'],
                    defaults={
                        'topic_father': father,
                        'topic_son': row['Topic_Son'].strip()
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new topic son: {row["Topic_Son"]}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated topic son: {row["Topic_Son"]}'))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
