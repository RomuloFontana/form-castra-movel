perguntar:
se o programa vai ficar só num pc (SIM)
    se sim, dá pra ir fazendo
    salvar o database no google drive ou na nuvem de forma automática ou fazer backup







#----------------------
# # Função do menu de escolhas
# def menu():
#     print("\n1. Adicionar usuário")
#     print("2. Listar usuários")
#     print("3. Atualizar usuário")
#     print("4. Deletar usuário")
#     print("5. Exportar dados para CSV")
#     print("6. Exportar dados para Excel")
#     print("7. Sair")


# while True:
#     menu()
#     escolha = input("Escolha uma opção: ")

#     if escolha == '1':
#         nome = input("Digite o nome do usuário: ")
#         idade = int(input("Digite a idade do usuário: "))
#         adicionar_usuario(nome, idade)
#         print("Usuário adicionado com sucesso!")
#     elif escolha == '2':
#         print("\nTodos os usuários:")
#         listar_usuarios()
#     elif escolha == '3':
#         id = int(input("Digite o ID do usuário a ser atualizado: "))
#         nome = input("Digite o novo nome do usuário: ")
#         idade = int(input("Digite a nova idade do usuário: "))
#         atualizar_usuario(id, nome, idade)
#         print("Usuário atualizado com sucesso!")
#     elif escolha == '4':
#         id = int(input("Digite o ID do usuário a ser deletado: "))
#         deletar_usuario(id)
#         print("Usuário deletado com sucesso!")
#     elif escolha == '5':
#         exportar_para_csv()
#     elif escolha == '6':
#         exportar_para_excel()
#     elif escolha == '7':
#         print("Saindo do programa...")
#         break
#     else:
#         print("Opção inválida. Por favor, escolha uma opção válida.")
#------------------------