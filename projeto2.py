import os
import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FICHEIRO = "produtos.xlsx"
COL_NOME = "Produto"
COL_UNIDADES = "Unidades Vendidas"


# ---------- Funções de dados (Excel) ----------
def carregar():
    if os.path.exists(FICHEIRO):
        return pd.read_excel(FICHEIRO)
    return pd.DataFrame(columns=[COL_NOME, COL_UNIDADES])


def guardar(df):
    try:
        df.to_excel(FICHEIRO, index=False)
        return True
    except PermissionError:
        messagebox.showerror(
            "Erro", f"Não foi possível gravar '{FICHEIRO}'.\nFeche o ficheiro no Excel e tente de novo."
        )
        return False


# ---------- Aplicação ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Produtos")
        self.geometry("520x480")
        self.minsize(460, 420)

        # --- 1) Tabela de produtos ---
        frame_tabela = ttk.LabelFrame(self, text="Produtos")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self.tabela = ttk.Treeview(
            frame_tabela, columns=("nome", "unidades"), show="headings", height=10
        )
        self.tabela.heading("nome", text="Produto")
        self.tabela.heading("unidades", text="Unidades vendidas")
        self.tabela.column("nome", width=250)
        self.tabela.column("unidades", width=130, anchor="center")
        self.tabela.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        self.tabela.bind("<<TreeviewSelect>>", self.ao_selecionar)

        scroll = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y", pady=5)

        # --- 2) Formulário (adicionar / eliminar) ---
        frame_form = ttk.LabelFrame(self, text="Adicionar / Eliminar produto")
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome = ttk.Entry(frame_form, width=28)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Unidades:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_unidades = ttk.Entry(frame_form, width=12)
        self.entry_unidades.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(frame_form, text="Acrescentar", command=self.adicionar).grid(
            row=0, column=2, padx=5, pady=5
        )
        ttk.Button(frame_form, text="Eliminar", command=self.eliminar).grid(
            row=1, column=2, padx=5, pady=5
        )

        # --- 3) Botões gerais ---
        frame_botoes = ttk.Frame(self)
        frame_botoes.pack(fill="x", padx=10, pady=(5, 10))
        ttk.Button(frame_botoes, text="Ver gráfico de vendas", command=self.ver_grafico).pack(
            side="left"
        )
        ttk.Button(frame_botoes, text="Sair", command=self.destroy).pack(side="right")

        self.atualizar_tabela()

    # ---- 1 - Ver produtos ----
    def atualizar_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for _, linha in carregar().iterrows():
            self.tabela.insert("", "end", values=(linha[COL_NOME], linha[COL_UNIDADES]))

    def ao_selecionar(self, _evento):
        """Ao clicar numa linha, preenche o nome (útil para eliminar)."""
        selecao = self.tabela.selection()
        if selecao:
            nome = self.tabela.item(selecao[0], "values")[0]
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome)

    # ---- 2 - Ver gráfico ----
    def ver_grafico(self):
        df = carregar()
        if df.empty:
            messagebox.showinfo("Gráfico", "Não existem produtos para mostrar.")
            return
        janela = tk.Toplevel(self)
        janela.title("Gráfico de vendas")
        janela.geometry("700x450")

        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.bar(df[COL_NOME], df[COL_UNIDADES], color="steelblue")
        ax.set_title("Vendas por produto")
        ax.set_xlabel("Produto")
        ax.set_ylabel("Unidades vendidas")
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=janela)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Liberta a figura da memória quando a janela fecha
        janela.protocol("WM_DELETE_WINDOW", lambda: (plt.close(fig), janela.destroy()))

    # ---- 3 - Acrescentar produto ----
    def adicionar(self):
        df = carregar()
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Escreva o nome do produto.")
            return
        # Verifica duplicados sem distinguir maiúsculas de minúsculas
        if (df[COL_NOME].astype(str).str.lower() == nome.lower()).any():
            messagebox.showwarning("Aviso", f"O produto '{nome}' já existe.")
            return
        try:
            unidades = int(self.entry_unidades.get())
            if unidades < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Aviso", "Unidades: introduza um número inteiro não negativo.")
            return

        novo = pd.DataFrame({COL_NOME: [nome], COL_UNIDADES: [unidades]})
        if guardar(pd.concat([df, novo], ignore_index=True)):
            self.entry_nome.delete(0, tk.END)
            self.entry_unidades.delete(0, tk.END)
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado.")

    # ---- 4 - Eliminar produto ----
    def eliminar(self):
        df = carregar()
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Escreva (ou selecione) o nome do produto a eliminar.")
            return
        # Pesquisa sem distinguir maiúsculas de minúsculas
        filtro = df[COL_NOME].astype(str).str.lower() == nome.lower()
        if not filtro.any():
            messagebox.showinfo("Eliminar", f"O produto '{nome}' não existe.")
            return
        if messagebox.askyesno("Confirmar", f"Eliminar o produto '{nome}'?"):
            if guardar(df[~filtro]):
                self.entry_nome.delete(0, tk.END)
                self.atualizar_tabela()
                messagebox.showinfo("Eliminar", f"Produto '{nome}' eliminado.")


if __name__ == "__main__":
    App().mainloop()