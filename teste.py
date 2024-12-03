import tkinter as tk
from tkinter import ttk

# Criando a janela principal
root = tk.Tk()
root.title("Tabela de Dados")

# Criando o Treeview
columns = ("Produto", "Quantidade", "Preço")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Configurando as colunas
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor=tk.CENTER)

# Inserindo dados
dados = [
    ("Parafuso", 50, "R$ 1,50"),
    ("Porca", 30, "R$ 0,80"),
    ("Arruela", 100, "R$ 0,30"),
]

for item in dados:
    tree.insert("", tk.END, values=item)

tree.pack(pady=20)

# Iniciando o loop da interface
root.mainloop()
