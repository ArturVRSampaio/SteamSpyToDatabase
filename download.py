import requests
import json

url = "https://steamspy.com/api.php"

all_data = []  # Lista para armazenar todos os dados

for page in range(0, 70):
    print(page)
    params = {"request": "all", "page": page}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        all_data.append(data)
    else:
        print(f"Erro ao fazer a solicitação para a página {page}. Código de status: {response.status_code}")

# Salvar todos os dados em um único arquivo JSON
with open("output.json", "w", encoding="utf-8") as file:
    json.dump(all_data, file, ensure_ascii=False, indent=4)
