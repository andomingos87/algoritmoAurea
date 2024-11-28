from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.post("/estimate_audience/")
async def estimate_audience():
    # Endpoint e token de acesso
    url = "https://business-api.tiktok.com/open_api/v1.3/ad/audience_size/estimate/"
    headers = {
        "Access-Token": "85d5230c0ca61ef5f741e1ea7aa045e49e895740",
        "Content-Type": "application/json"
    }
    # Dados da requisição
    data = {
        "advertiser_id": "7420919198131732481",
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "objective_type": "REACH",
        "optimization_goal": "CLICK",
        "location_ids": ["6252001"],
        "auto_targeting_enabled": True
    }
    
    # Fazendo a chamada para o endpoint
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Verifica se houve erro na requisição
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
