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
    benchmarks = json.load(f)

# Modelo para requisição
class EstimativaRequest(BaseModel):
    investimento: int
    categoria: str
    localizacao: dict
    tipo_campanha: str
    access_token: str
    age_min: int
    age_max: int
    gender: list[int]
    interests: list[int]

def estimar_alcance(investimento, categoria, localizacao, tipo_campanha, access_token, age_min, age_max, gender_list, interests):
    campanha = benchmarks[tipo_campanha]
    setor = campanha["setores"][categoria]
    ctr = setor["ctr"]
    cpc = setor["cpc"]

    tamanho_publico = 1000000 # Exemplo de 1 milhão
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
        # Tentar calcular o alcance estimado
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

    except HTTPException as http_exc:
        # Repassar exceções já tratadas como HTTPException
        raise http_exc

    except Exception as e:
        # Capturar erros não previstos e retornar uma mensagem genérica
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")
