import PySimpleGUI as sg
for i in range(1, 1000):
    sg.one_line_progress_meter(
        'progress_bar',
        i + 1,
        1000,
        'this progress bar key',
        'isto é uma barra de progressão',
        orientation='h',
        bar_color=("#64F464", '#FFFFFF')
    )