from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PontoForm
from .utils import limpar_pdfs_temporarios

@receiver(post_save, sender=PontoForm)
def cleanup_temp_files(sender, **kwargs):
    """
    Signal para limpar arquivos temporários após cada visualização de ponto
    """
    limpar_pdfs_temporarios()