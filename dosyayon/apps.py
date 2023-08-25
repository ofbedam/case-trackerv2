# dosyayon/apps.py
from django.apps import AppConfig

class DosyayonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dosyayon'

    # def ready(self):
    #     # Register the signal handler
    #     import dosyayon.signals  # Importing here to avoid circular import
