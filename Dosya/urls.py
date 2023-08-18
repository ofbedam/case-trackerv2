# dosya/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Diğer URL örüntüleri
    path('analyze/', views.analyze_data, name='analyze_data'),
]
