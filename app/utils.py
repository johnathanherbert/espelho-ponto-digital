import fitz # type: ignore
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from django.utils import timezone

def extrair_pagina_por_nome(pdf_path, nome_colaborador):
    try:
        with fitz.open(pdf_path) as pdf:
            print(f"\nProcurando por colaborador: {nome_colaborador}")
            print(f"Total de páginas no PDF: {len(pdf)}")
            
            for num, pagina in enumerate(pdf.pages()):
                texto = pagina.get_text()
                print(f"\nAnalisando página {num + 1}:")
                
                # Normaliza os textos para comparação
                texto_normalizado = texto.upper().strip()
                nome_normalizado = nome_colaborador.upper().strip()
                
                # Procura por variações do padrão
                padroes_busca = [
                    f"COLABORADOR: {nome_normalizado}",
                    f"COLABORADOR:{nome_normalizado}",
                    f"COLABORADOR : {nome_normalizado}",
                    nome_normalizado  # Busca só o nome também
                ]
                
                # Debug do texto encontrado
                if "COLABORADOR" in texto_normalizado:
                    print("Encontrou menção a COLABORADOR na página")
                    # Pega o contexto ao redor da palavra COLABORADOR
                    inicio = texto_normalizado.find("COLABORADOR")
                    print(f"Contexto: {texto_normalizado[inicio:inicio+100]}")
                
                # Tenta encontrar o nome usando os diferentes padrões
                for padrao in padroes_busca:
                    if padrao in texto_normalizado:
                        print(f"Encontrou padrão: {padrao}")
                        print(f"Extraindo página {num + 1}")
                        
                        # Cria um novo PDF com apenas esta página
                        novo_pdf = fitz.open()
                        novo_pdf.insert_pdf(pdf, from_page=num, to_page=num)
                        pdf_bytes = novo_pdf.write()
                        novo_pdf.close()
                        return ContentFile(pdf_bytes, name=f"{nome_colaborador}.pdf")
            
            print(f"\nNome não encontrado: {nome_colaborador}")
            print("Padrões procurados:", padroes_busca)
            return None
            
    except Exception as e:
        print(f"Erro ao processar PDF: {str(e)}")
        return None

def limpar_pdfs_temporarios():
    """
    Remove PDFs temporários antigos
    """
    temp_dir = 'temp_pdfs'
    if default_storage.exists(temp_dir):
        # Remove arquivos mais antigos que 1 hora
        for arquivo in default_storage.listdir(temp_dir)[1]:
            path = os.path.join(temp_dir, arquivo)
            if default_storage.get_modified_time(path) < timezone.now() - timezone.timedelta(hours=1):
                default_storage.delete(path)
