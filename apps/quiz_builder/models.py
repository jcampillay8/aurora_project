from django.db import models
from django.contrib.auth.models import User

class CourseLessonQuiz(models.Model):
    Course_Level = models.CharField(max_length=255)
    Categoria_Lesson = models.CharField(max_length=255)
    Lesson_Content = models.CharField(max_length=255)
    Topic_Father = models.CharField(max_length=255)
    Topic_Son = models.CharField(max_length=255, default='Generico')
    Quiz_Name = models.CharField(max_length=255)

class QuizContent(models.Model):
    FK_Course_Lesson_Quiz = models.ForeignKey(CourseLessonQuiz, on_delete=models.CASCADE)
    Spanish = models.TextField()
    English = models.TextField()

class UserAnswerScore(models.Model):
    FK_Table_Quiz_Course_Level = models.ForeignKey(CourseLessonQuiz, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    FK_Quiz_Content = models.ForeignKey(QuizContent, on_delete=models.CASCADE)
    Score = models.IntegerField(default=5)
