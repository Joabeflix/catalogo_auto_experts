import requests
import os
from dotenv import load_dotenv
from token_gerador import gerar_arquivo_token

print('Inicial')

def ler_txt_token():
    with open("token.txt", "r", encoding="utf-8") as arquivo:
        access_token = arquivo.read()
        return access_token

# token_acesso = get_access_token(client_key_value, client_secret_value)
def retorno_dados(url_valor):
    access_token = ler_txt_token()

    url = f'{url_valor}'
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
         print('Gerando um novo token')
         gerar_arquivo_token()
         print('Novo token gerado')
         return retorno_dados(url_valor)
    
    print('Verificando se o status é 200')
    if response.status_code == 200:
        print('Ok')
        return response
    
def retorno_veiculos(part_number):
        url = f'https://api.intelliauto.com.br/v1/produtos/partnumber/{part_number}'
        data = retorno_dados(url).json()
        veiculos = data['data'][0]['aplicacoes'][0]['veiculos']

        codigo_veiculos = [
            veiculo["codigo"]
            for veiculo in veiculos]
        
        lista_veiculos = []
        for codigo in codigo_veiculos:
            url = f'https://api.intelliauto.com.br/v1/veiculos/codigo/{codigo}'
            data = retorno_dados(url).json()
            
            resultado = {
                "marca": data["marca"],
                "nome": data["nome"],
                "modelo": data["modelo"],
                "anosDeVenda": data["anosDeVenda"]
            }
            lista_veiculos.append(resultado)

            # Transformando os dados em uma única variável formatada
            dados_formatados = "\n".join([
                f"{item['marca']} {item['nome']} {item['modelo']} ANO: {', '.join(map(str, item['anosDeVenda']))}"
                for item in lista_veiculos
            ])

        return dados_formatados
print(retorno_veiculos('AP 30460'))
