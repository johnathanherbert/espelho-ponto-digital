from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Gestão de Espelho de Ponto'

    def ready(self):
        import app.signals  # Importa os signals quando o app iniciar
