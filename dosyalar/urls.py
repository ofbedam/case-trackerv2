# dosyalar/urls.py


# urls.py
from django.urls import path
from . import views

from django.contrib import admin

urlpatterns = [

    # ... other URL patterns ...
    path('dosya-ekle/3-12/', views.create_dosya_3_12, name='create_dosya_3_12'),
    # path('dosya-ekle/3-13/', views.create_dosya_3_13, name='create_dosya_3_13'),
    # path('dosya-ekle/3-12-bilgi/', views.create_dosya_3_12_bilgi, name='create_dosya_3_12_bilgi'),
]





