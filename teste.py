import sqlite3
import pandas as pd
import tkinter as tk
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
                        nome_pet TEXT,
                        especie TEXT,
                        cor TEXT,
                        peso REAL,
                        idade INTEGER,
                        porte TEXT,
                        raca TEXT,
                        sexo TEXT)''')
    conexao.commit()
    conexao.close()

# Função para adicionar um novo usuário
def adicionar_usuario(data, nome, contato, rg, cpf, nis, endereço, nome_pet, especie, cor, peso, idade, porte, raca, sexo):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO usuarios 
                      (data, nome, contato, rg, cpf, nis, endereço, nome_pet, especie, cor, peso, idade, porte, raca, sexo) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (data, nome, contato, rg, cpf, nis, endereço, nome_pet, especie, cor, peso, idade, porte, raca, sexo))
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
def atualizar_usuario(id, data, nome, contato, rg, cpf, nis, endereço, nome_pet, especie, cor, peso, idade, porte, raca, sexo):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''UPDATE usuarios 
                      SET data = ?, nome = ?, contato = ?, rg = ?, cpf = ?, nis = ?, endereço = ?, 
                          nome_pet = ?, especie = ?, cor = ?, peso = ?, idade = ?, porte = ?, raca = ?, sexo = ? 
                      WHERE id = ?''', 
                      (data, nome, contato, rg, cpf, nis, endereço, nome_pet, especie, cor, peso, idade, porte, raca, sexo, id))
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

#------------------Se der errado, abrir essa função
# def exportar_para_excel():
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM usuarios''')
    usuarios = cursor.fetchall()

    # Converter os dados para um DataFrame do pandas
    df = pd.DataFrame(usuarios, columns=['ID', "data", "nome", "contato", "rg", "cpf", "nis", "endereço", "especie", "cor", "peso", "idade", "porte", "raca", "sexo"])

    # Salvar o DataFrame em um arquivo Excel
    df.to_excel('usuarios.xlsx', index=False, engine='openpyxl')
    
    print("Dados exportados para 'usuarios.xlsx' com sucesso!")
    conexao.close()
#---------------------------

# Função para exportar dados para Excel
def exportar_para_excel():
    usuarios = listar_usuarios()
    df = pd.DataFrame(usuarios, columns=['ID', 'Data', 'Nome', 'Contato', 'RG', 'CPF', 'NIS', 'Endereço', 'Nome do Pet',
                                         'Espécie', 'Cor', 'Peso', 'Idade', 'Porte', 'Raça', 'Sexo'])
    df.to_excel('usuarios.xlsx', index=False, engine='openpyxl')
    messagebox.showinfo("Sucesso", "Dados exportados para 'usuarios.xlsx' com sucesso!")


#-------Função para exportar dados para CSV
#------------------------
# def exportar_para_csv():
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM usuarios''')
    usuarios = cursor.fetchall()

    # Converter os dados para um DataFrame do pandas
    df = pd.DataFrame(usuarios, columns=['ID',"data", "nome", "contato", "rg", "cpf", "nis", "endereço", "especie", "cor", "peso", "idade", "porte", "raca", "sexo"])

    # Salvar o DataFrame em um arquivo CSV
    df.to_csv('usuarios.csv', index=False)
    
    print("Dados exportados para 'usuarios.csv' com sucesso!")
    conexao.close()
#--------------------

def exportar_para_csv():
    usuarios = listar_usuarios()
    df = pd.DataFrame(usuarios, columns=['ID', 'Data', 'Nome', 'Contato', 'RG', 'CPF', 'NIS', 'Endereço', 'Nome do Pet',
                                         'Espécie', 'Cor', 'Peso', 'Idade', 'Porte', 'Raça', 'Sexo'])
    df.to_csv('usuarios.csv', index=False)
    messagebox.showinfo("Sucesso", "Dados exportados para 'usuarios.csv' com sucesso!")


# Função para visualizar os dados em uma nova janela
def visualizar_dados():
    usuarios = listar_usuarios()
    
    janela_visualizacao = tk.Toplevel()
    janela_visualizacao.title("Visualização de Dados")
    
    text_area = tk.Text(janela_visualizacao)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    text_area.insert(tk.END, "ID\tData\tNome\tContato\tRG\tCPF\tNIS\tEndereço\tNome do Pet\tEspécie\tCor\tPeso\tIdade\tPorte\tRaça\tSexo\n")
    text_area.insert(tk.END, "-"*120 + "\n")
    
    for usuario in usuarios:
        text_area.insert(tk.END, "\t".join(map(str, usuario)) + "\n")


# Função para editar um usuário existente
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

    labels = ["Data", "Nome", "Contato", "RG", "CPF", "NIS", "Endereço", "Nome do Pet", 
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


def somente_numeros(char):
    return char.isdigit()


# Criando a Interface com Tkinter
def criar_interface():
    root = tk.Tk()
    root.title("Cadastro Castra Móvel")
    
    # Labels e Entradas para os campos do formulário
    labels = ["Data", "Nome", "Contato", "RG", "CPF", "NIS", "Endereço", "Nome do Pet", 
              "Espécie", "Cor", "Peso", "Idade", "Porte", "Raça", "Sexo"]
    entries = {}
    
    for idx, label in enumerate(labels):
        tk.Label(root, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        if label in ["Espécie", "Porte", "Sexo"]:
            if label == "Espécie":
                values = ["Felino", "Canino"]
            elif label == "Porte":
                values = ["Pequeno", "Médio", "Grande"]
            elif label == "Sexo":
                values = ["Fêmea", "Macho"]
            entries[label] = ttk.Combobox(root, values=values, state="readonly")
        elif (label == "Data") or (label == "RG") or (label == "CPF") or (label == "Contato") or (label == "NIS"):
            vcmd = (root.register(somente_numeros), '%S')
            entries[label] = tk.Entry(root, validate="key", validatecommand=vcmd)
        else:
            entries[label] = tk.Entry(root)
        entries[label].grid(row=idx, column=1, padx=10, pady=5, sticky="w")
    
    def salvar_dados():
        dados = [entries[label].get() for label in labels]
        adicionar_usuario(*dados)
    
    # Botões
    tk.Button(root, text="Salvar", command=salvar_dados).grid(row=len(labels), columnspan=2, pady=10)
    tk.Button(root, text="Visualizar Dados", command=visualizar_dados).grid(row=len(labels)+1, columnspan=2, pady=10)
    tk.Button(root, text="Editar Usuário", command=editar_usuario).grid(row=len(labels)+2, columnspan=2, pady=10)
    tk.Button(root, text="Exportar para Excel", command=exportar_para_excel).grid(row=len(labels)+3, column=0, pady=10)
    tk.Button(root, text="Exportar para CSV", command=exportar_para_csv).grid(row=len(labels)+3, column=1, pady=10)
    
    # Inicia o loop da interface
    root.mainloop()

criar_tabela()
# Criar a interface gráfica
criar_interface()
