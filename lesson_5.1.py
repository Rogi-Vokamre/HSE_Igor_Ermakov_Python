#Написать регулярное выражение для поиска электронных адресов
import json
import re

def find_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return set(re.findall(email_pattern, text))

def collect_emails(data):
    result = {}

    def extract_emails(obj):
        if isinstance(obj, dict):
            inn = obj.get('publisher_inn')
            if inn:
                if inn not in result:
                    result[inn] = set()
                emails = find_emails(json.dumps(obj))
                result[inn].update(emails)

            for value in obj.values():
                extract_emails(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_emails(item)

    extract_emails(data)

    for inn, emails in result.items():
        result[inn] = list(emails)

    return result

with open('/Users/igor_ermakov/Desktop/1000_efrsb_messages.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

emails = collect_emails(data)

with open('emails1.json', 'w', encoding='utf-8') as file:
    json.dump(emails, file, indent=4, ensure_ascii=False)