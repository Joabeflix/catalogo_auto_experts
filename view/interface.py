import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utils.utils import texto_no_console, limpar_prompt, verificar_permissao_usuario, tela_aviso
from models.integracao_gs import IntegracaoGS
import os
from models.tratamento_imagem import ImagemProduto

integracao = IntegracaoGS(
    conta_de_servico_json=r'configs/conta_servico.json',
    nome_planilha='auto_experts',
    nome_aba='pag1'
)






class Interface:
    def __init__(self):

        self.root = ttk.Window(themename='cosmo', title='Catálogo Auto Experts')
        self.root.geometry('1270x745')

        self.planilha_google = integracao.conectar()
        self.dados_necessarios = ['cod marca', 'nome', 'marca', 'aplicacao', 'ean', 'peso']

        self.dados_atualizados = integracao.retorno_google_planilhas_pandas(planilha_google=self.planilha_google, dados_necessarios=self.dados_necessarios)

        ttk.Label(text='Pesquisar').place(x=10, y=4)
        self.entrada_filtro = ttk.Entry(self.root, width=22)
        self.entrada_filtro.place(x=10, y=35)

        self.entrada_filtro.bind('<Return>', self.filtrar_dados_interface)

        self.filtro_exato_variavel = tk.BooleanVar(value=False)
        self.checkbox_filtro_exato = ttk.Checkbutton(self.root, text="Pesquisa exata", variable=self.filtro_exato_variavel)
        self.checkbox_filtro_exato.place(x=340, y=40)

        self.botao_atualizar_catalogo = ttk.Button(self.root, text='Atualizar', command=lambda: self.atualizar_dados_interface())
        self.botao_atualizar_catalogo.place(x=255, y=35)

        self.codigo_produto = ttk.Entry(self.root, width=22)
        self.codigo_produto.place(x=10, y=600)

        self.marca_produto = ttk.Entry(self.root, width=22)
        self.marca_produto.place(x=100, y=600)

        self.botao_mostrar_imagem = ttk.Button(self.root, text='Ver Imagem', style='success-outline', command=lambda: self.mostrar_imagem_produto())
        self.botao_mostrar_imagem.place(x=260, y=600)




        self.arvore_de_dados = None
        self.carregar_arvore_de_dados()



        self.root.mainloop()


    def mostrar_imagem_produto(self):
        if self.codigo_produto.get():
            app = ImagemProduto(codigo_produto=self.codigo_produto.get(), marca_produto=self.marca_produto.get())
            app.mostrar_imagem()
    

    def atualizar_dados_interface(self):
        self.dados_atualizados = integracao.retorno_google_planilhas_pandas(
            planilha_google=self.planilha_google,
            dados_necessarios=self.dados_necessarios
        )
        if self.dados_atualizados:
            self.carregar_arvore_de_dados()
            texto_no_console("Interface atualizada com novas informações.")

    
    def carregar_arvore_de_dados(self):

        if self.arvore_de_dados:
            self.arvore_de_dados.destroy()

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

        self.arvore_de_dados = ttk.Treeview(self.root, columns=list(colunas_e_configs_arvore.keys()), show="headings")

        for key, config in colunas_e_configs_arvore.items():
            self.arvore_de_dados.heading(key, text=key, anchor=config['anchor_heading'])
            self.arvore_de_dados.column(key, anchor=config['anchor_column'], width=config['width'])
        

        self.arvore_de_dados.place(x=10, y=82, width=1250, height=450)
        
        if self.dados_atualizados:
            for row in self.dados_atualizados:
                self.arvore_de_dados.insert("", "end", values=row)

        self.arvore_de_dados.bind("<ButtonRelease-1>", self.adicionar_entry_item_selecionado)
        self.arvore_de_dados.bind("<<TreeviewSelect>>", self.adicionar_entry_item_selecionado) 

    def filtrar_dados_interface(self, event=None):
        self.arvore_de_dados.delete(*self.arvore_de_dados.get_children())

        try:
            query = self.entrada_filtro.get().strip().lower()
            filtro_exato = self.filtro_exato_variavel.get()

            if not query:
                self.carregar_arvore_de_dados()
                return

            query_parts = query.split()

            dados_filtrados = []

            for row in self.dados_atualizados:
                if filtro_exato:
                    if all(any(str(item).lower() == part for item in row) for part in query_parts):
                        dados_filtrados.append(row)
                else:
                    if all(any(part in str(item).lower() for item in row) for part in query_parts):
                        dados_filtrados.append(row)

            dados_filtrados.sort(key=lambda x: str(x[0]))


            for row in dados_filtrados:
                self.arvore_de_dados.insert("", "end", values=row)
            
        except Exception as e:
            texto_no_console(f"Erro ao filtrar dados: {e}")


    def adicionar_entry_item_selecionado(self, event=None):
        item_selecionado = self.arvore_de_dados.selection()
        if item_selecionado:
            valores = self.arvore_de_dados.item(item_selecionado[0])["values"]

            self.codigo_produto.delete(0, tk.END)
            self.codigo_produto.insert(0, valores[0])

            self.marca_produto.delete(0, tk.END)
            self.marca_produto.insert(0, valores[2])
            







app = Interface()








