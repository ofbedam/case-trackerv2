# dosyayon/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

from .views import CocuklarAutocomplete, KisilerAutocomplete, generate_pdf, CountryAutocomplete, StateAutocomplete, CityAutocomplete
from django.views.generic import TemplateView




urlpatterns = [
    path('admin/', admin.site.urls),
    # Your other URL patterns
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('cocuklar-autocomplete/', CocuklarAutocomplete.as_view(), name='cocuklar-autocomplete'),
    path('kisiler-autocomplete/', KisilerAutocomplete.as_view(), name='kisiler-autocomplete'),
    path('kurumlar/', include('kurumlar.urls')),
    path('select2/', include('django_select2.urls')),
    path('chaining/', include('smart_selects.urls')),

    # path("todo-app/", include("todo_app.urls")),
    # path("todo/", include("todo.urls")),
    path('cocuklar/', include('cocuklar.urls')),
    path('Dosya/', include('Dosya.urls')),

    path('CountryAutocomplete/', CountryAutocomplete.as_view(), name='CountryAutocomplete'),
    path('StateAutocomplete/', StateAutocomplete.as_view(), name='StateAutocomplete'),
    path('CityAutocomplete/', CityAutocomplete.as_view(), name='CityAutocomplete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

