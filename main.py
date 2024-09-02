import sqlite3
import openpyxl
import pandas as pd
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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

# Funão reordenar os ID's

def reordenar_ids():
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()

    # Selecionar todos os usuários, ordenados por ID
    cursor.execute('''SELECT id FROM usuarios ORDER BY id''')
    ids = cursor.fetchall()

    # Atualizar os IDs para serem consecutivos
    for novo_id, (id_atual,) in enumerate(ids, start=1):
        cursor.execute('''UPDATE usuarios SET id = ? WHERE id = ?''', (novo_id, id_atual))

    conexao.commit()
    conexao.close()

# Função para deletar um usuário
def deletar_usuario(id):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''DELETE FROM usuarios WHERE id = ?''', (id,))
    conexao.commit()
    conexao.close()

    reordenar_ids()
    messagebox.showinfo("Sucesso","Usuário deletado com sucesso!")

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

    labels = ["Data:", "Nome:", "Contato:", "RG:", "CPF:", "NIS:", "Endereço:", "Bairro", "Nome do Pet:", 
              "Espécie:", "Cor:", "Peso:", "Idade:", "Porte:", "Raça:", "Sexo:"]
    
    # Criando dicionário de valores iniciais
    valores_iniciais = dict(zip(labels, usuario[1:]))  # usuario[1:] porque o primeiro elemento é o ID
    
    entries = criar_campos_formulario(janela_edicao, labels, valores_iniciais)
    
    def salvar_edicao():
        dados = [entries[label].get() for label in labels]
        atualizar_usuario(id_usuario, *dados)
        janela_edicao.destroy()

    tk.Button(janela_edicao, text="Salvar", command=salvar_edicao).grid(row=len(labels), columnspan=2, pady=10)

## Função para deletar um usuário a partir da interface

def deletar_usuario_interface():
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

def limpar_campos(entries):
    for entry in entries.values():
        if isinstance(entry, ttk.Combobox):
            entry.set('')  # Limpa o valor selecionado para combobox
        else:
            entry.delete(0, tk.END)  # Limpa o texto para Entry
#---------

def criar_campos_formulario(container, labels, valores_iniciais=None):
    entries = {}
    
    for idx, label in enumerate(labels):
        tk.Label(container, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        if label in ["Espécie:", "Porte:", "Sexo:"]:
            if label == "Espécie:":
                values = ["Felino", "Canino"]
            elif label == "Porte:":
                values = ["Pequeno", "Médio", "Grande"]
            elif label == "Sexo:":
                values = ["Fêmea", "Macho"]
            
            entries[label] = ttk.Combobox(container, values=values, state="readonly", width=10)
            
            # Se valores iniciais forem fornecidos, preencha os campos com esses valores
            if valores_iniciais:
                entries[label].set(valores_iniciais.get(label, ""))
                
        elif label in ["Data:", "RG:", "CPF:", "Contato:", "NIS:"]:
            vcmd = (container.register(somente_numeros), '%S')
            entries[label] = tk.Entry(container, validate="key", validatecommand=vcmd, width=20)
        else:
            entries[label] = tk.Entry(container, width=30)
        
        # Se valores iniciais forem fornecidos, preencha os campos com esses valores
        if valores_iniciais:
            if label not in ["Espécie:", "Porte:", "Sexo:"]:
                entries[label].insert(0, valores_iniciais.get(label, ""))
        
        entries[label].grid(row=idx, column=1, padx=10, pady=5, sticky="we")
    
    return entries


#Fazer upload pro GOOGLE DRIVE------
# def upload_drive(filename):
#     try:
#         # Autenticação com Google Drive
#         gauth = GoogleAuth()
#         gauth.LocalWebserverAuth()  # Abre um navegador para a autenticação
#         drive = GoogleDrive(gauth)

#         # Cria o arquivo no Google Drive
#         arquivo_drive = drive.CreateFile({'title': filename})
#         arquivo_drive.SetContentFile(filename)
#         arquivo_drive.Upload()
        
#         messagebox.showinfo("Backup Concluído", "O backup foi salvo com sucesso no Google Drive!")
#     except Exception as e:
#         messagebox.showerror("Erro de Backup", f"Falha ao fazer upload para o Google Drive: {e}")

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

# Função para criar a interface----------------------
def criar_interface():
    root = tk.Tk()
    root.title("Cadastro Castra Móvel")
    
    largura_desejada = int(root.winfo_screenwidth() * 0.3)
    altura_desejada = int(root.winfo_screenheight() * 1.0)
    centralizar_janela(root, largura_desejada, altura_desejada)
    
    labels = ["Data:", "Nome:", "Contato:", "RG:", "CPF:", "NIS:", "Endereço:", "Bairro", "Nome do Pet:", 
              "Espécie:", "Cor:", "Peso:", "Idade:", "Porte:", "Raça:", "Sexo:"]
    
    entries = criar_campos_formulario(root, labels)
    
    def salvar_dados():
        dados = {label: entries[label].get() for label in labels}

        # Verificar se todos os campos obrigatórios estão preenchidos
        campos_obrigatorios = ["Data:", "Nome:", "Nome do Pet:", "Espécie:", "Porte:", "Sexo:"]
        campos_faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]

        if campos_faltando:
            messagebox.showerror("Erro", f"Os seguintes campos são obrigatórios e devem ser preenchidos: {', '.join(campos_faltando)}")
            return

        adicionar_usuario(*[dados[label] for label in labels])
        limpar_campos(entries)

    
    # Botões
    tk.Button(root, text="Salvar", command=salvar_dados, width=30).grid(row=len(labels), column=0, pady=5, columnspan=2, sticky="e")
    tk.Button(root, text="Deletar Usuário", command=deletar_usuario_interface, width=30).grid(row=len(labels)+1, columnspan=2, pady=5, sticky="e")
    tk.Button(root, text="Visualizar Dados", command=visualizar_dados, width=30).grid(row=len(labels)+2, columnspan=2, pady=5, sticky="e")
    tk.Button(root, text="Editar Usuário", command=editar_usuario, width=30).grid(row=len(labels)+3, columnspan=2, pady=5, sticky="e")
    tk.Button(root, text="Exportar para Excel", command=exportar_para_excel, width=30).grid(row=len(labels)+4, column=1, pady=5,  sticky="e")
    
    # Inicia o loop da interface
    root.mainloop()

criar_tabela()
criar_interface()
# upload_drive('banco_dados.db')