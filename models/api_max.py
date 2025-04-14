import requests
import json
import os
import tkinter as tk
from PIL import Image, ImageTk
from dotenv import load_dotenv
from utils.utils import texto_no_console

load_dotenv()

class TokenGerador:
    def __init__(self):
        pass


    CLIENT_KEY=os.getenv('CLIENT_KEY')
    CLIENT_SECRET=os.getenv('CLIENT_SECRET')
 
    def pegar_token_de_acesso(self):
        token_url = 'https://api.intelliauto.com.br/v1/login'
        token_payload = {
            'clientKey': self.CLIENT_KEY,
            'clientSecret': self.CLIENT_SECRET
        }
        print(f'Arquivo enviado: {token_payload}')
        token_response = requests.post(token_url, json=token_payload)
        if token_response.status_code == 200:
            return token_response.json().get('accessToken')
        return None

    def gerar_arquivo_token(self):
        token = self.pegar_token_de_acesso()
        with open(r"configs\token.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(token)

    def ler_txt_token(self):
        try:
            with open(r"configs\token.txt", "r", encoding="utf-8") as arquivo:
                access_token = arquivo.read()
                return access_token
            
        except FileNotFoundError:
            self.gerar_arquivo_token()
            self.ler_txt_token()

class APICliente: 
    BASE_URL = 'https://api.intelliauto.com.br/v1/produtos/partnumber/'

    def __init__(self, token_manager):
        self.token_manager = token_manager

    def obter_dados(self, part_number):

        access_token = self.token_manager.ler_txt_token()
        url = f'{self.BASE_URL}{part_number}'
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            self.token_manager.gerar_arquivo_token()
            return self.obter_dados(part_number)

        if response.status_code == 200:
            return response

class FiltroJSON:
    @staticmethod
    def filtrar_dados(data, filtro_json, item_filtro=None):
        try:
            retorno = eval(f"data{filtro_json}")
        except Exception as e:
            print(f"Erro ao acessar dados com o filtro: {e}")
            return f""
        if item_filtro:
            try:
                filtrados = [dado for dado in retorno if dado.get("item") == item_filtro]
                return filtrados[0]['descricao']
            except IndexError:
                return f'"{item_filtro}" indisponível.'
        return retorno
    
def acerto_codigo_produto(codigo_produto):
    texto_saida = str(codigo_produto).replace(' ', '')

    # Ordenados por tamanho decrescente
    padroes = {
        "NCDE": " ",
        "NKF": " ",
        "N": " ",
        "MG": " ",
        "HG": " ",
        "AC": " ",
        "C": "-",
        "L": "-",
        "P": "-"
    }
    for padrao in padroes.keys():
        if texto_saida.startswith(padrao):

            retorno = f'{padrao}{padroes.get(padrao)}{texto_saida[len(padrao):]}'

            texto_no_console([f'Código alterado de: {codigo_produto}', f'Código alterado para: {retorno}'])

            return retorno


    return 'Sem formatação programada'

    
def puxar_dados_api(codigo_produto, dados_necessarios=[]):

    token_manager = TokenGerador()
    api_cliente = APICliente(token_manager)
    filtro = FiltroJSON()
    response = api_cliente.obter_dados(codigo_produto)
    dados = response.json()

    if dados['data'] == []:
        codigo_produto = acerto_codigo_produto(codigo_produto)
        response = api_cliente.obter_dados(codigo_produto)
        dados = response.json()
        
    if response:
        
        mapeamentos = {
            'nome': {
                'mapeamento': "['data'][0]['aplicacoes'][0]['descricao']",
                'mapeamento_secundario': False
            },
            'marca': {
                'mapeamento': "['data'][0]['marca']['nome']",
                'mapeamento_secundario': False
            },
            'aplicacao': {
                'mapeamento': "['data'][0]['aplicacoes'][0]['descricaoFrota']",
                'mapeamento_secundario': False
            },
            'ean': {
                'mapeamento': "['data'][0]['especificacoes']",
                'mapeamento_secundario': "Código de barras (EAN)"
            },
            'ncm': {
                'mapeamento': "['data'][0]['especificacoes']",
                'mapeamento_secundario': "NCM"
            },
            'peso': {
                'mapeamento': "['data'][0]['especificacoes']",
                'mapeamento_secundario': "Peso bruto"
            },
            'imagem_url': {
                'mapeamento': "['data'][0]['imagens'][0]['url']",
                'mapeamento_secundario': False
            },
            'cod_marca': {
                'mapeamento': "['data'][0]['partNumber']",
                'mapeamento_secundario': False
            },
            'json_completo': {
                'mapeamento': "['data']",
                'mapeamento_secundario': False
            }
        }

        lista_retorno = []

        for dado in dados_necessarios:

            if dado in mapeamentos.keys():
                mapeamento_primario = mapeamentos[dado]['mapeamento']
                mapeamento_secundario = mapeamentos[dado]['mapeamento_secundario']
                
                if mapeamento_secundario:
                    valor = filtro.filtrar_dados(dados, mapeamento_primario, mapeamento_secundario)
                    lista_retorno.append((dado, valor))
                
                else:
                    valor = filtro.filtrar_dados(dados, mapeamento_primario)
                    lista_retorno.append((dado, valor))


    return dict(lista_retorno)




if __name__ == "__main__":
    cod = 'NBJ7016DP'
    # url = puxar_dados_api(cod, ['nome', 'marca', 'aplicacao', 'ean', 'ncm', 'peso'])
    # url = puxar_dados_api(cod, ['cod_marca'])
    # print(type(url))

    # print(url)

    app = ImagemProduto(codigo_produto='HG32810')
    app.baixar_imagem()
    app.mostrar_imagem()



