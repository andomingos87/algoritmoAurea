curl -X POST http://127.0.0.1:8000/estimativa-alcance \
-H "Content-Type: application/json" \
-d '{
  "investimento": 1000,
  "categoria": "Alimentação e Bebidas",
  "tamanho_publico": 1000000,
  "localizacao": {"pais": "Brasil", "estado": "SP"},
  "access_token": "EAALLu500ZAVEBOZBspgec0wFbAblLUnz5NhBMLzKpMlcaXEkTfClxxjkMuqMIPxhBZCXeHcPHZA0z99l9mCnVhQpo7bNOLn2SS3jv7ZByg6L6E8Yov9JZBL88yY01oHBf3cIHY7tpnckwZCKQMlZAHXpRQNn8hcETb1D1z6ZBk3WZABynqxSq5WMZCVY4CBxCMbOoiIa51KFs7i",
  "age_min": 18,
  "age_max": 65,
  "gender": [1],
  "interests": [6003029869785]
}'