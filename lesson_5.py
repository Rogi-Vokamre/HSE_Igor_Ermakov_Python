#Задание 1 - найти информацию об организациях
import json
import csv

def search_in_json(file_path, search_keys):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    def recursive_search(data, keys):
        found_values = {}
        if isinstance(data, dict):
            for k, v in data.items():
                if k == 'inn' and v in keys:
                    ogrn = data.get('ogrn', 'Не найдено')
                    address = data.get('address', 'Не найдено')
                    found_values[v] = {'ogrn': ogrn, 'address': address}
                elif isinstance(v, (dict, list)):
                    found_values.update(recursive_search(v, keys))
        elif isinstance(data, list):
            for item in data:
                found_values.update(recursive_search(item, keys))
        return found_values

    return recursive_search(data, search_keys)


def save_to_csv(data, csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['ИНН', 'ОГРН', 'Адрес'])
        for inn, info in data.items():
            writer.writerow([inn, info['ogrn'], info['address']])


file_path = '/Users/igor_ermakov/Desktop/traders.json'
search_keys = ['7702758341', '7802654025', '5027217264', '6324042940', '5834031870', '1657061756', '3665044042', '6453102410']
results = search_in_json(file_path, search_keys)

if results:
    print(f'Найденные значения: {results}')
    csv_file_path = '/Users/igor_ermakov/Desktop/traders.csv'
    save_to_csv(results, csv_file_path)
    print(f'Данные сохранены в CSV файл: {csv_file_path}')
else:
    print(f'Ни один ключ из списка {search_keys} не найден в файле.')