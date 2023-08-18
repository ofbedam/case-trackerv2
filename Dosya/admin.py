from dal import autocomplete
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Dosya, CocugaBakimTurleri, CocuklaYakinlikTurleri, MahkemeRedNedenleri, NihaiSonucTurleri, Dosya1980CK


from django.contrib import admin
from django import forms

from .models import Dosya, DosyaIliski, DosyaIade, DosyaBilgi, Dosya1996, Dosya1980Velayet

class DosyaIliskiInline(admin.StackedInline):  # veya admin.TabularInline
    model = DosyaIliski  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği

class DosyaIadeInline(admin.StackedInline):  # veya admin.TabularInline
    model = DosyaIade  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği

class Dosya1996Inline(admin.StackedInline):  # veya admin.TabularInline
    model = Dosya1996  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği7

class Dosya1980VelayetInline(admin.StackedInline):  # veya admin.TabularInline
    model = Dosya1980Velayet  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği

class DosyaBilgiInline(admin.StackedInline):  # veya admin.TabularInline
    model = DosyaBilgi  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği


# class DosyaAdminForm(forms.ModelForm):
#     class Meta:
#         model = Dosya
#         fields = '__all__'
#
#     def clean(self):
#         cleaned_data = super().clean()
#         dosya_kodu = cleaned_data.get('dosya_kodu')
#         yil = cleaned_data.get('yil')
#         sayi = cleaned_data.get('sayi')
#
#         if dosya_kodu in ['A', 'B', 'C']:
#             if yil is not None and sayi is not None:
#                 # Kontrol edilecek kombinasyonu bulma
#                 existing_dosya = Dosya.objects.filter(
#                     dosya_kodu=dosya_kodu,
#                     yil=yil,
#                     sayi=sayi,
#                 ).exclude(pk=self.instance.pk).first()
#
#                 if existing_dosya:
#                     raise forms.ValidationError("Bu kombinasyon zaten mevcut.")


class DosyaAdminForm(forms.ModelForm):
    class Meta:
        model = Dosya
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        dosya_kodu = cleaned_data.get('dosya_kodu')
        yil = cleaned_data.get('yil')
        sayi = cleaned_data.get('sayi')

        if dosya_kodu in ['A', 'B', 'C']:
            if yil is not None and sayi is not None:
                existing_dosyalar = Dosya.objects.filter(
                    yil=yil,
                    sayi=sayi,
                ).exclude(dosya_kodu=dosya_kodu)

                error_messages = []
                for existing_dosya in existing_dosyalar:
                    error_messages.append(
                        f"[dosya_kodu= {dosya_kodu} Yil={yil} ve Sayi={sayi}] ile [dosya_kodu= {existing_dosya.dosya_kodu} Yil={existing_dosya.yil} ve Sayi={existing_dosya.sayi}] mükerrerdir."
                    )

                if error_messages:
                    raise forms.ValidationError(error_messages)


class DosyaAdminForm(forms.ModelForm):
    class Meta:
        model = Dosya
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        dosya_kodu = cleaned_data.get('dosya_kodu')
        yil = cleaned_data.get('yil')
        sayi = cleaned_data.get('sayi')

        if dosya_kodu in ['A', 'B', 'C']:
            existing_dosya = Dosya.objects.filter(
                dosya_kodu__in=['A', 'B', 'C'],
                yil=yil,
                sayi=sayi,
            ).exclude(pk=self.instance.pk).first()

            if existing_dosya:
                raise forms.ValidationError(
                    f"[dosya_kodu= {dosya_kodu} Yil={yil} ve Sayi={sayi}] ile [dosya_kodu= {existing_dosya.dosya_kodu} Yil={existing_dosya.yil} ve Sayi={existing_dosya.sayi}] mükerrerdir."
                )

        elif dosya_kodu in ['D']:
            existing_dosya = Dosya.objects.filter(
                dosya_kodu='D',
                yil=yil,
                sayi=sayi,
            ).exclude(pk=self.instance.pk).first()

            if existing_dosya:
                raise forms.ValidationError(
                    f"[dosya_kodu= {dosya_kodu} Yil={yil} ve Sayi={sayi}] ile [dosya_kodu= {existing_dosya.dosya_kodu} Yil={existing_dosya.yil} ve Sayi={existing_dosya.sayi}] mükerrerdir."
                )

        elif dosya_kodu in ['E']:
            existing_dosya = Dosya.objects.filter(
                dosya_kodu='E',
                yil=yil,
                sayi=sayi,
            ).exclude(pk=self.instance.pk).first()

            if existing_dosya:
                raise forms.ValidationError(
                    f"[dosya_kodu= {dosya_kodu} Yil={yil} ve Sayi={sayi}] ile [dosya_kodu= {existing_dosya.dosya_kodu} Yil={existing_dosya.yil} ve Sayi={existing_dosya.sayi}] mükerrerdir."
                )


@admin.register(Dosya)
class DosyaAdmin(admin.ModelAdmin):
    form = DosyaAdminForm
    search_fields = ['yil', 'sayi', 'Cocuklar__Adi', 'Cocuklar__Soyadi']
    # Define the list display columns
    list_display = ['id', 'dosya_kodu', 'yil', 'sayi', 'aciklama',  'DosyaAcilisTarihi',
                    'DosyaKapatmaTarihi', 'DosyaDurumu', 'get_cocuklar']

    def get_cocuklar(self, obj):
        return ", ".join([cocuk.__str__() for cocuk in obj.Cocuklar.all()])

    get_cocuklar.short_description = 'Çocuklar'  # Set a custom column header

    # Define the list filter options for specific fields
    list_filter = ['yil', 'dosya_kodu', 'DosyaDurumu']
    # list_display = ('dosya_kodu', 'yil', 'sayi', 'aciklama')
    # inlines = [DosyaIliskiInline, DosyaIadeInline, Dosya1980VelayetInline, Dosya1996Inline,DosyaBilgiInline]
    change_form_template = 'admin/dosya_change_form.html'
    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []

        dosya_kodu = obj.dosya_kodu
        if dosya_kodu == 'A':
            return [DosyaIadeInline(self.model, self.admin_site)]
        elif dosya_kodu == 'B':
            return [DosyaIliskiInline(self.model, self.admin_site)]
        elif dosya_kodu == 'C':
            return [Dosya1996Inline(self.model, self.admin_site)]
        elif dosya_kodu == 'D':
            return [Dosya1980VelayetInline(self.model, self.admin_site)]
        elif dosya_kodu == 'E':
            return [DosyaBilgiInline(self.model, self.admin_site)]

        return []

    def add_view(self, request, form_url='', extra_context=None):
        # Form ekranı yüklendiğinde, formset'in TOTAL_FORMS ve INITIAL_FORMS değerlerini belirtin
        if extra_context is None:
            extra_context = {}
        extra_context['dosyaiade-TOTAL_FORMS'] = 1  # İlk yüklemede 1 form gösterilecek
        extra_context['dosyaiade-INITIAL_FORMS'] = 0  # İlk yüklemede boş form

        latest_values = []

        dosya_kodlari = ['A', 'B', 'C', 'D', 'E']  # Tüm dosya kodları

        for dosya_kodu in dosya_kodlari:
            yil, sayi = Dosya.get_latest_yil_sayi(dosya_kodu)
            dosya_kodu_adi = dict(Dosya.DOSYA_KODLARI).get(dosya_kodu)

            if yil is not None and sayi is not None:
                latest_values.append({
                    'dosya_kodu': dosya_kodu,
                    'dosya_kodu_adi': dosya_kodu_adi,
                    'yil': yil,
                    'sayi': sayi,
                })

        latest_dosya_id = []

        dosya_kodlari = ['A', 'B', 'C', 'D', 'E']  # Tüm dosya kodları

        for dosya_kodu in dosya_kodlari:
            yil, sayi = Dosya.get_latest_dosya_id(dosya_kodu)
            dosya_kodu_adi = dict(Dosya.DOSYA_KODLARI).get(dosya_kodu)

            if yil is not None and sayi is not None:
                latest_dosya_id.append({
                    'dosya_kodu': dosya_kodu,
                    'dosya_kodu_adi': dosya_kodu_adi,
                    'yil': yil,
                    'sayi': sayi,
                })
        extra_context['latest_dosya_id'] = latest_dosya_id
        extra_context['latest_values'] = latest_values
        return super().add_view(request, form_url=form_url, extra_context=extra_context)





    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        latest_dosya = Dosya.objects.order_by('-yil', '-sayi').first()

        if latest_dosya:
            initial_data['yil'] = latest_dosya.yil
            initial_data['sayi'] = latest_dosya.sayi + 1
        else:
            initial_data['yil'] = 2022
            initial_data['sayi'] = 1



        latest_values = []

        dosya_kodlari = ['A', 'B', 'C', 'D', 'E']  # Tüm dosya kodları

        for dosya_kodu in dosya_kodlari:
            yil, sayi = Dosya.get_latest_yil_sayi(dosya_kodu)
            dosya_kodu_adi = dict(Dosya.DOSYA_KODLARI).get(dosya_kodu)

            if yil is not None and sayi is not None:
                latest_values.append(f"[dosya_kodu= {dosya_kodu_adi} Yil={yil} ve Sayi={sayi}]")

        initial_data['latest_values'] = '\n'.join(latest_values)
        return initial_data




class DosyaIadeForm(forms.ModelForm):
    class Meta:
        model = DosyaIade
        fields = '__all__'

# @admin.register(DosyaIade)
# class DosyaIadeAdmin(admin.ModelAdmin):
#     form = DosyaIadeForm
#     fieldsets = (
#         ('Dosya Bilgileri', {
#             'fields': ('dosya', 'neden')
#         }),
#         # ('Ek Bilgiler', {
#         #     'fields': ('diger_alan1', 'diger_alan2'),
#         #     'classes': ('collapse',)
#         # }),
#     )
#
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if obj:
#             form.base_fields['dosya'].disabled = True
#         return form
#
#
#
#
# class DosyaIadeAdminForm(forms.ModelForm):
#     dosya_kodu = forms.ChoiceField(choices=[(dosya.dosya_kodu, str(dosya)) for dosya in Dosya.objects.all()])
#
#     class Meta:
#         model = DosyaIade
#         fields = '__all__'
#
# @admin.register(DosyaIade)
# class DosyaIadeAdmin(admin.ModelAdmin):
#     form = DosyaIadeAdminForm


#
# class DosyaIadeAdminForm(forms.ModelForm):
#     yil = forms.IntegerField(widget=forms.HiddenInput())
#
#     sayi = forms.IntegerField()
#     aciklama = forms.CharField(widget=forms.Textarea, required=False)
#     neden = forms.CharField(max_length=50)
#
#
#
#     class Meta:
#         model = DosyaIade
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.initial['yil'] = self.instance.dosya.yil  # Dosya kaydının yil alanını alıp form alanına atar
# @admin.register(DosyaIade)
# class DosyaIadeAdmin(admin.ModelAdmin):
#     form = DosyaIadeAdminForm



admin.site.register(CocugaBakimTurleri)
admin.site.register(CocuklaYakinlikTurleri)
admin.site.register(MahkemeRedNedenleri)
admin.site.register(NihaiSonucTurleri)
admin.site.register(Dosya1980CK)