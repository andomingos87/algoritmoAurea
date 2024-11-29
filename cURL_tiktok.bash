curl --location 'http://127.0.0.1:8000' \
    --header 'Access-Token: 85d5230c0ca61ef5f741e1ea7aa045e49e895740' \
    --header 'Content-Type: application/json' \
    --data '{
    "advertiser_id": "7420919198131732481",
    "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
    "objective_type": "REACH",
    "optimization_goal": "CLICK",
    "location_ids": [
        "6252001"
    ],
    "auto_targeting_enabled": true
}'

curl --location 'http://127.0.0.1:8000' \
    --header 'Access-Token: 85d5230c0ca61ef5f741e1ea7aa045e49e895740' \
    --header 'Content-Type: application/json' \
    --data '{
    "advertiser_id": "7420919198131732481",
    "placement_type": "PLACEMENT_TYPE_AUTOMATIC",  // Configuração automática de colocação
    "objective_type": "REACH",
    "optimization_goal": "CLICK",
    "location_ids": [
        "6252001"
    ],
    "gender": "GENDER_UNLIMITED",
    "age_groups": ["AGE_18_24", "AGE_25_34"],
    "interest_categories": [
        123456789,
        987654321
    ],
    "auto_targeting_enabled": false
}'
