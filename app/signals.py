from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import PontoForm
from .utils import limpar_pdfs_temporarios

@receiver(post_save, sender=PontoForm)
def cleanup_temp_files(sender, **kwargs):
    """
    Signal para limpar arquivos temporários mais antigos que 5 minutos
    """
    # Modifica a função para manter arquivos recentes
    def limpar_pdfs_antigos():
        from django.core.files.storage import default_storage
        import os
        
        temp_dir = 'temp_pdfs'
        if default_storage.exists(temp_dir):
            # Remove apenas arquivos mais antigos que 5 minutos
            for arquivo in default_storage.listdir(temp_dir)[1]:
                path = os.path.join(temp_dir, arquivo)
                if default_storage.get_modified_time(path) < timezone.now() - timedelta(minutes=5):
                    default_storage.delete(path)
    
    limpar_pdfs_antigos()