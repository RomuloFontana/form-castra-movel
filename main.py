import sqlite3
import openpyxl
import pandas as pd
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import Tk, Label, Entry, Button
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

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
                        sexo TEXT,
                        observacoes TEXT)''')
    conexao.commit()
    conexao.close()

# Função para adicionar um novo usuário
def adicionar_usuario(data, nome, contato, rg, cpf, nis, endereço, bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo, observacoes):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO usuarios 
                    (data, nome, contato, rg, cpf, nis, endereço, bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo, observacoes) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (data, nome, contato, rg, cpf, nis, endereço, bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo, observacoes))
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
def atualizar_usuario(id, data, nome, contato, rg, cpf, nis, endereço, bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo, observacoes):
    conexao = sqlite3.connect('banco_dados.db')
    cursor = conexao.cursor()
    cursor.execute('''UPDATE usuarios 
                    SET data = ?, nome = ?, contato = ?, rg = ?, cpf = ?, nis = ?, endereço = ?, bairro = ?, 
                        nome_pet = ?, especie = ?, cor = ?, peso = ?, idade = ?, porte = ?, raca = ?, sexo = ?, observacoes = ? 
                    WHERE id = ?''', 
                    (data, nome, contato, rg, cpf, nis, endereço,bairro, nome_pet, especie, cor, peso, idade, porte, raca, sexo, observacoes, id ))
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
                                        'Espécie', 'Cor', 'Peso', 'Idade', 'Porte', 'Raça', 'Sexo', 'Observações'])
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

    # Adicionando barras de rolagem
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical")
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal")
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    # Criando o Treeview com ligação às barras de rolagem
    colunas = ["ID", "Data", "Nome", "Contato", "RG", "CPF", "NIS", "Endereço","Bairro", "Nome do Pet",
              "Espécie", "Cor", "Peso", "Idade", "Porte", "Raça", "Sexo", "Observações"]
    tree = ttk.Treeview(frame, columns=colunas, show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    
    # Ligando as barras de rolagem ao Treeview
    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configurando as colunas do Treeview
    fonte = tkFont.Font()
    for coluna in colunas:
        tree.heading(coluna, text=coluna)
        # Calcular a largura com base no cabeçalho
        largura = fonte.measure(coluna)
        tree.column(coluna, width=largura, anchor=tk.CENTER)
    
    # Inserindo os dados na tabela
    for usuario in usuarios:
        tree.insert("", tk.END, values=usuario)

    # Ajustando automaticamente o tamanho das colunas com base nos valores inseridos
    for i, coluna in enumerate(colunas):
        max_width = fonte.measure(coluna)
        for item in tree.get_children():
            valor = tree.set(item, coluna)
            if valor:
                largura = fonte.measure(valor)
                if largura > max_width:
                    max_width = largura
        # Adicionar um buffer para melhor visualização
        tree.column(coluna, width=max_width + 20)



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

    largura_desejada = int(janela_edicao.winfo_screenwidth() * 0.3)
    altura_desejada = int(janela_edicao.winfo_screenheight() * 1.0)
    centralizar_janela(janela_edicao, largura_desejada, altura_desejada)
    
    frame_principal = tk.Frame(janela_edicao)
    frame_principal.pack(fill=tk.BOTH, expand=True)
    
    # Adicionando um Canvas para suportar a scrollbar
    canvas = tk.Canvas(frame_principal)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Adicionando a scrollbar vertical
    scrollbar_vertical = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Configurando o Canvas para usar a scrollbar
    canvas.configure(yscrollcommand=scrollbar_vertical.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Criando outro Frame dentro do Canvas para conter os widgets
    frame_conteudo = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_conteudo, anchor="nw")

    labels = ["Data:", "Nome:", "Contato:", "RG:", "CPF:", "NIS:", "Endereço:", "Bairro", "Nome do Pet:", 
              "Espécie:", "Cor:", "Peso:", "Idade:", "Porte:", "Raça:", "Sexo:", "Observações:"]
    
    # Criando dicionário de valores iniciais
    valores_iniciais = dict(zip(labels, usuario[1:]))  # usuario[1:] porque o primeiro elemento é o ID
    
    entries = criar_campos_formulario(frame_conteudo, labels, valores_iniciais)
    
    def salvar_edicao():
        dados = []
        for label in labels:
            if label == "Observações:":
                dados.append(entries[label].get("1.0", tk.END).strip())
            else:
                dados.append(entries[label].get().strip())
        
        # Atualizar o usuário no banco de dados
        atualizar_usuario(id_usuario, *dados)
        janela_edicao.destroy()

    # Botões
    tk.Button(frame_conteudo, text="Salvar", command=salvar_edicao, width=30).grid(row=len(labels), column=0, columnspan=2, pady=10)
    tk.Button(frame_conteudo, text="Cancelar", command=janela_edicao.destroy, width=30).grid(row=len(labels)+1, columnspan=2, pady=10)



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

def limpar_campos(entries):
    for entry in entries.values():
        if isinstance(entry, ttk.Combobox):
            entry.set('')  # Limpa o valor selecionado para combobox
        elif isinstance(entry, tk.Entry):
            entry.delete(0, tk.END)  # Limpa o texto para Entry
        elif isinstance(entry, tk.Text):
            entry.delete('1.0', tk.END)  # Limpa o texto para Text

#---------

def criar_campos_formulario(container, labels, valores_iniciais=None):
    entries = {}
    
    def somente_numeros(char):
        return char.isdigit() or char == "/" or char == "-" or char == "(" or char == ")" or char == " " or char == ""
    
    def formatar_data(entry):
        data = entry.get().replace("/", "")
        if len(data) > 2:
            data = data[:2] + '/' + data[2:]
        if len(data) > 5:
            data = data[:5] + '/' + data[5:]
        if len(data) > 10:
            data = data[:10]
        
        entry.delete(0, tk.END)
        entry.insert(0, data)

    def formatar_contato(entry):
        contato = entry.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        
        # Verificar se o contato está completo
        if len(contato) > 11:
            contato = contato[:11]
        
        # Formatar o contato
        if len(contato) > 6:
            contato = f"({contato[:2]}) {contato[2:7]}-{contato[7:]}"
        elif len(contato) > 2:
            contato = f"({contato[:2]}) {contato[2:]}"
        
        entry.delete(0, tk.END)
        entry.insert(0, contato)


    def formatar_rg(entry):
        rg = entry.get().replace(" ", "")
        if len(rg) > 7:
            rg = rg[:7]
        entry.delete(0, tk.END)
        entry.insert(0, rg)

    def formatar_cpf(entry):
        cpf = entry.get().replace("-", "").replace(" ", "")
        if len(cpf) > 11:
            cpf = cpf[:11]
        if len(cpf) > 9:
            cpf = cpf[:9] + "-" + cpf[9:]
            entry.delete(0, tk.END)
            entry.insert(0, cpf)

    for idx, label in enumerate(labels):
        tk.Label(container, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        
        if label == "Observações:":
            text_area = tk.Text(container, height=5, width=30, wrap="word")
            scrollbar = ttk.Scrollbar(container, command=text_area.yview)
            text_area.config(yscrollcommand=scrollbar.set)

            if valores_iniciais:
                text_area.insert("1.0", valores_iniciais.get(label, ""))  # Inserindo texto no índice "1.0" em vez de "0"

            text_area.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            scrollbar.grid(row=idx, column=2, sticky="ns")
            entries[label] = text_area

        elif label == "Data:":
            entry = tk.Entry(container, width=20)
            entry.insert(0, valores_iniciais.get(label, "") if valores_iniciais else "")
            
            entry.bind("<KeyRelease>", lambda event, e=entry: formatar_data(e))
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            entries[label] = entry

        elif label == "Contato:":
            entry = tk.Entry(container, width=20)
            entry.insert(0, valores_iniciais.get(label, "") if valores_iniciais else "")
            entry.bind("<KeyRelease>", lambda event, e=entry: formatar_contato(e))
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            entries[label] = entry

        elif label == "RG:":
            entry = tk.Entry(container, width=20)
            entry.insert(0, valores_iniciais.get(label, "") if valores_iniciais else "")
            entry.bind("<KeyRelease>", lambda event, e=entry: formatar_rg(e))
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            entries[label] = entry

        elif label == "CPF:":
            entry = tk.Entry(container, width=20)
            entry.insert(0, valores_iniciais.get(label, "") if valores_iniciais else "")
            entry.bind("<KeyRelease>", lambda event, e=entry: formatar_cpf(e))
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            entries[label] = entry

        elif label in ["Espécie:", "Porte:", "Sexo:"]:
            if label == "Espécie:":
                values = ["Felino", "Canino"]
            elif label == "Porte:":
                values = ["Pequeno", "Médio", "Grande"]
            elif label == "Sexo:":
                values = ["Fêmea", "Macho"]
            
            combobox = ttk.Combobox(container, values=values, state="readonly", width=10)
            if valores_iniciais:
                combobox.set(valores_iniciais.get(label, ""))
            combobox.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            entries[label] = combobox
        
        elif label in ["Data:", "RG:", "CPF:", "Contato:", "NIS:"]:
            vcmd = (container.register(somente_numeros), '%S')
            entry = tk.Entry(container, validate="key", validatecommand=vcmd, width=20)
            if valores_iniciais:
                entry.insert(0, valores_iniciais.get(label, ""))
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            entries[label] = entry
        
        else:
            entry = tk.Entry(container, width=30)
            if valores_iniciais:
                entry.insert(0, valores_iniciais.get(label, ""))
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            entries[label] = entry
    
    return entries




#Fazer upload pro GOOGLE DRIVE------

def upload_drive(root):
    try:
        # Configura o GoogleAuth para usar o arquivo client_secrets.json
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.txt")

        if not gauth.credentials:
            # Define o arquivo client_secrets.json para autenticação
            gauth.LoadClientConfigFile("client_secrets.json")
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile("mycreds.txt")

        drive = GoogleDrive(gauth)

        # Faz o upload do arquivo
        file_upload = "banco_dados.db"
        file_drive = drive.CreateFile({'title': file_upload})
        file_drive.SetContentFile(file_upload)
        file_drive.Upload()

        # Mensagem de sucesso
        messagebox.showinfo("Sucesso", "Arquivo enviado para o Google Drive com sucesso!")
    except Exception as e:
        # Mensagem de erro
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        
# Criando a Interface com Tkinter------------------------------------------------------------------

# Função para centralizar a janela e definir seu tamanho com base na resolução do monitor
def centralizar_janela(root, largura_desejada, altura_desejada):
    # Obter a largura e altura da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    # Calcular as coordenadas para centralizar a janela
    x = (largura_tela - largura_desejada) // 2
    y = (altura_tela - altura_desejada) // 6

    # Definir o tamanho e posição da janela
    root.geometry(f"{largura_desejada}x{altura_desejada}+{x}+{y}")

# Função para criar a interface----------------------
def criar_interface():
    root = tk.Tk()
    root.title("Cadastro Castra Móvel")
    
    largura_desejada = int(root.winfo_screenwidth() * 0.3)
    altura_desejada = int(root.winfo_screenheight() * 0.89)
    centralizar_janela(root, largura_desejada, altura_desejada)
    
    # root_google = Tk()
    # root_google.title("Upload para Google Drive")
    # Label(root_google, text="E-mail do Google:").grid(row=0, column=0, padx=10, pady=10)
    # email_entry = Entry(root_google, width=30)
    # email_entry.grid(row=0, column=1, padx=10, pady=10)
    # Button(root_google, text="Fazer Backup", command=lambda: upload_drive(email_entry.get())).grid(row=1, column=1, padx=10, pady=10)

    frame_principal = tk.Frame(root)
    frame_principal.pack(fill=tk.BOTH, expand=True)
    
    # Adicionando um Canvas para suportar a scrollbar
    canvas = tk.Canvas(frame_principal)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Adicionando a scrollbar vertical
    scrollbar_vertical = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Configurando o Canvas para usar a scrollbar
    canvas.configure(yscrollcommand=scrollbar_vertical.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Criando outro Frame dentro do Canvas para conter os widgets
    frame_conteudo = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_conteudo, anchor="nw")

    labels = ["Data:", "Nome:", "Contato:", "RG:", "CPF:", "NIS:", "Endereço:", "Bairro", "Nome do Pet:", 
              "Espécie:", "Cor:", "Peso:", "Idade:", "Porte:", "Raça:", "Sexo:", "Observações:"]
    
    entries = criar_campos_formulario(frame_conteudo, labels)
    
    def salvar_dados():
        dados = {}
        for label in labels:
            if label == "Observações:":
                dados[label] = entries[label].get("1.0", tk.END).strip()
            else:
                dados[label] = entries[label].get().strip()
        
        # Verificar se todos os campos obrigatórios estão preenchidos
        campos_obrigatorios = ["Data:", "Nome:", "Nome do Pet:", "Espécie:", "Porte:", "Sexo:"]
        campos_faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]

        if campos_faltando:
            messagebox.showerror("Erro", f"Os seguintes campos são obrigatórios e devem ser preenchidos: {', '.join(campos_faltando)}")
            return

        data = dados['Data:']
        if len(data) != 10 or not data[2] == '/' or not data[5] == '/':
            messagebox.showerror("Erro", "A data deve estar no formato dd/mm/yyyy e conter 10 caracteres.")
            return
        
        adicionar_usuario(*[dados[label] for label in labels])
        limpar_campos(entries)

    # Botões
    tk.Button(frame_conteudo, text="Salvar", command=salvar_dados, width=30).grid(row=len(labels), column=0, pady=5, columnspan=2, sticky="e")
    tk.Button(frame_conteudo, text="Deletar Usuário", command=deletar_usuario_interface, width=30).grid(row=len(labels)+1, columnspan=2, pady=5, sticky="e")
    tk.Button(frame_conteudo, text="Visualizar Dados", command=visualizar_dados, width=30).grid(row=len(labels)+2, columnspan=2, pady=5, sticky="e")
    tk.Button(frame_conteudo, text="Editar Usuário", command=editar_usuario, width=30).grid(row=len(labels)+3, columnspan=2, pady=5, sticky="e")
    tk.Button(frame_conteudo, text="Exportar para Excel", command=exportar_para_excel, width=30).grid(row=len(labels)+4, column=1, pady=5,  sticky="e")
    tk.Button(frame_conteudo, text="Fazer upload Google Drive", command=lambda: upload_drive(root), width=30).grid(row=len(labels)+5, column=1, pady=5,  sticky="e")
    
    # Inicia o loop da interface
    root.mainloop()


criar_tabela()
criar_interface()
