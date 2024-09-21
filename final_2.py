# Задание № 2 - Парсинг
import requests
from bs4 import BeautifulSoup
import json
import os

class ParserCBRF:
    def __init__(self):
        self.url = 'https://www.cbr.ru/currency_base/daily/'
        self.data_to_save = {}

    def start(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим дату
            date_element = soup.find('h2')
            date_text = date_element.text.strip() if date_element else 'Дата не найдена'

            # Извлекаем нужную часть строки и очищаем от лишних символов
            date_info = date_text.split('без обязательств')[0].strip()
            date_info = date_info.replace('\r', '').replace('\n', '').replace('\t', '').strip()
            date_info = ' '.join(date_info.split())

            # Находим таблицу с курсами валют
            table = soup.find('table', {'class': 'data'})

            # Получаем заголовки таблицы
            headers = [header.text.strip() for header in table.find_all('th')]

            # Собираем строки таблицы + игнорируем СДР (специальные права заимствования)
            rows = []
            for row in table.find_all('tr')[1:]:
                row_data = [cell.text.strip() for cell in row.find_all('td')]
                if row_data and row_data[0] != 'СДР (специальные права заимствования)':
                    rows.append(row_data)

            # Подготовка данных для сохранения в JSON
            self.data_to_save = {
                'date_info': date_info,
                'exchange_rates': [dict(zip(headers, row)) for row in rows]
            }

            # Путь к папке parsed_data
            output_dir = os.path.join(os.getcwd(), 'parsed_data')
            os.makedirs(output_dir, exist_ok=True)

            # Полный путь к файлу
            json_file_path = os.path.join(output_dir, 'exchange_rates.json')

            # Сохраняем данные в JSON файл
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(self.data_to_save, json_file, ensure_ascii=False, indent=4)

            return json_file_path  # Возвращаем путь к файлу
        else:
            return f"Не удалось получить данные. Код ответа: {response.status_code}"

class ExchangeRatesCBRF:
    def __init__(self, data_file='parsed_data/exchange_rates.json'):
        self.data_file = data_file
        self.exchange_rates = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as json_file:
                exchange_rates = json.load(json_file).get('exchange_rates', [])
                return [rate for rate in exchange_rates if rate['Валюта'] != 'СДР (специальные права заимствования)']
        else:
            return []

    def parse_rate(self, rate):
        return float(rate.replace(',', '.'))

    def min_rate(self):
        if not self.exchange_rates:
            return "Нет доступных данных."
        min_currency = min(self.exchange_rates, key=lambda x: self.parse_rate(x.get('Курс', '0')))
        # Возвращаем только нужные данные
        return {
            'Валюта': min_currency['Валюта'],
            'Курс': min_currency['Курс'],
            'Единиц': min_currency['Единиц']
        }

    def max_rate(self):
        if not self.exchange_rates:
            return "Нет доступных данных."
        max_currency = max(self.exchange_rates, key=lambda x: self.parse_rate(x.get('Курс', '0')))
        # Возвращаем только нужные данные
        return {
            'Валюта': max_currency['Валюта'],
            'Курс': max_currency['Курс'],
            'Единиц': max_currency['Единиц']
        }

if __name__ == "__main__":
    parser = ParserCBRF()
    parser.start()

    rates = ExchangeRatesCBRF()  # Загружаем данные о курсах

    while True:
        method = input("Введите метод ('min' для минимального курса, 'max' для максимального курса или 'exit' для выхода): ").strip().lower()

        if method == 'min':
            min_currency = rates.min_rate()
            print(min_currency)
        elif method == 'max':
            max_currency = rates.max_rate()
            print(max_currency)
        elif method == 'exit':
            break
        else:
            pass
