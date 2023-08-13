from django.contrib import admin
from django import forms

from dal import autocomplete
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dosyalar.models import Dosyalar, CocugaBakimTurleri, CocuklaYakinlikTurleri, MahkemeRedNedenleri, NihaiSonucTurleri, Talep1980CK
from kisiler.models import Kisiler

# Register your models here.
# Define the customized form for Dosyalar
class DosyalarAdminForm(forms.ModelForm):
    class Meta:
        model = Dosyalar
        fields = '__all__'
        widgets = {
            'Cocuklar': autocomplete.ModelSelect2Multiple(
                url='cocuklar-autocomplete',  # Replace this with the URL pattern for CocuklarAutocomplete view
            ),
            'DosyaTuru': forms.Select(),  # Use the default Select widget for DosyaTuru
        }

    basvurucu = forms.ModelChoiceField(queryset=Kisiler.objects.all(), label='Başvurucu', widget=autocomplete.ModelSelect2(url='kisiler-autocomplete'))
    karsi_taraf = forms.ModelChoiceField(queryset=Kisiler.objects.all(), label='Karşı Taraf', widget=autocomplete.ModelSelect2(url='kisiler-autocomplete'))


# Register DosyalarAdmin with the customized form
class DosyalarAdmin(admin.ModelAdmin):
    form = DosyalarAdminForm
    # Define the search fields to enable search functionality
    search_fields = ['DosyaYil', 'DosyaNo', 'Cocuklar__Adi', 'Cocuklar__Soyadi']
    # Define the list display columns
    list_display = ['DosyaID', 'DosyaYil', 'DosyaNo', 'Aciklama', 'DosyaTuru', 'DosyaAcilisTarihi', 'DosyaKapatmaTarihi', 'DosyaDurumu', 'get_cocuklar']

    def get_cocuklar(self, obj):
        return ", ".join([cocuk.__str__() for cocuk in obj.Cocuklar.all()])

    get_cocuklar.short_description = 'Çocuklar'  # Set a custom column header

    # Define the list filter options for specific fields
    list_filter = ['DosyaYil', 'DosyaTuru', 'DosyaDurumu']


    def get_changeform_initial_data(self, request):
        latest_dosya = Dosyalar.objects.order_by('-DosyaYil', '-DosyaNo').first()
        initial_data = super().get_changeform_initial_data(request)
        if latest_dosya:
            initial_data['DosyaYil'] = latest_dosya.DosyaYil
            initial_data['DosyaNo'] = latest_dosya.DosyaNo + 1
        else:
            # If no existing records, provide default values
            initial_data['DosyaYil'] = 2022
            initial_data['DosyaNo'] = 1
        return initial_data

    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = list(self.readonly_fields)
    #     if obj and obj.pk:
    #         # If object is being edited (not during creation), add DosyaTuru to readonly_fields
    #         readonly_fields.append('DosyaTuru')
    #     return readonly_fields

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('DosyaTuru', 'DosyaYil', 'DosyaNo')
        return self.readonly_fields

    from django.http import HttpResponse
    from django.urls import path
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    # Custom admin action to save selected Dosyalar records as PDF
    def save_as_pdf_action(modeladmin, request, queryset):
        # Create a response object with PDF content type
        response = HttpResponse(content_type='application/pdf')
        # Set the filename for the PDF
        response['Content-Disposition'] = 'attachment; filename="dosyalar.pdf"'

        # Create a ReportLab canvas
        p = canvas.Canvas(response, pagesize=letter)

        # Write content to the PDF
        for dosya in queryset:
            p.drawString(100, 700, f"Dosya ID: {dosya.DosyaID}")
            p.drawString(100, 680, f"DosyaYil: {dosya.DosyaYil}")
            p.drawString(100, 680, f"DosyaYil: {dosya.DosyaYil}")

            # Add more fields as needed...

            # Move to the next page
            p.showPage()

        # Close the canvas
        p.save()

        return response



    def print_dosyalar(modeladmin, request, queryset):
        # Custom admin action for "Print"
        html = render_to_string('dosyalar_pdf.html', {'dosyalar_list': queryset})
        return HttpResponse(html)

    print_dosyalar.short_description = "Print"
  # Add custom actions to the DosyalarAdmin
    actions = [print_dosyalar, save_as_pdf_action]
admin.site.register(Dosyalar, DosyalarAdmin)
admin.site.register(CocugaBakimTurleri)
admin.site.register(CocuklaYakinlikTurleri)
admin.site.register(MahkemeRedNedenleri)
admin.site.register(NihaiSonucTurleri)
admin.site.register(Talep1980CK)