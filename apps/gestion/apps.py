# gestion/apps.py
from django.apps import AppConfig


class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gestion' # Asegúrate de que el nombre de tu aplicación sea correcto

    def ready(self):
        import apps.gestion.signals.signals # Importa el módulo de señales aquí