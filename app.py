import requests
import os
from dotenv import load_dotenv
from token_gerador import gerar_arquivo_token, ler_txt_token


# token_acesso = get_access_token(client_key_value, client_secret_value)
def retorno_dados(part_number):

    access_token = ler_txt_token()

    url = f'https://api.intelliauto.com.br/v1/produtos/partnumber/{part_number}'
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
         gerar_arquivo_token()
         return retorno_dados(part_number)

    if response.status_code == 200:
        return response
    
def filtro_dados_json(part_number):

        data = retorno_dados(part_number).json()
        veiculos = data['data'][0]['aplicacoes'][0]['descricaoFrota']
        return veiculos

print(filtro_dados_json('AP 30460'))

