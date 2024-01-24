from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from GamingProfession import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('demand', views.demand, name='demand'),
    path('geography', views.geography, name='geography'),
    path('skills', views.skills, name='skills'),
    path('latest_vacancies', views.latest_vacancies, name='latest_vacancies'),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)