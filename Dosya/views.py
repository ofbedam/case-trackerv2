import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import Dosya
from django.conf import settings
import os
import matplotlib as mpl

mpl.use('Agg')  # Matplotlib'ı GUI modunda başlatmadan kullanmak için

def analyze_data(request):
    dosya_objects = Dosya.objects.all()
    dosya_kodlari = [dosya.dosya_kodu for dosya in dosya_objects]
    dosya_sayilari = [dosya.sayi for dosya in dosya_objects]

    plt.figure(figsize=(10, 6))
    plt.bar(dosya_kodlari, dosya_sayilari)
    plt.title("Dosya Koduna Göre Dosya Sayısı Analizi")
    plt.xlabel("Dosya Kodu")
    plt.ylabel("Dosya Sayısı")
    plt.xticks(rotation=45)
    plt.grid()

    # Save the plot to the media directory
    plot_file = os.path.join(settings.MEDIA_ROOT, "dosya_analysis.png")
    plt.savefig(plot_file)
    plt.close()

    # Create the absolute URL for the saved plot file
    plot_file_url = request.build_absolute_uri(settings.MEDIA_URL + "dosya_analysis.png")

    context = {'plot_file_url': plot_file_url}
    return render(request, 'dosya_analysis.html', context)
