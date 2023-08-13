# dosyayon/urls.py


from django.urls import path, include
from django.contrib import admin

from .views import CocuklarAutocomplete, KisilerAutocomplete, generate_pdf
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

    path("todo-app/", include("todo_app.urls")),
    path("todo/", include("todo.urls")),






]
