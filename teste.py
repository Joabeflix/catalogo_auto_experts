import requests

url = "https://atacadao186732.protheus.cloudtotvs.com.br:10357/rest/wsrsys/pedido/faturado?notainicial=000000001&notafinal=00000003"

username = "ecommerce"
password = "123456"

response = requests.get(url, auth=(username, password))

if response.status_code == 200:
    print("Sucesso!")
    print(response.json())
else:
    print(f"Erro {response.status_code}: {response.text}")
