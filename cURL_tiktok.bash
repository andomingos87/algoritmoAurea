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