from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.quiz_builder_home, name="quiz_builder_home"),
    path("new_quiz/<int:pk>", views.new_quiz, name="new_quiz"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
