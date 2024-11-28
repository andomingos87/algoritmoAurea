from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Define o modelo para os dados esperados na requisição
class AudienceEstimateRequest(BaseModel):
    advertiser_id: str
    placement_type: str
    objective_type: str
    optimization_goal: str
    location_ids: list
    auto_targeting_enabled: bool

@app.post("/estimate_audience/")
async def estimate_audience(request_data: AudienceEstimateRequest):
    # Endpoint e token de acesso
    url = "https://business-api.tiktok.com/open_api/v1.3/ad/audience_size/estimate/"
    headers = {
        "Access-Token": "85d5230c0ca61ef5f741e1ea7aa045e49e895740",
        "Content-Type": "application/json"
    }

    # Converte os dados recebidos para um dicionário
    data = request_data.dict()

    # Fazendo a chamada para o endpoint
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Verifica se houve erro na requisição
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
