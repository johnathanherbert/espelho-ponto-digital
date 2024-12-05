from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
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

def buscar_ponto(request, id_colaborador):
    colaborador = get_object_or_404(Colaborador, id_colaborador=id_colaborador)
    try:
        espelho = EspelhoPonto.objects.latest('data_envio')
        
        if not espelho.arquivo:
            return HttpResponse("Arquivo PDF não encontrado.", status=404)
            
        pdf_extracao = extrair_pagina_por_nome(espelho.arquivo.path, colaborador.nome)
        
        if pdf_extracao:
            response = HttpResponse(pdf_extracao, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{colaborador.nome}.pdf"'
            return response
        else:
            return HttpResponse(
                f"Não foi possível encontrar o espelho de ponto para o colaborador: {colaborador.nome}. "
                "Verifique se o nome está exatamente igual ao que consta no PDF.", 
                status=404
            )
    except EspelhoPonto.DoesNotExist:
        return HttpResponse("Nenhum arquivo PDF foi enviado ainda.", status=404)
    except Exception as e:
        return HttpResponse(f"Erro ao processar o PDF: {str(e)}", status=500)

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
            
            print(f"\nBuscando espelho para:")
            print(f"Nome: {colaborador.nome}")
            print(f"Arquivo: {espelho.arquivo.path}")
            
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
                
        except Colaborador.DoesNotExist:
            messages.error(request, "Matrícula ou CPF inválidos.")
        except EspelhoPonto.DoesNotExist:
            messages.error(request, "Nenhum arquivo de ponto foi enviado ainda.")
        except Exception as e:
            messages.error(request, f"Erro ao processar a solicitação: {str(e)}")
            print(f"Erro detalhado: {str(e)}")
    
    return render(request, 'buscar_id.html')

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

