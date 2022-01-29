import traceback

import PySimpleGUI as sg

from main import main

HEAD = ['ФИО', 'Дата рожд.', 'Место рождения', '№СП', 'Дата СП', 'Мировой суд', '№ ИП', 'ФССП Отдел', 'ФССП Адрес', 'ФИО СПИ', 'Сумма долга', 'Вид задолженности', 'Телефон']

def main_gui():
    layout = [
        [sg.Checkbox(i, True) for i in ['ФИО', 'Дата рожд.', 'Место рождения', '№СП', 'Дата СП']],
        [sg.Checkbox(i, True) for i in ['Мировой суд', '№ ИП', 'ФССП Отдел', 'ФССП Адрес']],
        [sg.Checkbox(i, True) for i in ['ФИО СПИ', 'Сумма долга', 'Вид задолженности', 'Телефон']],
        [sg.Output(size=(70, 5))],
        [sg.Submit('Поиск'), sg.Cancel('Выход')]
    ]
    window = sg.Window('ФССП Парсер', layout)
    while True:  # The Event Loop
        event, values = window.read()
        # print(event, values) #debug
        if event in (None, 'Exit', 'Выход'):
            break

        elif event == 'Поиск':
            if True not in values:
                print('Требуется хотя бы один параметр для выгрузки')
            else:
                try:
                    main(values)
                except:
                    print('ОШИБКА, свяжитесь с разработчиком')
                    print(traceback.format_exc())
                else:
                    print('Успешно!')
                    print('------------------------------')


if __name__ == '__main__':
    main_gui()