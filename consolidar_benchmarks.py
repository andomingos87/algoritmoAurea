import json
import pandas as pd

def carregar_benchmarks(caminho_arquivo):
    """
    Carrega o arquivo benchmarks.json.

    Args:
        caminho_arquivo (str): Caminho para o arquivo JSON de benchmarks.

    Returns:
        dict: Dados carregados do JSON.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            benchmarks = json.load(file)
        return benchmarks
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        exit(1)

def consolidar_benchmarks(benchmarks):
    """
    Consolida os dados de benchmarks em um DataFrame.

    Args:
        benchmarks (dict): Dados de benchmarks carregados do JSON.

    Returns:
        pd.DataFrame: DataFrame consolidado com os benchmarks.
    """
    dados = []

    for tipo_campanha, campanha in benchmarks.get('campanhas', {}).items():
        setores = campanha.get('setores', {})
        for categoria, metrics in setores.items():
            row = {
                'Tipo Campanha': tipo_campanha.capitalize(),
                'Categoria': categoria
            }

            # Tratamento específico para cada tipo de campanha
            if tipo_campanha == 'trafego':
                row['CTR (%)'] = metrics.get('ctr_trafego', 0)
                row['CPC (BRL)'] = round(metrics.get('cpc_trafego_brl', 0), 2)
                row['CPM (BRL)'] = round(metrics.get('cpm_trafego_brl', 0), 2)
                row['CVR'] = None  # Não aplicável
                row['CPL (BRL)'] = None  # Não aplicável
            elif tipo_campanha == 'leads':
                row['CTR (%)'] = metrics.get('ctr_leads', 0)
                row['CPC (BRL)'] = round(metrics.get('cpc_leads_brl', 0), 2)
                row['CPM (BRL)'] = round(metrics.get('cpm_leads_brl', 0), 2)
                row['CVR'] = metrics.get('cvr_leads', 0)
                row['CPL (BRL)'] = round(metrics.get('cpl_leads_brl', 0), 2)
            else:
                # Se outros tipos de campanhas forem adicionados
                row['CTR (%)'] = metrics.get('ctr', 0)
                row['CPC (BRL)'] = round(metrics.get('cpc_brl', 0), 2)
                row['CPM (BRL)'] = round(metrics.get('cpm_brl', 0), 2)
                row['CVR'] = metrics.get('cvr', 0)
                row['CPL (BRL)'] = round(metrics.get('cpl_brl', 0), 2)

            dados.append(row)

    # Criar DataFrame
    df = pd.DataFrame(dados, columns=[
        'Tipo Campanha',
        'Categoria',
        'CTR (%)',
        'CPC (BRL)',
        'CPM (BRL)',
        'CVR',
        'CPL (BRL)'
    ])

    return df

def salvar_csv(df, caminho_saida):
    """
    Salva o DataFrame em um arquivo CSV.

    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        caminho_saida (str): Caminho para o arquivo CSV de saída.
    """
    try:
        df.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
        print(f"Planilha consolidada salva em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")
        exit(1)

def main():
    caminho_arquivo = 'benchmarks.json'  # Substitua pelo caminho do seu arquivo JSON
    caminho_saida = 'benchmarks_consolidado.csv'  # Nome do arquivo CSV de saída

    benchmarks = carregar_benchmarks(caminho_arquivo)
    df_consolidado = consolidar_benchmarks(benchmarks)
    salvar_csv(df_consolidado, caminho_saida)

if __name__ == "__main__":
    main()