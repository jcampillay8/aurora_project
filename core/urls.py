from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler404
from apps.Error_handler.views import Error404View, Error505View

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("authentication/", include("apps.authentication.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include("apps.home.urls")),
    path('starter/', include('apps.content_management.urls')),
    path('quiz_builder/', include('apps.quiz_builder.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
)

handler404 = Error404View.as_view()

handler505 = Error505View.as_error_view()