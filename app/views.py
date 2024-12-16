from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.utils import timezone
from .models import Colaborador, EspelhoPonto, PontoForm
from .utils import extrair_pagina_por_nome
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.db.models import Count
from datetime import timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.views.static import serve
import mimetypes

def buscar_ponto(request, id_colaborador):
    colaborador = get_object_or_404(Colaborador, id_colaborador=id_colaborador)
    try:
        espelho = EspelhoPonto.objects.latest('data_envio')
        
        if not espelho.arquivo:
            messages.error(request, "Arquivo PDF não encontrado.")
            return render(request, 'buscar_id.html')
            
        pdf_extracao = extrair_pagina_por_nome(espelho.arquivo.path, colaborador.nome)
        
        if pdf_extracao:
            temp_path = f'temp_pdfs/{colaborador.nome}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            pdf_url = default_storage.save(temp_path, pdf_extracao)
            
            context = {
                'colaborador': colaborador,
                'pdf_url': default_storage.url(pdf_url),
                'now': timezone.now(),
                'espelho': espelho
            }
            return render(request, 'resultado_busca.html', context)
        else:
            messages.error(
                request, 
                f"Não foi possível encontrar o espelho de ponto para {colaborador.nome}. "
                "Verifique se o nome está exatamente igual ao que consta no PDF."
            )
            return render(request, 'buscar_id.html')
            
    except EspelhoPonto.DoesNotExist:
        messages.error(request, "Nenhum arquivo PDF foi enviado ainda.")
        return render(request, 'buscar_id.html')
    except Exception as e:
        messages.error(request, f"Erro ao processar o PDF: {str(e)}")
        return render(request, 'buscar_id.html')

def buscar_ponto_form(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        cpf = request.POST.get('cpf')
        
        try:
            colaborador = Colaborador.objects.get(matricula=matricula, cpf=cpf)
            espelho = EspelhoPonto.objects.latest('data_envio')
            
            if not espelho.arquivo:
                messages.error(request, "Arquivo PDF não encontrado.")
                return render(request, 'buscar_id.html')
            
            pdf_extracao = extrair_pagina_por_nome(espelho.arquivo.path, colaborador.nome)
            
            if pdf_extracao:
                # Cria o diretório temp_pdfs se não existir
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_pdfs')
                os.makedirs(temp_dir, exist_ok=True)
                
                # Salva o arquivo temporário
                temp_filename = f'{colaborador.nome}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf'
                temp_path = os.path.join('temp_pdfs', temp_filename)
                
                # Salva usando default_storage
                pdf_path = default_storage.save(temp_path, pdf_extracao)
                full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
                
                # Configura a resposta com os cabeçalhos corretos
                response = FileResponse(
                    open(full_path, 'rb'),
                    content_type='application/pdf'
                )
                response['Content-Disposition'] = f'inline; filename="{temp_filename}"'
                response['X-Frame-Options'] = 'SAMEORIGIN'
                
                context = {
                    'colaborador': colaborador,
                    'pdf_url': request.build_absolute_uri(settings.MEDIA_URL + pdf_path),
                    'now': timezone.now(),
                    'espelho': espelho,
                    'pdf_response': response,  # Adiciona a resposta ao contexto
                }
                
                return render(request, 'resultado_busca.html', context)
            else:
                messages.error(request, f"Não foi possível encontrar o espelho de ponto para {colaborador.nome}")
                
        except Exception as e:
            messages.error(request, f"Erro ao processar a solicitação: {str(e)}")
            print(f"Erro detalhado: {str(e)}")
    
    return render(request, 'buscar_id.html')

# Adicione esta view para servir os PDFs
def serve_pdf(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print(f"Tentando servir PDF: {file_path}")  # Debug
    print(f"O arquivo existe? {os.path.exists(file_path)}")  # Debug
    
    if os.path.exists(file_path):
        try:
            response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="' + os.path.basename(file_path) + '"'
            response['X-Frame-Options'] = 'SAMEORIGIN'
            print(f"Cabeçalhos da resposta: {dict(response.headers)}")  # Debug
            return response
        except Exception as e:
            print(f"Erro ao servir PDF: {str(e)}")  # Debug
            return HttpResponse(f'Erro ao abrir arquivo: {str(e)}', status=500)
    
    print("Arquivo não encontrado")  # Debug
    return HttpResponse('Arquivo não encontrado', status=404)

def create_superuser(request):
    # Chave secreta para autorização
    SECRET_KEY = os.environ.get('DJANGO_SUPERUSER_KEY', 'sua-chave-secreta-aqui')
    
    # Verifica se a chave fornecida na URL está correta
    if request.GET.get('key') != SECRET_KEY:
        return HttpResponse("Acesso não autorizado", status=403)
    
    try:
        # Verifica se já existe um superusuário
        if User.objects.filter(is_superuser=True).exists():
            return HttpResponse("Superusuário já existe!")
        
        # Cria o superusuário
        user = User.objects.create_superuser(
            username='admin',
            email='johnathan.herbert@gmail.com',
            password='070594teste'
        )
        
        return HttpResponse(f"Superusuário criado com sucesso!\nUsername: {user.username}\nSenha: sua-senha-segura-aqui")
    
    except Exception as e:
        return HttpResponse(f"Erro ao criar superusuário: {str(e)}")

