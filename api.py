from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import json

# Inicializa o FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens; altere conforme necessário.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega os benchmarks do arquivo JSON
with open('benchmark.json', 'r', encoding='utf-8') as f:
    benchmarks = json.load(f)

# Modelo para requisição
class EstimativaRequest(BaseModel):
    investimento: int
    categoria: str
    tamanho_publico: int  # Novo parâmetro para receber o tamanho do público
    localizacao: dict
    access_token: str
    age_min: int
    age_max: int
    gender: list[int]
    interests: list[int]

def estimar_alcance(investimento, categoria, tamanho_publico, age_min, age_max, gender_list, interests):
    # Obter dados do benchmark para "Alcance e Visibilidade" e categoria especificada
    campanha = benchmarks["Alcance e Visibilidade"]
    setor = campanha["setores"].get(categoria)
    if not setor:
        raise Exception(f"Categoria '{categoria}' não encontrada nos benchmarks.")
    cpm = setor["cpm"]  # Usando CPM para calcular impressões

    # Calcula o número de impressões estimadas
    numero_impressoes = (investimento / cpm) * 1000  # Multiplica por 1000 porque o CPM é o custo por mil impressões

    # Define uma frequência média esperada
    frequencia_media = campanha.get("frequencia_media", 1.2)

    # Calcula o alcance estimado
    alcance_estimado = numero_impressoes / frequencia_media

    # O alcance não pode ser maior que o tamanho do público
    alcance_estimado = min(alcance_estimado, tamanho_publico)

    # Pode adicionar uma margem de erro se desejar
    margem_erro = min(0.05 * investimento, 0.1 * alcance_estimado)
    alcance_estimado_com_margem = alcance_estimado + margem_erro

    return math.ceil(alcance_estimado_com_margem)

# Endpoint para estimativa de alcance
@app.post("/estimativa-alcance")
async def estimativa(request: EstimativaRequest):
    try:
        # Tentar calcular o alcance estimado
        alcance = estimar_alcance(
            investimento=request.investimento,
            categoria=request.categoria,
            tamanho_publico=request.tamanho_publico,
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