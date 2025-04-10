import json
import numpy as np
import os
from tkinter import messagebox

def texto_no_console(obj):
    if isinstance(obj, list):
        print(f'{'.' * 120}')
        for t in obj:
            print(f'>>> {t}{'\n'}')
        return None
    print(f'{'.' * 120}')
    print(f'>>> {obj}{'\n'}{'.' * 120}')

def alterar_valor_json(caminho_json, chave, novo_valor):
    with open(file=caminho_json, mode='r', encoding='utf8') as arquivo:
        dados = json.load(arquivo)
    dados[chave] = novo_valor
    with open(file=caminho_json, mode='w', encoding='utf8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

def tela_aviso(titulo, mensagem, tipo):

    tipos = {
        "informacao": messagebox.showinfo,
        "erro": messagebox.showerror
    }
    if tipo in tipos.keys():
        texto_no_console('oi')
        return tipos.get(tipo)(title=titulo, message=mensagem) and texto_no_console('teste')
    texto_no_console([
        f'Tipo de tela não cadastrado na função: {tipo}', 
        f'Tipos cadastrados: {list(tipos.keys())}'])

def converter_int64_para_int(obj):
    """ Se não for int64 ele retorna o valor original."""
    if isinstance(obj, np.int64):
        return int(obj)
    return obj

def limpar_prompt(self, event=None):
    os.system('cls')



def verificar_permissao_usuario():
    with open(r'configuracoes/usuario.json') as arquivo:
        usuario = json.load(arquivo)['usuario']



    permisao_adm = {
        "estoque": False,
        "administrador": True
    }
    return permisao_adm.get(usuario)


