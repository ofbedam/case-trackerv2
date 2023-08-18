from django.urls import path
from . import views

urlpatterns = [
    path('dosya/<int:dosya_id>/duzenle/', views.dosya_duzenle, name='dosya_duzenle'),

]
