#case tracker/ulkeler/admin.py

from django.contrib import admin
from ulkeler.models import Ulkeler
# Register your models here.

# Register Ulkeler, Kisiler, YasalTemsilciler models without customization
admin.site.register(Ulkeler)

