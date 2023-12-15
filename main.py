import requests
from bs4 import BeautifulSoup
import json

def parse_vacancies():
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110 ',
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return 'Ошибка запроса'

    soup = BeautifulSoup(response.text, 'html.parser')
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
    result = []

    for vacancy in vacancies:
        title = vacancy.find('a', {'class': 'bloko-link'}).text
        link = vacancy.find('a', {'class': 'bloko-link'})['href']
        company = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text.strip()
        location = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text.strip()
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        salary = salary.text.strip() if salary else None

        description = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}) or ''
        description += vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}) or ''
        if 'Django' in description.text or 'Flask' in description.text:
            result.append({
                'title': title,
                'link': link,
                'company': company,
                'location': location,
                'salary': salary
            })

    return result

vacancies = parse_vacancies()
print(json.dumps(vacancies, ensure_ascii=False, indent=4))
