from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.starter, name="starter"),
    path("starter_home", views.starter_home, name="starter_home"),
    path("a1_home", views.a1_home, name="a1_home"),
    path("a2_home", views.a2_home, name="a2_home"),
    path("b1_home", views.b1_home, name="b1_home"),
    path("b2_home", views.b2_home, name="b2_home"),
    path("details/<str:course_level>/<str:categoria_lesson>/", views.lesson_details, name="lesson_details"),
    path("course_detail/<int:lesson_id>/", views.course_detail, name="course_detail"),  # Nueva ruta
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
