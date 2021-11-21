import requests
import re
import csv
from bs4 import BeautifulSoup

from residents import RESIDENTIALS
from RE_templates import RE_templates


def get_key(d, value):  # взять ключ из словаря по его значению
    for key in d.keys():
        if d[key] == value:
            return key


def find_same_cls(tag):  # находит список самых частых классов среди детей блока
    """
    Находит список самых частых классов среди детей блока
    :param tag: html element or block
    :return: list of childs with max popular class
    """
    clss = {}
    childs = tag.find_all(recursive=False)
    for child in childs:
        if child:
            child_cls = child.get('class')  # список класов ребёнка
            if child_cls:
                for element in child_cls:
                    if clss.get(element):
                        clss[element] += 1
                    else:
                        clss[element] = 1

    if clss.values():
        max_pop_count = max(clss.values())
        result = {
            "class": get_key(clss, max_pop_count),
            "count": max_pop_count,
        }
        return result
    else:
        return {}


def search_info(residents):
    """
    Основная функция по поиску информации о каждом ЖК

    :param residents: массив из словарей, в которых находится информация о ЖК
    :return:
    """
    for residence in residents:
        if len(residence.get("urls")) == 1:
            for url in residence.get("urls"):
                print("Парсинг урла: ", url)
                data = data_parser(url)
                print("Кол-во квартир:", len(data))
                record_data(data, residence)
        else:
            number = 0
            for url in residence.get("urls"):
                print("Парсинг урла: ", url)
                data = data_parser(url)
                print("Кол-во квартир:", len(data))
                number += 1
                record_data(data, residence, str(number))


def data_parser(url):
    """
    Парсит ссылку и обрабатывает её
    :param url:
    :return:
    """
    response = requests.get(url)
    return get_content(response)


def get_content(html):
    """
    Обрабатывает html-документ
    :param html:
    :return:
    """
    soup = BeautifulSoup(html.text, 'html.parser')
    print(soup)
    blocks = soup.find('body').find_all(['div'])  # Ищет все блоки div

    result_residential = []
    need_blocks = []
    for block in blocks:  # рассматривается один блок div
        dict_cls = find_same_cls(block)
        if dict_cls.get('class') and dict_cls.get('count') > 2:
            need_blocks.append(block)
            # print(dict_cls)
            # print("Кол-во элементов с одним классом ", dict_cls.get('count'))


    for need_block in need_blocks:  # обработка каждого блока, у которого несколько детей с одним классом
        for block in need_block:  # обработка каждого дочернего блока
            text_block = find_text(block)
            # print(text_block)

            for template in RE_templates:
                price = re.findall(template.get('price'), text_block)
                square = re.findall(template.get('square'), text_block)
                floor = re.findall(template.get('floor'), text_block)
                rooms = re.findall(template.get('rooms'), text_block)
                # print("Данные о квартире:", rooms, square, price, floor)
                if validate_data(rooms, square, price, floor):
                    # print("Данные о квартире:", rooms, square, price, floor)
                    flat = {
                        'rooms': rooms[0],
                        'price': price[0],
                        'square': square[0]
                    }
                    if floor:
                        flat['floor'] = re.search(r'\d+', floor[0]).group(0)
                        result_residential.append(flat)
                    break

    return result_residential


def find_text(html):
    result_string = ''
    for string in html.stripped_strings:
        result_string += string + ' '
    result_string.replace('\n', '')
    result_string.replace('\t', '')
    return result_string


def validate_data(rooms, square, price, floor=[]):
    """
    Функция проверки правильности полученных данных из регулярных выражений
    :param rooms:
    :param square:
    :param price:
    :param floor:
    :return:
    """
    if len(rooms) == len(square) == len(price) == 1:
        return True
    else:
        return False


def record_data(data, residence, number=''):
    """
    Запись данных в csv файл(ы)
    :param data:
    :param residence:
    :param number:
    :return:
    """
    file_name = residence.get('name') + number + '.csv'
    with open(file_name, mode="w", encoding='utf-16') as file:
        file_writer = csv.writer(file, delimiter=';', lineterminator="\r")
        file_writer.writerow(['Количество комнат', 'Цена квартиры', 'Площадь', 'Этаж'])
        for flat in data:
            file_writer.writerow([
                flat.get('rooms'),
                flat.get('price'),
                flat.get('square'),
                flat.get('floor')
            ])


if __name__ == '__main__':
    search_info(RESIDENTIALS)
