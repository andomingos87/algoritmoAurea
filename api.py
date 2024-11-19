from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import math
import json

# Inicializa o FastAPI
app = FastAPI()

# Carrega os benchmarks do arquivo JSON
with open('benchmarks.json', 'r', encoding='utf-8') as f:
    benchmarks = json.load(f)["campanhas"]

# Modelo para requisição
class EstimativaRequest(BaseModel):
    investimento: float
    categoria: str
    localizacao: dict
    tipo_campanha: str
    access_token: str
    age_min: int
    age_max: int
    gender: list[int]
    interests: list[int]

# Função para obter o tamanho do público alvo
def obter_tamanho_publico(localizacao, access_token, age_min, age_max, gender_list, interests):
    url = "https://graph.facebook.com/v21.0/act_294128312846727/reachestimate"
    targeting_spec = {
        "geo_locations": {
            "countries": [localizacao["pais"]]
        },
        "age_min": age_min,
        "age_max": age_max,
        "genders": gender_list,
        "interests": interests
    }

    params = {
        "targeting_spec": json.dumps(targeting_spec),
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get("users_lower_bound", 0)
    else:
        raise HTTPException(status_code=400, detail=f"Erro ao consultar a API do Facebook: {response.status_code} - {response.text}")

# Função para estimar o alcance
def estimar_alcance(investimento, categoria, localizacao, tipo_campanha, access_token, age_min, age_max, gender_list, interests):
    if tipo_campanha not in benchmarks:
        raise ValueError("Tipo de campanha não encontrado nos benchmarks")

    campanha = benchmarks[tipo_campanha]
    if categoria not in campanha["setores"]:
        raise ValueError("Categoria não encontrada nos benchmarks")

    setor = campanha["setores"][categoria]
    ctr_key = f"ctr_{tipo_campanha}"
    cpc_key = f"cpc_{tipo_campanha}_brl"

    ctr = setor.get(ctr_key)
    cpc = setor.get(cpc_key)

    if not ctr or not cpc:
        raise ValueError("Dados de CTR ou CPC não encontrados para o setor e tipo de campanha fornecidos")

    tamanho_publico = obter_tamanho_publico(localizacao, access_token, age_min, age_max, gender_list, interests)

    numero_cliques = investimento / cpc
    numero_impressoes = numero_cliques / (ctr / 100)
    alcance_estimado = min(numero_impressoes, tamanho_publico)

    margem_erro = min(0.05 * investimento, 0.1 * alcance_estimado)
    alcance_estimado_com_margem = alcance_estimado + margem_erro

    return math.ceil(alcance_estimado_com_margem)

# Endpoint para estimativa de alcance
@app.post("/estimativa")
async def estimativa(request: EstimativaRequest):
    try:
        alcance = estimar_alcance(
            investimento=request.investimento,
            categoria=request.categoria,
            localizacao=request.localizacao,
            tipo_campanha=request.tipo_campanha,
            access_token=request.access_token,
            age_min=request.age_min,
            age_max=request.age_max,
            gender_list=request.gender,
            interests=request.interests
        )
        return {"alcance_estimado": alcance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Para executar a aplicação, use o comando: uvicorn nome_do_arquivo:app --reload
