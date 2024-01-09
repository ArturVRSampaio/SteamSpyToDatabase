import mysql.connector
import json
import os
from dotenv import load_dotenv
import re

load_dotenv()
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_database = os.getenv("MYSQL_DATABASE")

# Conectar ao banco de dados MySQL
connection = mysql.connector.connect(
    user=db_user,
    password=db_password,
    database=db_database,
    port='8005',
    charset='utf8mb4',  # Adicione isso para suportar uma gama mais ampla de caracteres
)

# Criar um cursor para executar consultas SQL
cursor = connection.cursor()

# Abrir o arquivo output.json como um arquivo de texto
with open('output.json', 'r', encoding='utf-8') as file:
    # Carregar dados JSON como um dicionário
    data_dict = json.load(file)

    # Iterar sobre cada chave (ID de aplicativo) no dicionário
    for app_id, app_data in data_dict.items():
        # Substituir ou remover caracteres não suportados nas colunas 'name', 'developer', 'publisher'
        app_data["name"] = re.sub(r'[^\x00-\x7F]+', '', app_data["name"])
        app_data["developer"] = re.sub(r'[^\x00-\x7F]+', '', app_data["developer"])
        app_data["publisher"] = re.sub(r'[^\x00-\x7F]+', '', app_data["publisher"])

        # Construir a consulta SQL para inserir os dados na tabela
        query = f"""
            INSERT INTO steam_spy_data
            (appid, name, developer, publisher, score_rank, positive, negative, userscore,
            owners, average_forever, average_2weeks, median_forever, median_2weeks,
            price, initialprice, discount, ccu, languages, genre, tags)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Obter os valores dos dados do aplicativo
        values = (
            app_data.get("appid", None), app_data.get("name", None), app_data.get("developer", None),
            app_data.get("publisher", None), app_data.get("score_rank", None), app_data.get("positive", None),
            app_data.get("negative", None), app_data.get("userscore", None), app_data.get("owners", None),
            app_data.get("average_forever", None), app_data.get("average_2weeks", None),
            app_data.get("median_forever", None), app_data.get("median_2weeks", None),
            app_data.get("price", None), app_data.get("initialprice", None), app_data.get("discount", None),
            app_data.get("ccu", None), app_data.get("languages", None),
            app_data.get("genre", None), json.dumps(app_data.get("tags", {}))
        )

        # Executar a consulta SQL
        cursor.execute(query, values)

# Confirmar as alterações no banco de dados
connection.commit()

# Fechar o cursor e a conexão
cursor.close()
connection.close()
