import os
import pandas as pd
import matplotlib.pyplot as plt

FICHEIRO = "produtos.xlsx"
COL_NOME = "Produto"
COL_UNIDADES = "Unidades Vendidas"


def carregar():
    if os.path.exists(FICHEIRO):
        return pd.read_excel(FICHEIRO)
    return pd.DataFrame(columns=[COL_NOME, COL_UNIDADES])


def guardar(df):
    df.to_excel(FICHEIRO, index=False)


def ver_produtos():
    df = carregar()
    if df.empty:
        print("\nNão existem produtos.")
        return
    print("\n--- Produtos ---")
    for _, linha in df.iterrows():
        print(f"{linha[COL_NOME]}: {linha[COL_UNIDADES]} unidades vendidas")


def ver_grafico():
    df = carregar()
    if df.empty:
        print("\nNão existem produtos para mostrar.")
        return
    plt.figure(figsize=(8, 5))
    plt.bar(df[COL_NOME], df[COL_UNIDADES], color="steelblue")
    plt.title("Vendas por produto")
    plt.xlabel("Produto")
    plt.ylabel("Unidades vendidas")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()


def adicionar_produto():
    df = carregar()
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("O nome não pode estar vazio.")
        return
    if (df[COL_NOME].astype(str).str.lower() == nome.lower()).any():
        print(f"O produto '{nome}' já existe.")
        return
    try:
        unidades = int(input("Unidades vendidas: "))
        if unidades < 0:
            raise ValueError
    except ValueError:
        print("Valor inválido. Introduza um número inteiro não negativo.")
        return
    novo = pd.DataFrame({COL_NOME: [nome], COL_UNIDADES: [unidades]})
    df = pd.concat([df, novo], ignore_index=True)
    guardar(df)
    print(f"Produto '{nome}' adicionado com sucesso.")


def eliminar_produto():
    df = carregar()
    nome = input("Nome do produto a eliminar: ").strip()
    # Pesquisa sem distinguir maiúsculas de minúsculas
    filtro = df[COL_NOME].astype(str).str.lower() == nome.lower()
    if filtro.any():
        df = df[~filtro]
        guardar(df)
        print(f"Produto '{nome}' eliminado.")
    else:
        print(f"O produto '{nome}' não existe.")


def menu():
    while True:
        print("\n===== MENU =====")
        print("1 - Ver produtos")
        print("2 - Ver gráfico de vendas")
        print("3 - Acrescentar produto novo")
        print("4 - Eliminar produto")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            ver_produtos()
        elif opcao == "2":
            ver_grafico()
        elif opcao == "3":
            adicionar_produto()
        elif opcao == "4":
            eliminar_produto()
        elif opcao == "0":
            print("Até breve!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()