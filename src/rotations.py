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
            line = line.strip()
            if not line or line.startswith(('<', 'key', 'Reset')) or line == 'table':
                continue

            # Разбиваем по табуляции и фильтруем пустые значения
            parts = [p.strip() for p in line.split('\t') if p.strip()]

            # Нас интересуют только строки с Right/Left
            if len(parts) >= 3 and parts[1] in ('Right', 'Left'):
                try:
                    # Извлекаем время (parts[2]) и time2 (последний элемент)
                    time = float(parts[2].replace(',', '.'))
                    time2 = parts[-1] if ':' in parts[-1] else None

                    data.append({
                        'event': parts[1],
                        'time': time,
                        'time2': time2
                    })
                except (ValueError, IndexError) as e:
                    print(f"Ошибка обработки строки: {line}")
                    print(f"Причина: {e}")

    return pd.DataFrame(data)


# Использование
df = parse_rotations('../data/50 1мг.txt')

if not df.empty:
    print("Успешно обработано записей:", len(df))
    print("\nПервые 5 записей:")
    print(df.head())
else:
    print("Не удалось извлечь данные. Проверьте формат файла.")