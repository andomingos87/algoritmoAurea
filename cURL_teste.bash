curl -X POST "http://127.0.0.1:8000/estimativa" \
-H "Content-Type: application/json" \
-d '{
  "investimento": 5000,
  "categoria": "Varejo",
  "localizacao": {
    "pais": "BR",
    "estado": "São Paulo",
    "cidade": "Guarulhos"
  },
  "tipo_campanha": "Alcance e visibilidade",
  "access_token": "EAALLu500ZAVEBOZBspgec0wFbAblLUnz5NhBMLzKpMlcaXEkTfClxxjkMuqMIPxhBZCXeHcPHZA0z99l9mCnVhQpo7bNOLn2SS3jv7ZByg6L6E8Yov9JZBL88yY01oHBf3cIHY7tpnckwZCKQMlZAHXpRQNn8hcETb1D1z6ZBk3WZABynqxSq5WMZCVY4CBxCMbOoiIa51KFs7i",
  "age_min": 18,
  "age_max": 35,
  "gender": [1, 2],
  "interests": [6003029869785]
}'

curl -X POST http://127.0.0.1:8000/estimativa \
-H "Content-Type: application/json" \
-d '{
  "investimento": 1000,
  "categoria": "Varejo",
  "localizacao": {"pais": "BR"},
  "tipo_campanha": "Alcance e visibilidade",
  "access_token": "EAALLu500ZAVEBOZBspgec0wFbAblLUnz5NhBMLzKpMlcaXEkTfClxxjkMuqMIPxhBZCXeHcPHZA0z99l9mCnVhQpo7bNOLn2SS3jv7ZByg6L6E8Yov9JZBL88yY01oHBf3cIHY7tpnckwZCKQMlZAHXpRQNn8hcETb1D1z6ZBk3WZABynqxSq5WMZCVY4CBxCMbOoiIa51KFs7i",
  "age_min": 18,
  "age_max": 35,
  "gender": [1, 2],
  "interests": [6003029869785]
}'