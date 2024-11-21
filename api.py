from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import math
import json

# Inicializa o FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Isso permite todas as origens; altere conforme necessário.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega os benchmarks do arquivo JSON
with open('benchmarks.json', 'r', encoding='utf-8') as f:
    benchmarks = json.load(f)  # Carregando diretamente como uma lista

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
    # Busca a categoria no JSON
    setor = next((item for item in benchmarks if item["Categoria"] == categoria), None)
    if not setor:
        raise ValueError("Categoria não encontrada nos benchmarks")
    
    # Obtém as métricas necessárias
    ctr = float(setor.get("CTR (%)").replace(',', '.'))  # Converte para float
    cpc = float(setor.get("CPC (R$)").replace(',', '.'))  # Converte para float

    # Calcula o tamanho do público
    tamanho_publico = obter_tamanho_publico(localizacao, access_token, age_min, age_max, gender_list, interests)

    # Calcula o alcance estimado
    numero_cliques = investimento / cpc
    numero_impressoes = numero_cliques / (ctr / 100)
    alcance_estimado = min(numero_impressoes, tamanho_publico)

    # Adiciona margem de erro
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
        print(f"Erro interno: {e}")  # Log do erro para depuração
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

# Para executar a aplicação, use o comando: uvicorn nome_do_arquivo:app --reload
