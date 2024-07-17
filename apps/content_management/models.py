# apps/content_management/models.py

from django.db import models

class StructuredEnglishGrammarCourse(models.Model):
    id = models.AutoField(primary_key=True)
    courses = models.CharField(max_length=255)
    lesson = models.CharField(max_length=255)
    lesson_content = models.TextField()

    def __str__(self):
        return self.courses


class ListTopicFather(models.Model):
    id = models.AutoField(primary_key=True)
    topic_father = models.CharField(max_length=255)

    def __str__(self):
        return self.topic_father
