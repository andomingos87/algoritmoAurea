import requests
import math
import json

benchmarks = {
    "Tecnologia": {
        "ctr_trafego": 0.0151,
        "cpc_trafego": 0.77,
        "ctr_leads": 0.0250,
        "cpc_leads": 1.73
    }
}

def obter_tamanho_publico(localizacao, access_token):
    url = "https://graph.facebook.com/v21.0/act_294128312846727/reachestimate"
    targeting_spec = {
        "geo_locations": {
            "countries": [localizacao["pais"]]
        },
        "age_min": 20,
        "age_max": 40
    }
    params = {
        "targeting_spec": json.dumps(targeting_spec),  # Serializa para JSON
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:        
        data = response.json()
        # print("Resposta da API:", data) # Debug
        return data.get('data', {}).get("users_lower_bound", 0)
    else:
        raise Exception(f"Erro ao consultar a API do Facebook: {response.status_code}")

def estimar_alcance(investimento, categoria, localizacao, tipo_campanha, access_token):
    if categoria not in benchmarks:
        raise ValueError("Categoria não encontrada nos benchmarks")

    benchmark = benchmarks[categoria]
    ctr = benchmark[f"ctr_{tipo_campanha}"]
    cpc = benchmark[f"cpc_{tipo_campanha}"]

    tamanho_publico = obter_tamanho_publico(localizacao, access_token)

    numero_cliques = investimento / cpc
    print(f"Cliques: {numero_cliques}")

    custo_por_clique = investimento / numero_cliques
    print(f"Custo por clique: {custo_por_clique}")

    numero_impressoes = numero_cliques / ctr
    print(f"Impressões: {numero_impressoes}")
    print(f"CPM: {numero_impressoes/1000}")

    alcance_estimado = min(numero_impressoes, tamanho_publico)

    margem_erro = min(0.05 * investimento, 0.1 * alcance_estimado)
    alcance_estimado_com_margem = alcance_estimado + margem_erro

    return math.ceil(alcance_estimado_com_margem)

# Exemplo de uso
if __name__ == "__main__":
    investimento = 50
    categoria = "Tecnologia"
    localizacao = {"cidade": "Guarulhos", "estado": "SP", "pais": "BR"}
    tipo_campanha = "trafego"  # ou "leads"
    access_token = "EAALLu500ZAVEBOzEav61dUS2kZCmekRlkKsfWAcc8DAZATvZCNq2nhlZBtLeT0kOMD5mbxdZCIbrjViP9RKru9dJqrn8Bi8Lbo6aeCGtRKeqJdQjT9xZCTiEhIxK0BTVcZCOiRuWEfl5n47cgVT4Hg8DCxtHtwDC0zShcpRPaCmFWO8oW9BsDVDEea0chhU3Ad20AhGcI932"

    try:
        alcance = estimar_alcance(investimento, categoria, localizacao, tipo_campanha, access_token)
        print("Alcance estimado:", alcance)
    except Exception as e:
        print("Erro:", e)
