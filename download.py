import requests
import json

url = "https://steamspy.com/api.php"

all_data = []

# download all games basic info
for page in range(0, 70):
    print("page " + str(page))
    params = {"request": "all", "page": page}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        all_data.append(data)
    else:
        print(f"Erro ao fazer a solicitação para a página {page}. Código de status: {response.status_code}")


with open("output.json", "w", encoding="utf-8") as file:
    file.write("{")
    for page in all_data:
        for item in page:
            print("item " + str(item))
            file.write("\"" + str(item) + "\"" + " : ")
            params = {"request": "appdetails", "appid": item}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write(",")

            else:
                print(f"Erro ao fazer a solicitação para a página {item}. Código de status: {response.status_code}")

    file.write("}")
