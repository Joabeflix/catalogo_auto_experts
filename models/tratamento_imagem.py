from . api_max import puxar_dados_api
import os
import tkinter as tk
from PIL import Image, ImageTk
from utils.utils import texto_no_console
import requests



class ImagemProduto():
    def __init__(self, codigo_produto, marca_produto):
        self.codigo_produto = codigo_produto
        self.marca_produto=str(marca_produto).upper()

    def baixar_imagem_api_auto_experts(self):

        url = puxar_dados_api(self.codigo_produto, ['imagem_url'])['imagem_url']
        nome_arquivo = f"temp/{self.codigo_produto}.jpg"

        try:
    
            resposta = requests.get(url)
        
            if resposta.status_code == 200:
         
                with open(nome_arquivo, 'wb') as arquivo:
                    arquivo.write(resposta.content)
                texto_no_console(f"Imagem salva como {nome_arquivo}")
            else:
                texto_no_console(f"Erro ao baixar a imagem: {resposta.status_code}")
        except Exception as e:
            texto_no_console(f"Ocorreu um erro: {e}")

    def baixar_imagem_idea2001(self):
        pd_url_marcas = {
            "SKF": "https://www.ideia2001.com.br/catmobile/FotoMobRetArq.asp?cerq=332&n=BRA",
            "COFAP": "",
            "SUSIN": "https://www.ideia2001.com.br/catmobile/FotoMobRetArq.asp?cerq=184&n=",
            "SYL": "https://www.ideia2001.com.br/catmobile/FotoMobRetArq.asp?cerq=65&n="       # 1800
        }

        try:
            url = f"{pd_url_marcas.get(self.marca_produto)}{self.codigo_produto}"
            nome_arquivo = f"temp/{self.codigo_produto}.jpg"

            try:
        
                resposta = requests.get(url)

                if resposta.status_code == 200:
            
            
                    with open(nome_arquivo, 'wb') as arquivo:
                        arquivo.write(resposta.content)
                    texto_no_console(f"Imagem salva como {nome_arquivo}")
                else:
                    texto_no_console(f"Erro ao baixar a imagem: {resposta.status_code}")
            except Exception as e:
                texto_no_console(f"Ocorreu um erro: {e}")

        except KeyError:
            texto_no_console("Marca não configurada para exibir foto, consulte o Joabe.")



    def mostrar_imagem(self):
        
        catalogo_idea = ['SKF', 'COFAP', 'SUSIN', 'SYL'],
        api_auto_experts = ['NAKATA', 'CONTROIL']

        self.funcao_baixar_imagem = self.baixar_imagem_api_auto_experts if self.marca_produto in api_auto_experts else self.baixar_imagem_idea2001


        janela = tk.Toplevel()
        janela.title(f'Imagem produto: {self.codigo_produto}')
        # janela.minsize(width=500, height=500)
        # janela.maxsize(width=500, height=500)

        image_path = f'temp/{self.codigo_produto}.jpg'
        texto_no_console(f"IMG path === {image_path}")
        try:
            img = Image.open(image_path)
            # img = img.resize((500, 500))
            tk_image = ImageTk.PhotoImage(img)

            label = tk.Label(janela, image=tk_image)
            label.image = tk_image  # Preserva a referência
            label.pack()

        except FileNotFoundError as e:
            janela.destroy()
            self.funcao_baixar_imagem()
            return self.mostrar_imagem()

        except Exception as e:
            texto_no_console(f"Erro ao exibir a imagem: {e}")

        
    def limpar_imagens(self):
        os.chdir('temp')
        for imagem in os.listdir():
            os.remove(imagem)
        os.chdir('..')

