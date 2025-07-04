import pandas as pd
import chardet
import re
from datetime import datetime

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
    data_out = []

    with open(file_path, 'r', encoding='IBM866') as f:
        for line in f:
            if not line:
                continue
            if line.startswith(('Right', 'Left', 'Up', 'Down')):
                line = line.replace('\t', ' ')
                line = line.strip()
                line_list = line.split(' ')
                line_dict = {'Rotation': line_list[0], 'Time_total': line_list[2], 'Time_start': line_list[5] }
                data_out.append(line_dict)

    return data_out

def list_rotations_to_excel(data_list):
    current_time = datetime.now()
    data_df = pd.DataFrame(data_list)
    print(data_df.head(10))
    filename_time = current_time
    foldername = '../data/'
    data_df.to_excel('../data/results.xlsx', index=False)

# Использование
data = parse_rotations('../data/50 1мг.txt') # Путь к сырому файлу
list_rotations_to_excel(data)

