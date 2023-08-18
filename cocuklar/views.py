from django.shortcuts import render, get_object_or_404, redirect
from Dosya.models import Dosya

def dosya_duzenle(request, dosya_id):
    dosya = get_object_or_404(Dosya, id=dosya_id)
    # Gerekli işlemleri yapın ve düzenleme formunu gösterin
    return render(request, 'dosya_duzenle.html', {'dosya': dosya})

