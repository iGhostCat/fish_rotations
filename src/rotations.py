import pandas as pd
import chardet
import re

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(1000)  # Читаем первые 1000 байт для анализа
        result = chardet.detect(raw_data)
        return result['encoding']

encoding = detect_encoding('../data/50 1мг.txt')
print(f"Кодировка файла: {encoding}")

'''with open('../data/50 1мг.txt', 'r', encoding=encoding) as file:
    for line in file:
        print(line.strip())'''


def parse_rotations(file_path):
    data = []

    with open(file_path, 'r', encoding='IBM866') as f:
        for line in f:
            if not line:
                continue
            if line.startswith(('Right', 'Left', 'Up', 'Down')):
                line = line.replace('\t', ' ')
                line = line.strip()
                print(line)
                line_list = line.split(' ')
                print(line_list)
                line_dict = {'Rotation': line_list[0], 'Time_total': line_list[2], 'Time_start': line_list[3] }
                print(line_dict)




# Использование
df = parse_rotations('../data/50 1мг.txt')

