# dosyayon/apps.py
from django.apps import AppConfig

class DosyayonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dosyayon'

    def ready(self):
        import dosyayon.signals
