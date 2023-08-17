from django.apps import AppConfig

class DosyaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dosya'  # Uygulama adınızı buraya yazın

    def ready(self):
        import Dosya.signals
