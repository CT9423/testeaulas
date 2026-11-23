import PySimpleGUI as sg 

#Abre uma janela para selecionar um ficheiro
path = sg.popup_get_file('Escolha o ficheiro que quiser')

#imprime o path para esse ficheiro
print(path)