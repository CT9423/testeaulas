import PySimpleGUI as sg

class TelaPython:
    def __init__(self):
        #Layout
        Layout = [
        [sg.Text('Nome'),sg.Input()],
        [sg.Text('Email'),sg.Input()],
        [sg.Text('Assunto'),sg.Input()],
        [sg.Button('Solicitar contacto')]
        ]

        #Janela
        janela = sg.Window("Pedido de contacto").layout(Layout)

        #Extrair os dados da Tela
        self.button, self.values = janela.Read()
    
    def Iniciar(self):
        print(self.values)


tela = TelaPython()
tela.Iniciar()