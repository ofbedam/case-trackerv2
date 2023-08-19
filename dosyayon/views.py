## dosyayon/views.py
from django.shortcuts import render
from dal import autocomplete
from cocuklar.models import Cocuklar

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from yerler.models import Country, State, City
from kisiler.models import Kisiler
from django.views.generic import ListView
from Dosya.models import Dosya

class KisilerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Kisiler.objects.all()

        if self.q:
            qs = qs.filter(Adi__icontains=self.q)

        return qs


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Country.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class StateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = State.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs



class CocuklarAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Cocuklar.objects.all()

        if self.q:
            qs = qs.filter(Adi__icontains=self.q)

        return qs

def generate_pdf(request):
        # Create a response object with PDF content type
        response = HttpResponse(content_type='application/pdf')
        # Set the filename for the PDF
        response['Content-Disposition'] = 'attachment; filename="example.pdf"'

        # Create a ReportLab canvas
        p = canvas.Canvas(response, pagesize=letter)

        # Write content to the PDF
        p.drawString(100, 700, "Hello, this is a PDF generated using ReportLab!")

        # Close the canvas
        p.showPage()
        p.save()

        return response



# dosyayon/views.py

from django.shortcuts import render

def index(request):
    # Burada isteğe bağlı olarak ana sayfa için verileri hazırlayabilirsiniz
    return render(request, 'todo/base.html')