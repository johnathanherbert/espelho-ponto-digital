import pandas as pd
from datetime import datetime
from django.contrib import messages
from .models import Colaborador

def importar_excel(modeladmin, request, arquivo):
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(arquivo)
        print("Colunas encontradas:", df.columns.tolist())  # Debug
        
        # Função para converter data
        def converter_data(data_str):
            if pd.isna(data_str):
                return None
            try:
                data_limpa = data_str.split(',')[-1].strip()
                return pd.to_datetime(data_limpa, format='%d/%m/%Y').date()
            except Exception as e:
                print(f"Erro ao converter data: {data_str} - {str(e)}")
                return None

        # Criar ou atualizar registros
        registros_atualizados = 0
        registros_criados = 0
        erros = []
        
        for index, row in df.iterrows():
            try:
                # Debug dos valores originais
                print(f"\nLinha {index + 2}:")
                print(f"CPF original: '{row['CPF']}'")
                print(f"PIS original: '{row['PIS']}'")

                dados = {
                    'matricula': str(row['Matrícula']).strip(),
                    'nome': str(row['Nome']).strip(),
                    'cpf': str(row['CPF']).strip() if pd.notna(row['CPF']) else None,
                    'pis': str(row['PIS']).strip() if pd.notna(row['PIS']) else None,
                    'cargo': str(row['Cargo']).strip(),
                    'turno': str(row['Turno']).strip(),
                    'centro_custo': str(row['Centro de custo']).strip(),
                    'data_admissao': converter_data(row['Data de admissão'])
                }

                # Adicionar data_demissao se existir
                if 'Data de demissão' in row and pd.notna(row['Data de demissão']):
                    dados['data_demissao'] = converter_data(row['Data de demissão'])

                # Debug dos dados a serem salvos
                print("Dados a serem salvos:", dados)
                
                colaborador, created = Colaborador.objects.update_or_create(
                    matricula=dados['matricula'],
                    defaults={k: v for k, v in dados.items() if k != 'matricula'}
                )
                
                if created:
                    registros_criados += 1
                else:
                    registros_atualizados += 1
                    
            except Exception as e:
                erro_msg = f"Erro na linha {index + 2}: {str(e)}"
                print(erro_msg)  # Debug
                erros.append(erro_msg)
        
        # Mensagens de feedback
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
        print(f"Erro na importação: {str(e)}")  # Debug
        messages.error(request, f'Erro ao importar arquivo: {str(e)}')