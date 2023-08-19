import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import Dosya
from django.conf import settings
import os
import matplotlib as mpl
import numpy as np
import json
from django.db import models

from datetime import datetime


mpl.use('Agg')  # Matplotlib'ı GUI modunda başlatmadan kullanmak için

def analyze_data(request):
    # dosya_counts = Dosya.objects.values('dosya_kodu').annotate(count=models.Count('dosya_kodu'))
    #
    # dosya_kodlari = [entry['dosya_kodu'] for entry in dosya_counts]
    # dosya_sayilari = [entry['count'] for entry in dosya_counts]
    #
    # plt.figure(figsize=(10, 6))
    # plt.bar(dosya_kodlari, dosya_sayilari)
    # plt.title("Dosya Koduna Göre Dosya Sayısı")
    # plt.xlabel("Dosya Kodu")
    # plt.ylabel("Dosya Sayısı")
    # plt.xticks(rotation=45)
    # plt.tight_layout()

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


def analyze_closing_time(request):
    dosya_objects = Dosya.objects.all()

    acilis_tarihleri = [dosya.DosyaAcilisTarihi for dosya in dosya_objects if dosya.DosyaKapatmaTarihi]
    kapanma_tarihleri = [dosya.DosyaKapatmaTarihi for dosya in dosya_objects if dosya.DosyaKapatmaTarihi]

    kapanma_sureleri = [(kapanma - acilis).days for acilis, kapanma in zip(acilis_tarihleri, kapanma_tarihleri) if
                        kapanma and acilis]

    ortalama_kapanma_suresi = np.mean(kapanma_sureleri)

    plt.figure(figsize=(10, 6))
    plt.hist(kapanma_sureleri, bins=20, color='blue', alpha=0.7)
    plt.axvline(ortalama_kapanma_suresi, color='red', linestyle='dashed', linewidth=1.5, label=f'Ortalama: {ortalama_kapanma_suresi:.2f} gün')
    plt.title('Dosya Ortalama Kapanma Süresi Analizi')
    plt.xlabel('Kapanma Süresi (gün)')
    plt.ylabel('Dosya Sayısı')
    plt.legend()
    plt.grid()

    # Save the plot to the media directory
    plot_file = os.path.join(settings.MEDIA_ROOT, "dosya_closing_time_analysis.png")
    plt.savefig(plot_file)
    plt.close()

    # Create the absolute URL for the saved plot file
    plot_file_url = request.build_absolute_uri(settings.MEDIA_URL + "dosya_closing_time_analysis.png")

    context = {'plot_file_url': plot_file_url}
    return render(request, 'dosya_closing_time_analysis.html', context)




def analyze_closing_time_by_code(request):
    dosya_objects = Dosya.objects.filter(DosyaDurumu='Kapalı')  # Sadece Kapalı dosyaları al

    # Dosya kodlarını çekme
    dosya_kodlari = list(set([dosya.dosya_kodu for dosya in dosya_objects]))

    plot_data = {}

    # Her bir dosya kodu için ayrı analiz yapma
    for dosya_kodu in dosya_kodlari:
        dosyalar = dosya_objects.filter(dosya_kodu=dosya_kodu)
        acilis_tarihleri = [dosya.DosyaAcilisTarihi for dosya in dosyalar if dosya.DosyaKapatmaTarihi]
        kapanma_tarihleri = [dosya.DosyaKapatmaTarihi for dosya in dosyalar if dosya.DosyaKapatmaTarihi]

        kapanma_sureleri = [(kapanma - acilis).days for acilis, kapanma in zip(acilis_tarihleri, kapanma_tarihleri) if kapanma]

        ortalama_kapanma_suresi = np.mean(kapanma_sureleri)

        plt.figure(figsize=(10, 6))
        plt.hist(kapanma_sureleri, bins=20, color='blue', alpha=0.7)
        plt.axvline(ortalama_kapanma_suresi, color='red', linestyle='dashed', linewidth=1.5, label=f'Ortalama: {ortalama_kapanma_suresi:.2f} gün')
        plt.title(f'Dosya Kodu: {dosya_kodu} - Ortalama Kapanma Süresi Analizi')
        plt.xlabel('Kapanma Süresi (gün)')
        plt.ylabel('Dosya Sayısı')
        plt.legend()
        plt.grid()

        # Save the plot to the media directory
        plot_file = os.path.join(settings.MEDIA_ROOT, f"{dosya_kodu}_dosya_closing_time_analysis.png")
        plt.savefig(plot_file)
        plt.close()

        # Create the absolute URL for the saved plot file
        plot_file_url = request.build_absolute_uri(settings.MEDIA_URL + f"{dosya_kodu}_dosya_closing_time_analysis.png")

        dosya_listesi = []
        for dosya, kapanma_suresi in zip(dosyalar, kapanma_sureleri):
            dosya_data = {
                'id': dosya.id,
                'dosya_kodu': dosya.dosya_kodu,
                'yil': dosya.yil,
                'sayi': dosya.sayi,
                'DosyaAcilisTarihi': dosya.DosyaAcilisTarihi,
                'DosyaKapatmaTarihi': dosya.DosyaKapatmaTarihi,
                'kapanma_suresi': kapanma_suresi,  # Doğru kapanma süresini burada kullan
            }
            dosya_listesi.append(dosya_data)

        plot_data[dosya_kodu] = {
            'ortalama_kapanma_suresi': ortalama_kapanma_suresi,
            'plot_file_url': plot_file_url,
            'dosyalar': dosya_listesi,  # Doğru dosya verilerini de sakla
            'kapanma_sureleri': kapanma_sureleri  # Doğru kapanma sürelerini de sakla
        }

    context = {
        'plot_data': plot_data,
        'dosya_kodlari': dosya_kodlari,
    }

    return render(request, 'dosya_closing_time_by_code_analysis.html', context)

