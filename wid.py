import tkinter as tk #biblioteca tkinter permite criar janelas e interfaces

janela = tk.Tk()   #cria a janela principal

label = tk.Label(janela, text="Olá Mundo")

label.pack() #posiciona e apresenta o texto

janela.mainloop() #mantem a janela aberta e ativa