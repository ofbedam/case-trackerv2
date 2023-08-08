#kurumlar/admin.py


from django.contrib import admin
from kurumlar.models import Kurumlar, KurumTurleri, SehirIlce
from .forms import KurumlarForm

# Register your models here.
admin.site.register(KurumTurleri)
admin.site.register(SehirIlce)

class KurumlarAdmin(admin.ModelAdmin):
    form = KurumlarForm

admin.site.register(Kurumlar, KurumlarAdmin)

