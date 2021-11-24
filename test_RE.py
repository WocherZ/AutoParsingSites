# Test regular expressions templates
import re

RE_templates = [
    {
        'price': r'\d{1,2}\s*\d{3}\s*\d{3}\s₽',
        'square': r'\d+[,\.]*\d+\sм²|\d+[,\.]*\d+\sм',
        'rooms': r'[ДдвухоОднТтреёх]+комнат[ная]+|[Сc]тудия|[12345]-к|[Пп][Ее][Нн][Тт][Хх][Аа][Уу][Сс]|[12345]-комнатная',
        'floor': r'этаж\s*\d+',
    }
]

examples = ["2-к 45.3 м 2 5 300 100 ₽ Сдача Секция Этаж Окна III кв. 2022 1 2 Внутренний двор"]

for example in examples:
    for template in RE_templates:
        price = re.findall(template.get('price'), example)
        square = re.findall(template.get('square'), example)
        floor = re.findall(template.get('floor'), example)
        rooms = re.findall(template.get('rooms'), example)
        print("Цена: ", price)
        print("Площадь: ", square)
        print("Комнаты: ", rooms)
        print("Этаж: ", floor)
