import os
from interface import MenuCandidato


def limpar_tela():
    os.system("clear" if os.name == "posix" else "cls")


def main():
    while True:
        limpar_tela()
        print("=" * 50)
        print("        BEM-VINDO AO SKILLUP")
        print("=" * 50)
        print("\nEscolha seu papel na plataforma:\n")
        print("1. Sou um Candidato")
        print("2. Sair")
        print("-" * 50)

        opcao = input("Digite a opção desejada (1 ou 2): ").strip()

        if opcao == "1":
            menu = MenuCandidato()
            menu.fluxo()  # entra no fluxo do candidato
        elif opcao == "2":
            limpar_tela()
            print("\n=== OBRIGADO POR USAR SKILLUP ===\n")
            print("Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")
            input("Pressione ENTER para continuar...")


if __name__ == "__main__":
    main()
