import requests
import json
from dotenv import load_dotenv
import os

# Buscando os dados de autenticação no .env
load_dotenv() 
client_key_value = os.getenv('CLIENT_KEY')
client_secret_value = os.getenv('CLIENT_SECRET')


#  Função para retorna o token de acesso
def get_access_token(client_key, client_secret):
    token_url = 'https://api.intelliauto.com.br/v1/login'
    token_payload = {
        'clientKey': client_key,
        'clientSecret': client_secret
    }
    token_response = requests.post(token_url, json=token_payload)
    if token_response.status_code == 200:
        return token_response.json().get('accessToken')
    return None


# Função para gerar um aquivo de token
def gerar_arquivo_token():
    token = get_access_token(client_key_value, client_secret_value)
    with open("token.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(token)


# Função para ler o token no arquivo txt
def ler_txt_token():
    try:
        with open("token.txt", "r", encoding="utf-8") as arquivo:
            access_token = arquivo.read()
            return access_token
        
# Se não existir o token, executa a função de gerar o token
# E em seguida executa novamente a função ler_txt_token
    except FileNotFoundError:
        gerar_arquivo_token()
        ler_txt_token()


