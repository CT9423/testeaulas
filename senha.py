import PySimpleGUI as sg
text = sg.popup_get_text('Digite a sua senha', password_char='*')
sg.popup(f'Password:{text}')