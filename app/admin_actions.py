import pandas as pd
from datetime import datetime
from django.contrib import messages
from .models import Colaborador

def importar_excel(modeladmin, request, arquivo):
    try:
        # Lê o arquivo Excel, pulando as duas primeiras linhas que são cabeçalho
        df = pd.read_excel(arquivo, skiprows=2)
        
        # Normaliza os nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Mapeamento de colunas
        mapeamento_colunas = {
            'Matrícula': 'Matrícula',
            'Nome': 'Nome',
            'Data de admissão': 'Data de admissão',
            'CPF': 'CPF',
            'PIS': 'PIS',
            'Cargo': 'Cargo',
            'Equipe': 'Equipe',
            'Turno': 'Turno',
            'Centro de custo': 'Centro de custo'
        }
        
        # Renomeia as colunas conforme o mapeamento
        df = df.rename(columns=lambda x: mapeamento_colunas.get(x, x))
        
        # Remove linhas vazias
        df = df.dropna(subset=['Matrícula'])
        
        # Mapeamento dos dias da semana em português para inglês
        dias_semana = {
            'Seg': 'Mon',
            'Ter': 'Tue',
            'Qua': 'Wed',
            'Qui': 'Thu',
            'Sex': 'Fri',
            'Sab': 'Sat',
            'Dom': 'Sun'
        }
        
        # Converte as datas do formato brasileiro para o formato do pandas
        def converter_data(data_str):
            for pt, en in dias_semana.items():
                data_str = data_str.replace(pt, en)
            return pd.to_datetime(data_str, format='%a, %d/%m/%Y')
        
        # Aplica a conversão na coluna de data
        df['Data de admissão'] = df['Data de admissão'].apply(converter_data)
        
        registros_criados = 0
        registros_atualizados = 0
        erros = []
        
        for index, row in df.iterrows():
            try:
                colaborador, created = Colaborador.objects.update_or_create(
                    matricula=str(int(row['Matrícula'])),
                    defaults={
                        'nome': row['Nome'],
                        'data_admissao': row['Data de admissão'],
                        'cpf': row['CPF'],
                        'pis': row['PIS'],
                        'cargo': row['Cargo'],
                        'turno': row['Turno'],
                        'centro_custo': row['Centro de custo']
                    }
                )
                if created:
                    registros_criados += 1
                else:
                    registros_atualizados += 1
                    
            except Exception as e:
                erro_msg = f"Erro na linha {index + 3}: {str(e)}"  # +3 porque pulamos 2 linhas
                erros.append(erro_msg)
        
        if registros_criados > 0 or registros_atualizados > 0:
            messages.success(
                request, 
                f'Importação concluída! {registros_criados} registros criados e {registros_atualizados} atualizados.'
            )
        
        if erros:
            messages.error(
                request,
                f'Ocorreram {len(erros)} erros durante a importação:\n' + '\n'.join(erros)
            )
            
    except Exception as e:
        messages.error(request, f'Erro ao importar arquivo: {str(e)}')