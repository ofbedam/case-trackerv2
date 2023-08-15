from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Dosyalar
from datetime import datetime
from .forms import DosyalarAdminForm

def create_dosya_3_12(request):
    if request.method == 'POST':
        form = DosyalarAdminForm(request.POST)
        if form.is_valid():
            # Form verileri doğruysa işleme adımlarını gerçekleştir
            current_year = datetime.now().year
            latest_dosya = Dosyalar.objects.filter(DosyaKodu='3-12', DosyaYil=current_year).order_by('-DosyaNo').first()
            if latest_dosya:
                next_dosya_no = latest_dosya.DosyaNo + 1
            else:
                next_dosya_no = 1

            # Dosya nesnesini oluştur
            dosya = form.save(commit=False)
            dosya.DosyaKodu = '3-12'
            dosya.DosyaYil = current_year
            dosya.DosyaNo = next_dosya_no
            dosya.DosyaAcilisTarihi = datetime.now()
            dosya.DosyaDurumu = 'Açık'
            dosya.save()

            return redirect(reverse('admin:dosyalar_dosyalar_changelist'))  # Admin sayfasına yönlendir
    else:
        form = DosyalarAdminForm()

    return render(request, 'dosyalar/create_dosya.html', {'dosya_kodu': '3-12', 'form': form})
