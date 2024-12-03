import tkinter as tk
from tkinter import ttk

# Criando a janela principal
root = tk.Tk()
root.title("Tabela de Dados")
root.geometry('500x500')

# Criando o Treeview
columns = ("Montadora", "Veículo", "Modelo", "Ano")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Configurando as colunas
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor=tk.CENTER)

# Inserindo dados
dados = [
    ("Volkswagen", "Gol", "G3", "1989, 1990, 1991, 1992, 1993"),
    ("Ford", "Ranger", "ST", "1992, 1993")
]

for item in dados:
    tree.insert("", tk.END, values=item)

tree.place(x=0, y=0)

# Iniciando o loop da interface
root.mainloop()
