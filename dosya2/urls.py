# dosya/urls.py
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Diğer URL örüntüleri
    path('analyze/', views.analyze_data, name='analyze_data'),
    path('kapatma/', views.analyze_closing_time,  name='analyze_closing_time'),
path('kapatmakodagore/', views.analyze_closing_time_by_code,  name='analyze_closing_time_by_code'),

]
