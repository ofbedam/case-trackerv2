# dosyayon/urls.py


from django.contrib import admin
from django.urls import path
from .views import CocuklarAutocomplete, KisilerAutocomplete, generate_pdf


urlpatterns = [
    path('admin/', admin.site.urls),
    # Your other URL patterns
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('cocuklar-autocomplete/', CocuklarAutocomplete.as_view(), name='cocuklar-autocomplete'),
    path('kisiler-autocomplete/', KisilerAutocomplete.as_view(), name='kisiler-autocomplete'),


]
