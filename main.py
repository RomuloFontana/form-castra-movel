import sqlite3
import pandas as pd
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog




# Função para criar a tabela
def criar_tabela():
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY,
                        data DATE,
                        nome TEXT NOT NULL,
                        contato INTEGER,
                        rg INTEGER,
                        cpf INTEGER,
                        nis INTEGER,
                        endereço TEXT,
                        bairro TEXT,
                        nome_pet TEXT,
                        especie TEXT,
                        cor TEXT,
                        peso TEXT,
                        idade INTEGER,
                        porte TEXT,
                        raca TEXT,
                        sexo TEXT)''')
    conexao.commit()
    conexao.close()

# Função para adicionar um novo usuário
def adicionar_usuario(data, nome, contato, rg, cpf, nis, endereço, bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO usuarios 
                    (data, nome, contato, rg, cpf, nis, endereço, bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (data, nome, contato, rg, cpf, nis, endereço, bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo))
    conexao.commit()
    conexao.close()
    messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")

# Função para listar todos os usuários
def listar_usuarios():
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM usuarios''')
    usuarios = cursor.fetchall()
    conexao.close()
    return usuarios

# Função para atualizar os dados de um usuário
def atualizar_usuario(id, data, nome, contato, rg, cpf, nis, endereço, bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''UPDATE usuarios 
                    SET data = ?, nome = ?, contato = ?, rg = ?, cpf = ?, nis = ?, endereço = ?, bairro = ?, 
                        nome_pet = ?, especie = ?, cor = ?, peso = ?, idade = ?, porte = ?, raca = ?, sexo = ? 
                    WHERE id = ?''', 
                    (data, nome, contato, rg, cpf, nis, endereço,bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo, id))
    conexao.commit()
    conexao.close()
    messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")

# Função para deletar um usuário
def deletar_usuario(id):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''DELETE FROM usuarios WHERE id = ?''', (id,))
    conexao.commit()
    conexao.close()
    messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!")

# Função para exportar dados para Excel
def exportar_para_excel():
    usuarios = listar_usuarios()
    df = pd.DataFrame(usuarios, columns=['ID', 'Data', 'Nome', 'Contato', 'RG', 'CPF', 'NIS', 'Endereço','Bairro', 'Nome do Pet',
                                        'Espécie', 'Cor', 'Peso', 'Idade', 'Porte', 'Raça', 'Sexo'])
    df.to_excel('usuarios.xlsx', index=False, engine='openpyxl')
    messagebox.showinfo("Sucesso", "Dados exportados para 'usuarios.xlsx' com sucesso!")


# Função para visualizar os dados em uma nova janela-------
def visualizar_dados():
    usuarios = listar_usuarios()
    
    janela_visualizacao = tk.Toplevel()
    janela_visualizacao.title("Visualização de Dados do Castra Móvel")
    
    # Definir o tamanho desejado para a janela
    largura_desejada = int(janela_visualizacao.winfo_screenwidth() * 0.9)
    altura_desejada = int(janela_visualizacao.winfo_screenheight() * 0.7)

    centralizar_janela(janela_visualizacao, largura_desejada, altura_desejada)

    # Criando o Frame para Treeview e barras de rolagem
    frame = tk.Frame(janela_visualizacao)
    frame.pack(fill=tk.BOTH, expand=True)

    # Criando o Treeview
    colunas = ["ID", "Data", "Nome", "Contato", "RG", "CPF", "NIS", "Endereço", "Bairro","Nome do Pet", "Espécie", "Cor", "Peso", "Idade", "Porte", "Raça", "Sexo"]
    tree = ttk.Treeview(frame, columns=colunas, show="headings")
    tree.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)



    # Inserindo os dados na tabela
    for usuario in usuarios:
        tree.insert("", tk.END, values=usuario)

    # Ajustando automaticamente o tamanho das colunas
    font = tkFont.Font()
    for i, coluna in enumerate(colunas):
        tree.heading(coluna, text=coluna)
        max_width = max(font.measure(str(item[i])) for item in usuarios)
        tree.column(coluna, anchor=tk.CENTER, width=max_width)

    # Adicionando barras de rolagem
    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
    
    scrollbar_x.pack(side="bottom", fill="x")
    scrollbar_y.pack(side="right", fill="y")



# Função para editar um usuário existente----------
def editar_usuario():
    id_usuario = simpledialog.askinteger("Editar Usuário", "Digite o ID do usuário que deseja editar:")
    if id_usuario is None:
        return
    
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM usuarios WHERE id = ?''', (id_usuario,))
    usuario = cursor.fetchone()
    conexao.close()
    
    if not usuario:
        messagebox.showerror("Erro", "Usuário não encontrado!")
        return
    
    janela_edicao = tk.Toplevel()
    janela_edicao.title("Editar Usuário")

    labels = ["Data", "Nome", "Contato", "RG", "CPF", "NIS", "Endereço", "Bairro", "Nome do Pet", 
            "Espécie", "Cor", "Peso", "Idade", "Porte", "Raça", "Sexo"]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(janela_edicao, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(janela_edicao)
        entry.insert(0, usuario[idx + 1])  # +1 porque o ID é o primeiro campo
        entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
        entries[label] = entry

    def salvar_edicao():
        dados = [entries[label].get() for label in labels]
        atualizar_usuario(id_usuario, *dados)
        janela_edicao.destroy()

    tk.Button(janela_edicao, text="Salvar", command=salvar_edicao).grid(row=len(labels), columnspan=2, pady=10)

## Função para deletar um usuário a partir da interface

def deletar_usuario():
    id_usuario = simpledialog.askinteger("Deletar Usuário", "Digite o ID do usuário que deseja deletar: ")
    if id_usuario is None:
        return
    conexao = sqlite3.connect("banco_dados.db")
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM usuarios WHERE id = ?''', (id_usuario,))
    usuario = cursor.fetchone()

    if not usuario:
        messagebox.showerror("Erro", "Usuário não encontrado!")
        return
    
    confirmacao = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar o usuário {usuario[2]}?")
    if confirmacao:
        deletar_usuario(id_usuario)


#-------------
def somente_numeros(char):
    return char.isdigit()


# Criando a Interface com Tkinter------------------------------------------------------------------

# Função para centralizar a janela e definir seu tamanho com base na resolução do monitor
def centralizar_janela(root, largura_desejada, altura_desejada):
    # Obter a largura e altura da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    # Calcular as coordenadas para centralizar a janela
    x = (largura_tela - largura_desejada) // 2
    y = (altura_tela - altura_desejada) // 2

    # Definir o tamanho e posição da janela
    root.geometry(f"{largura_desejada}x{altura_desejada}+{x}+{y}")

# Função para criar a interface
def criar_interface():
    root = tk.Tk()
    root.title("Cadastro Castra Móvel")
    
    # Definir tamanho desejado (por exemplo, 80% da largura da tela e 70% da altura da tela)
    largura_desejada = int(root.winfo_screenwidth() * 0.3)
    altura_desejada = int(root.winfo_screenheight() * 1.0)
    
    # Centralizar a janela
    centralizar_janela(root, largura_desejada, altura_desejada)
    
    # Labels e Entradas para os campos do formulário
    labels = ["Data:", "Nome:", "Contato:", "RG:", "CPF:", "NIS:", "Endereço:","Bairro", "Nome do Pet:", 
            "Espécie:", "Cor:", "Peso:", "Idade:", "Porte:", "Raça:", "Sexo:"]
    entries = {}
    
    for idx, label in enumerate(labels):
        tk.Label(root, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        if label in ["Espécie:", "Porte:", "Sexo:"]:
            if label == "Espécie:":
                values = ["Felino", "Canino"]
            elif label == "Porte:":
                values = ["Pequeno", "Médio", "Grande"]
            elif label == "Sexo:":
                values = ["Fêmea", "Macho"]
            entries[label] = ttk.Combobox(root, values=values, state="readonly", width=10)
        elif label in ["Data:","RG:", "CPF:", "Contato:", "NIS:"]:
            vcmd = (root.register(somente_numeros), '%S')
            entries[label] = tk.Entry(root, validate="key", validatecommand=vcmd, width=20)
        else:
            entries[label] = tk.Entry(root, width=30)
        entries[label].grid(row=idx, column=1, padx=10, pady=5, sticky="we")
    
    def salvar_dados():
        dados = [entries[label].get() for label in labels]
        adicionar_usuario(*dados)
    
    # Botões
    tk.Button(root, text="Salvar", command=salvar_dados, width=30).grid(row=len(labels), column=0, pady=5, columnspan=2, sticky="e")
    tk.Button(root, text="Deletar Usuário", command=deletar_usuario, width=30).grid(row=len(labels)+1, columnspan=2, pady=5, sticky="e")
    tk.Button(root, text="Visualizar Dados", command=visualizar_dados, width=30).grid(row=len(labels)+2, columnspan=2, pady=5, sticky="e")
    tk.Button(root, text="Editar Usuário", command=editar_usuario, width=30).grid(row=len(labels)+3, columnspan=2, pady=5, sticky="e")
    tk.Button(root, text="Exportar para Excel", command=exportar_para_excel, width=30).grid(row=len(labels)+4, column=1, pady=5,  sticky="e")
    
    # Inicia o loop da interface
    root.mainloop()

criar_tabela()
criar_interface()