import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

url = "https://steamspy.com/api.php"
all_data = []


def get_game_details(item):
    print("item :" + item)
    params = {"request": "appdetails", "appid": item}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        with open("output.json", "a", encoding="utf-8") as file:
            file.write(f'"{item}": {json.dumps(data, ensure_ascii=False, indent=4)},\n')
    else:
        print(f"Erro ao fazer a solicitação para a página {item}. Código de status: {response.status_code}")


start_time = time.time()

for page in range(0, 70):
    print("page " + str(page))
    params = {"request": "all", "page": page}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        all_data.extend(data)
    else:
        print(f"Erro ao fazer a solicitação para a página {page}. Código de status: {response.status_code}")

with open("output.json", "w", encoding="utf-8") as file:
    file.write("{")

with ThreadPoolExecutor() as executor:
    executor.map(get_game_details, all_data)

with open("output.json", "a", encoding="utf-8") as file:
    file.write("}")

end_time = time.time()
total_time = end_time - start_time
print(f"Total time spent: {total_time} seconds")