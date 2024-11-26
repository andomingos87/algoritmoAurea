from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('benchmark.json', 'r', encoding='utf-8') as f:
    benchmarks = json.load(f)

class EstimativaRequest(BaseModel):
    investimento: int
    categoria: str
    tamanho_publico: int
    localizacao: dict
    access_token: str

def estimar_alcance(investimento, categoria, tamanho_publico):
    campanha = benchmarks["Alcance e Visibilidade"]
    setor = campanha["setores"].get(categoria)
    if not setor:
        raise Exception(f"Categoria '{categoria}' não encontrada nos benchmarks.")
    
    # Dados do setor
    cpm = setor["cpm"]  # Custo por Mil Impressões
    taxa_engajamento = setor["taxa_engajamento"]  # Taxa de Engajamento (%)
    ctr = setor["ctr"]  # Taxa de Cliques (%)

    # Cálculo do número de impressões
    numero_impressoes = (investimento / cpm) * 1000

    # Cálculo do alcance estimado
    frequencia_media = campanha.get("frequencia_media", 1.2)
    alcance_estimado = numero_impressoes / frequencia_media
    alcance_estimado = min(alcance_estimado, tamanho_publico)
  
    # Ajuste com margem de erro
    margem_erro = min(0.05 * investimento, 0.1 * alcance_estimado)
    alcance_estimado_com_margem = alcance_estimado + margem_erro
    alcance_estimado_com_margem = min(alcance_estimado_com_margem, tamanho_publico)

    # Retorno dos resultados
    return {
        "alcance_estimado": math.ceil(alcance_estimado_com_margem)
    }

# Endpoint para estimativa de alcance
@app.post("/estimativa-alcance")
async def estimativa(request: EstimativaRequest):
    try:
        # Cálculo dos resultados
        resultados = estimar_alcance(
            investimento=request.investimento,
            categoria=request.categoria,
            tamanho_publico=request.tamanho_publico
        )
        return resultados

    except HTTPException as http_exc:
        # Repassar exceções já tratadas como HTTPException
        raise http_exc

    except Exception as e:
        # Capturar erros não previstos e retornar uma mensagem genérica
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")
