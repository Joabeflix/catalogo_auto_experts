import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utils.utils import texto_no_console, limpar_prompt, verificar_permissao_usuario, tela_aviso
from models.integracao_gs import IntegracaoGS
import os

integracao = IntegracaoGS(
    conta_de_servico_json=r'configs/conta_servico.json',
    nome_planilha='auto_experts',
    nome_aba='pag1'
)






class Interface:
    def __init__(self):
        self.dados_necessarios = ['cod marca', 'nome', 'marca', 'aplicacao', 'ean', 'peso']

        self.root = ttk.Window(themename='darkly', title='Catálogo Auto Experts')
        self.root.geometry('1270x745')

        self.entrada_filtro = ttk.Entry(self.root, width=35)
        self.entrada_filtro.place(x=10, y=20)

        self.tree_main = None
        self.carregar_arvore_de_dados()

        self.root.mainloop()

    
    def carregar_arvore_de_dados(self):

        if self.tree_main:
            self.tree_main.destroy()

        colunas_e_configs_arvore = {
            "Cód Produto": {
                "anchor_heading": 'center',
                "anchor_column": 'center',
                "width": 60
            },
            "Produto": {
                "anchor_heading": 'center',
                "anchor_column": 'center',
                "width": 60
            },
            "Marca": {
                "anchor_heading": 'center',
                "anchor_column": 'center',
                "width": 60
            },
            "Aplicação": {
                "anchor_heading": 'center',
                "anchor_column": 'center',
                "width": 60
            },
            "EAN": {
                "anchor_heading": 'center',
                "anchor_column": 'center',
                "width": 60
            },
            "Peso": {
                "anchor_heading": 'center',
                "anchor_column": 'center',
                "width": 60
            },
        }

        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Helvetica", 8), rowheight=30)
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        self.tree_main = ttk.Treeview(self.root, columns=list(colunas_e_configs_arvore.keys()), show="headings")

        for key, config in colunas_e_configs_arvore.items():
            self.tree_main.heading(key, text=key, anchor=config['anchor_heading'])
            self.tree_main.column(key, anchor=config['anchor_column'], width=config['width'])
        

        self.tree_main.place(x=10, y=65, width=1250, height=450)





app = Interface()








