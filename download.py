import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

url = "https://steamspy.com/api.php"
all_data = []

def remove_last_comma(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find the last comma and its position
    last_comma_index = content.rfind(',')
    if last_comma_index != -1:
        # Remove the last comma
        content = content[:last_comma_index] + content[last_comma_index + 1:]

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Last comma removed from {file_path}")
    else:
        print("No comma found in the file.")

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

remove_last_comma("output.json")

with open("output.json", "a", encoding="utf-8") as file:
    file.write("}")

end_time = time.time()
total_time = end_time - start_time
print(f"Total time spent: {total_time} seconds")
