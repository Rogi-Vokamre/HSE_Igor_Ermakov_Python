#Задание № 1 - парсинг
import requests
from bs4 import BeautifulSoup


class ParserCBRF:
    def __init__(self):
        self.url = "https://www.cbr.ru/hd_base/infl/"
        self.data = {}

    def start(self):
        page_content = self._fetch_page_content()
        if page_content:
            parsed_data = self._parse_content(page_content)
            self._save_data(parsed_data)
        else:
            print("Не удалось загрузить страницу.")

    def _fetch_page_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return None

    def _parse_content(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        table = soup.find('table')
        if not table:
            print("Таблица не найдена на странице.")
            return None

        rows = table.find_all('tr')

        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 3:
                date = cells[0].text.strip()  # Дата
                key_rate = cells[1].text.strip()  # Ключевая ставка
                inflation = cells[2].text.strip()  # Инфляция

                self.data[date] = {
                    'key_rate': key_rate,
                    'inflation': inflation
                }

        return self.data

    def _save_data(self, parsed_data):
        if parsed_data:
            for date, values in parsed_data.items():
                print(f"{date}: Ключевая ставка - {values['key_rate']}, Инфляция - {values['inflation']}")
        else:
            print("Нет данных для сохранения.")


parser = ParserCBRF()
parser.start()

