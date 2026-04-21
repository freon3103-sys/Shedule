from time import time, sleep
from traceback import print_tb

import requests, cloudscraper
from bs4 import BeautifulSoup as bs
from module import Str_shed, Table_shed
import random

def writelinks(url):### открывает файл со ссылками и добавляет новую

    url = url.strip()  # удаляем лишние пробелы и \n, чтобы не было двойных переносов

    try:

        with open("files//Links.txt", "r", encoding='utf-8') as file:

            lines = file.readlines()

    except:

        print("Файл для чтения не найден!")
        lines = []

    # Убираем пустые строки в конце, если есть
    while lines and lines[-1].strip() == "":

        lines.pop()

    # Убедимся, что последняя строка заканчивается на \n
    lines[-1] += "\n" if lines and not lines[-1].endswith("\n") else ""

    # Добавляем новую ссылку с \n
    lines.append(url + '\n')

    # Перезаписываем файл
    with open("files//Links.txt", "w", encoding='utf-8') as file:
        file.writelines(lines)

def compare(old, new):

    mistake = []

    i = 0
    len_new = len(new)

    for x in old:

        if i < len_new:

            print(i)
            print(x)
            print(new[i])

            if x != new[i]:

                mistake.append(x)

        i += 1

    return mistake

def time_test(func):

    def wrapper(*args, **kwargs):

        start_time = time()
        result = func(*args, **kwargs)
        print(time() - start_time)

        return result

    return wrapper

def cod_gettext(url): # скачивание информации со страницы

    code = requests.get(url).text # получение html кода страницы
    code = bs(code, 'html.parser') # превращение его в объект класса BeautifulSoup
    return code

def cod_colors(code):

    first_table = code.get_text().splitlines()[400:]  # Получение кода страницы в текстовом варианте
    color = ["Красным", "Оранжевым", "Фиолетовым", "Синим", "Зелёным", "Коричневым",
             "Полужирным"]  # цвета расписания которые можно встретить в коде
    new_table = []  # создание списка в котором будет содержаться строка с информацией о подмаршруте по цветовому обозначению

    for x in first_table: # перебор строк в поиске строк с упоминанием цвета

        if x and x[0] != " ":

            if any(y in x for y in color):

                new_table.append(x)

    return new_table

def cod_days(new_table):

    color = ["Красным", "Оранжевым", "Фиолетовым", "Синим", "Зелёным", "Коричневым",
             "Полужирным"]

    result = {}  # Создание списка со списками [будние дни, выходные дни]

    if new_table:  # проверка не пустой ли список

        mark = color[0]
        second_table = []  # выходные дни
        bool1 = False  # маркер который покажет, что расписание началось заново, это про дни будни/выходные
        start_count = False  # счетчик для различия между первым запуском перебора и вторым
        first_table = []  # будние дни

        for x in new_table:  # перебор списка с цветами

            if bool1:  # если будние дни уже добавились bool1 переключается и остальной текст добавляется во второй день

                second_table.append(x)
                continue

            else:

                if start_count and mark in x:  # если count не ноль и цвет повторяется значит начался другой день
                    bool1 = True
                    second_table.append(x)
                    result["будние дни"] = first_table
                    continue

                start_count = True
                first_table.append(x)

        if second_table:

            result["выходные дни"] = second_table

        else:

            result["Уточнить дни работы на сайте"] = first_table

    return result

def cod_splittable(table):

    table_shed = []  # создание списка в котором будет находиться расписание

    ### получение таблиц
    for x in table:

        x = str(x).lower()

        if "<table border=\"0\" cellspacing=\"1\">" in x:
            table_shed.append(x)

    return table_shed

def cod_gettime(table_shed):

    all_shed = []

    for x in table_shed:

        # разбивание на элементы таблицы
        table = bs(x, 'html.parser').find_all("tr")

        hour = []

        ### разбивание на отдельные рейсы в виде объектов класса строки который в свою очередь наполнен объектами класса рейсов

        i = int(table[1].decode_contents().splitlines()[2][46:48])
        flight = []
        flight_name = table[0].get_text(strip=False).strip()

        for y in table[2].decode_contents().splitlines()[2:-1]:

            if any(char.isdigit() for char in y):

                hour.append(i)

            y = Str_shed(y[55:], i)
            flight.append(y)
            i += 1

        ### добавляет часы к расписанию и разбивание на подмаршруты, все обрабатывается в отдельном классе

        all_shed.append(Table_shed(flight, flight_name))

    return all_shed

def cod(url):

    code = cod_gettext(url)

    table = code.find_all("table")  # нахождение всех таблиц в коде

    other_table = table[4].get_text() + table[5].get_text() + table[7].get_text()

    new_table = cod_colors(code) # получение списка со строками с информацией о подмаршруте и его цвете

    result = cod_days(new_table) # разбитие по будним и выходным дням

    table_shed = cod_splittable(table) # получение списка с таблицами

    all_shed = cod_gettime(table_shed)

    return all_shed, result, other_table

def parse_func(lines):

        for x in lines:

            for y in x:

                if y.bool:

                    with open(f'files//oldshed//{y.text_name()}_old.txt', "w", encoding='utf-8') as path_name:

                        result = cod(y.url)
                        other_table = result[2]
                        result = cod(y.url)[0]
                        const = result[0].name
                        path_name.writelines("Расписание движения (рабочие дни)\n")
                        count = 0

                        for c_object in result:

                            if const == c_object.name and count:

                                path_name.writelines("Расписание движения (выходные дни)\n")

                            path_name.writelines(f"{c_object.name}\n")

                            for key, value in c_object.result.items():

                                path_name.writelines(f"{key}: {value}\n")

                            count += 1

                        path_name.writelines(other_table)

def chec_func(lines):

    with open(f'files//mistake.txt', "w", encoding='utf-8') as name:

        name.writelines("")

    for x in lines:

        for y in x:

            if y.bool:

                with open(f'files//oldshed//{y.text_name()}_old.txt', "r", encoding='utf-8') as path_name:

                    old_shed = path_name.readlines()
                    new_shed = []
                    result = cod(y.url)
                    other_table = result[2]
                    result = cod(y.url)[0]
                    const = result[0].name
                    new_shed.append("Расписание движения (рабочие дни)\n")
                    count = 0

                    for c_object in result:

                        if const == c_object.name and count:
                            new_shed.append("Расписание движения (выходные дни)\n")

                        new_shed.append(f"{c_object.name}\n")

                        for key, value in c_object.result.items():
                            new_shed.append(f"{key}: {value}\n")

                        count += 1

                    for x in other_table.splitlines(keepends="True"):

                        new_shed.append(x)

                    mistake = compare(old_shed, new_shed)

                    if mistake:

                        with open(f'files//mistake.txt', "a", encoding='utf-8') as path_name:

                            path_name.writelines(f"{y.text_name()}\n")

                            for x in mistake:

                                path_name.writelines(x)

                        with open(f'files//oldshed//{y.text_name()}_old.txt', "w", encoding='utf-8') as path_name:

                            result = cod(y.url)
                            other_table = result[2]
                            result = cod(y.url)[0]
                            const = result[0].name
                            path_name.writelines("Расписание движения (рабочие дни)\n")
                            count = 0

                            for c_object in result:

                                if const == c_object.name and count:
                                    path_name.writelines("Расписание движения (выходные дни)\n")

                                path_name.writelines(f"{c_object.name}\n")

                                for key, value in c_object.result.items():
                                    path_name.writelines(f"{key}: {value}\n")

                                count += 1

                            path_name.writelines(other_table)

def watch_func(lines): # запускает парсинг одного маршрута, проверяя галочку, и возвращает его как список из объектов класса

    for x in lines:

        for y in x:

            if y.bool:

                parse, parse_title, fake = cod(y.url)

                break

    return parse, parse_title